from utils import *
from variables import *
from expressions import *
from conditions import *
import generator 
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
        elif type(self.variable) == str:
            self.code = load_value_to_registry(
                self.variable, "a")
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

class ForCommand(BaseCommand):

    def __init__(self, pid: str,  from_value: int, to_value: int, commands: list):
        self.pid = pid
        self.commands = commands
        self.from_value = from_value
        self.to_value = to_value
        self.code = []

    def generate_code(self, register="a"):
        # optymalizacje: gdy jeden for; przeskoczenie pierwszego wczytania
        self.code = load_value_to_registry(self.from_value, "e")
        self.code.extend(load_value_to_registry(self.to_value, "f"))
        self.code.append("INC f")

        my_iterator = add_iterator(self.pid, self.from_value, self.to_value)

        self.code.extend(load_value_to_registry(my_iterator.memory_location, "d"))

        # e-poczatek iteratora, f-koniec iteratora +1, (+1 dla warunku czy wiekszy)
        # d-memory iteratora, d+1 -> memory konca iteratora
        self.code.extend(["SWAP e", "STORE d", "SWAP e", "INC d", "SWAP f","STORE d", "SWAP f", "DEC d"])
        # --- kody podkomend + store iteratora
        sub_commands_code = ["SWAP e", "STORE d", "SWAP e"]
        for command in self.commands:
            command.generate_code()
            sub_commands_code.extend(command.code)
        # --- kod inkrementacji iteratora
        incrementation_code = load_value_to_registry(
            my_iterator.memory_location, "d")
        incrementation_code.extend(
            ["LOAD d","SWAP e", "INC d", "LOAD d", "SWAP f", "DEC d", "INC e"])
        # --- kod sprawdzenia warunku
        condition_code = ["RESET a", "ADD f", "SUB e"]
        # --- przeskok z warunku poza for'a
        # +1 żeby poza kod, +1 żeby ponad jumpa
        condition_code.append(
            "JZERO " + str(len(sub_commands_code)+len(incrementation_code)+2))
        # --- przeskok do sprawdzania warunku
        jump_code = "JUMP " + \
            str(-(len(sub_commands_code) +
                  len(condition_code) + len(incrementation_code)))

        self.code.extend(condition_code)
        self.code.extend(sub_commands_code)
        self.code.extend(incrementation_code)
        self.code.append(jump_code)
        remove_iterator(my_iterator)


class ForDownCommand(BaseCommand):

    def __init__(self, pid: str,  from_value: int, to_value: int, commands: list):
        self.pid = pid
        self.commands = commands
        self.from_value = from_value
        self.to_value = to_value
        self.code = []

    def generate_code(self, register="a"):
        # optymalizacje: gdy jeden for; przeskoczenie pierwszego wczytania
        self.code = load_value_to_registry(self.from_value, "e")
        self.code.extend(load_value_to_registry(self.to_value, "f"))
        self.code.append("DEC f")

        my_iterator = add_iterator(self.pid, self.from_value, self.to_value)

        self.code.extend(load_value_to_registry(my_iterator.memory_location, "d"))

        # e-poczatek iteratora, f-koniec iteratora +1, (+1 dla warunku czy wiekszy)
        # d-memory iteratora, d+1 -> memory konca iteratora
        self.code.extend(["SWAP e", "STORE d", "SWAP e", "INC d", "SWAP f","STORE d", "SWAP f", "DEC d"])
        # --- kody podkomend + store iteratora
        sub_commands_code = ["SWAP e", "STORE d", "SWAP e"]
        for command in self.commands:
            command.generate_code()
            sub_commands_code.extend(command.code)
        # --- kod inkrementacji iteratora
        incrementation_code = load_value_to_registry(
            my_iterator.memory_location, "d")
        incrementation_code.extend(
            ["LOAD d","SWAP e", "INC d", "LOAD d", "SWAP f", "DEC d", "DEC e"])
        # --- kod sprawdzenia warunku
        condition_code = ["RESET a", "ADD e", "SUB f"]
        # --- przeskok z warunku poza for'a
        # +1 żeby poza kod, +1 żeby ponad jumpa
        condition_code.append(
            "JZERO " + str(len(sub_commands_code)+len(incrementation_code)+2))
        # --- przeskok do sprawdzania warunku
        jump_code = "JUMP " + \
            str(-(len(sub_commands_code) +
                  len(condition_code) + len(incrementation_code)))

        self.code.extend(condition_code)
        self.code.extend(sub_commands_code)
        self.code.extend(incrementation_code)
        self.code.append(jump_code)
        remove_iterator(my_iterator)

def add_iterator(pid, start, end):
    iterator = VariableIterator(
        pid, generator.Generator.next_memory, start, end)
    generator.Generator.next_memory += 2
    if [el for el in generator.Generator.iterators if el.pid == pid]:
        raise IteratorAlreadyExists

    generator.Generator.iterators.append(iterator)
    if pid in generator.Generator.variables:
        generator.Generator.variables[pid].is_in_iterator = True
        generator.Generator.variables[pid].reference_to_iterator = iterator
    return iterator


def remove_iterator(iterator: VariableIterator):
    generator.Generator.iterators.remove(iterator)
    if iterator.pid in generator.Generator.variables:
        generator.Generator.variables[iterator.pid].is_in_iterator = False
        generator.Generator.variables[iterator.pid].reference_to_iterator = None

class IteratorAlreadyExists(Exception):
    pass