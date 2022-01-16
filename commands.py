from utils import *
from variables import *
from expressions import *
from conditions import *

class BaseCommand:
    def __init__(self) -> None:
        self.code = []

    def generate_code(self):
        pass

class EndCommand(BaseCommand):
    def __init__(self):
        self.code = []
    
    def generate_code(self):
        self.code = ["HALT"]

class WriteCommand(BaseCommand):
    def __init__(self,variable):
        self.variable = variable
        self.code = []

    def generate_code(self):
        if type(self.variable) == int:
            self.code = []
            self.code.extend(load_value_to_registry(self.variable, "a", "b"))
            self.code.append("PUT")
        elif type(self.variable) == SimpleVariable:
            self.code = load_value_to_registry(
                self.variable, "a","b")
            self.code.append("PUT")
        elif type(self.variable) == VariableOfArray:
            self.code = load_value_to_registry(
                self.variable, "a")
            # Location of var in "a"
            self.code.append("PUT")

class ReadCommand(BaseCommand):
    def __init__(self,variable):
        self.variable = variable
        self.code = []

    def generate_code(self):
        self.code = load_value_to_registry(
            self.variable.memory_number, "b", "c")
        self.code.append("GET")
        self.code.append("STORE b")

class AssignCommand(BaseCommand):

    def __init__(self, variable, expression: Expression):
        self.variable = variable
        self.expression = expression
        self.code = []

    def generate_code(self, registry="d"):
        self.code = self.expression.generate_code("a","b")
        self.code.append("SWAP d")
        if type(self.variable) == VariableOfArray:
            
            self.code.extend(load_value_to_registry(
                self.variable, "a", do_variablearray_memory=True))
        else:
            self.code.extend(load_value_to_registry(
                self.variable.memory_number, "a", "b"))
        self.code.append("SWAP d")
        self.code.append("STORE d")

class IfCommand(BaseCommand):

    def __init__(self, condition: Condition, commands: list):
        self.condition = condition
        self.commands = commands
        self.code = []

    def generate_code(self, register="a"):
        commands_code = []
        self.code = []
        for command in self.commands:
            command.generate_code()
            commands_code.extend(command.code)
        self.code = self.condition.generate_code(len(commands_code)+1)
        self.code.extend(commands_code)


class IfElseCommand(BaseCommand):

    def __init__(self, condition: Condition, commands_if: list, commands_else: list):
        self.condition = condition
        self.commands_if = commands_if
        self.commands_else = commands_else
        self.code = []

    def generate_code(self, register="a"):
        commands_if_code = []
        commands_else_code = []
        for command in self.commands_if:
            command.generate_code()
            commands_if_code.extend(command.code)

        for command in self.commands_else:
            command.generate_code()
            commands_else_code.extend(command.code)

        self.code = self.condition.generate_code(len(commands_if_code)+2)
        self.code.extend(commands_if_code)
        self.code.append("JUMP " + str(len(commands_else_code) + 1))
        self.code.extend(commands_else_code)

class WhileCommand(BaseCommand):

    def __init__(self, condition: Condition, commands: list):
        self.condition = condition
        self.commands = commands
        self.code = []

    def generate_code(self, register="a"):
        commands_code = []
        for command in self.commands:
            command.generate_code()
            commands_code.extend(command.code)

        self.code = self.condition.generate_code(len(commands_code)+2)
        self.code.extend(commands_code)
        self.code.append("JUMP " + str(-len(self.code)))


class RepeatCommand(BaseCommand):

    def __init__(self, condition: Condition, commands: list):
        self.condition = condition
        self.commands = commands
        self.code = []

    def generate_code(self, register="a"):
        commands_code = []
        for command in self.commands:
            command.generate_code()
            commands_code.extend(command.code)

        self.code = commands_code
        self.code.extend(self.condition.generate_code(-len(self.code)))