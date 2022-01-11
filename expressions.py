from utils import *

class Expression:
    def __init__(self, variable1, variable2=None):
        self.variable1 = variable1
        self.variable2 = variable2

    def generate_code(self, registry):
        pass

class ValueExpression(Expression):
    def generate_code(self, registry,second_registry):
        return load_value_to_registry(self.variable1, registry,second_registry)

class AddExpression(Expression):
    def generate_code(self, registry,second_registry,third_registry="c"):
        if type(self.variable1) == int and type(self.variable2) == int:
            return load_value_to_registry(self.variable1 + self.variable2, registry,second_registry)
        elif isinstance(self.variable1, SimpleVariable) and type(self.variable2) == int:
            if self.variable2 == 0:
                return ValueExpression(self.variable1).generate_code(registry, second_registry)
        elif type(self.variable1) == int and isinstance(self.variable2, SimpleVariable):
            if self.variable1 == 0:
                return ValueExpression(self.variable2).generate_code(registry, second_registry)
        code = load_two_values_to_registries(
            self.variable1, self.variable2, registry, second_registry, third_registry)
        if registry == "a":
            code.append("ADD " + second_registry)
        elif second_registry == "a":
            code.append("ADD " + registry)
            code.append("SWAP " + registry)
        else:
            code.append("SWAP " + registry)
            code.append("ADD " + second_registry)
            code.append("SWAP " + registry)
        return code

class SubExpression(Expression):
    def generate_code(self, registry="a",second_registry = "b",third_registry="c"):
        if type(self.variable1) == int and type(self.variable2) == int:
            return load_value_to_registry(self.variable1 - self.variable2, registry,second_registry)
        elif isinstance(self.variable1, SimpleVariable) and type(self.variable2) == int:
            if self.variable2 == 0:
                return ValueExpression(self.variable1).generate_code(registry, second_registry)
        code = load_two_values_to_registries(
            self.variable1, self.variable2, registry, second_registry, third_registry)
        if registry == "a":
            code.append("SUB " + second_registry)
        elif second_registry == "a":
            code.append("SWAP " + registry)
            code.append("SUB " + registry)
            code.append("SWAP " + registry)
        else:
            code.append("SWAP " + registry)
            code.append("SUB " + second_registry)
            code.append("SWAP " + registry)
        return code