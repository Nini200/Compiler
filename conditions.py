from utils import *

class Condition:

    def __init__(self, variable1, variable2):
        self.variable1 = variable1
        self.variable2 = variable2
        self.jump_length = 0
        self.is_condition_static = False

    def generate_code(self, jump_length, register1="a", register2="b"):
        pass

    def get_jump_length(self, code: list):
        toret = self.jump_length if self.jump_length >= 0 else self.jump_length - len(code)
        return str(toret)

class LessCondition(Condition):
    def generate_code(self, jump_length, register="a", second_register="b"):
        self.jump_length = jump_length
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 < self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + self.get_jump_length([])]
        code = load_two_values_to_registries(self.variable1, self.variable2, register, second_register, "c")
        code.append("SUB " + second_register )
        code.append("INC a")
        code.append("JPOS " + self.get_jump_length(code)) #when false, jump to else/end
        return code


class GreaterCondition(Condition):
    def generate_code(self, jump_length, register="a", second_register="b"):
        self.jump_length = jump_length
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 > self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + self.get_jump_length([])]
        code = load_two_values_to_registries(self.variable1, self.variable2, register, second_register, "c")
        code.append("SUB " + second_register)
        code.append("DEC a")
        code.append("JNEG " + self.get_jump_length(code)) #when false, jump to else/end
        return code

class LessEqualsCondition(Condition):
    def generate_code(self, jump_length, register="a", second_register="b"):
        self.jump_length = jump_length
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 <= self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + self.get_jump_length([])]
        code = load_two_values_to_registries(self.variable1, self.variable2, register, second_register, "c")
        code.append("SUB " + second_register )
        code.append("JPOS " + self.get_jump_length(code)) #when false, jump to else/end
        return code


class GreaterEqualsCondition(Condition):
    def generate_code(self, jump_length, register="a", second_register="b"):
        self.jump_length = jump_length
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 >= self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + self.get_jump_length([])]
        code = load_two_values_to_registries(self.variable1, self.variable2, register, second_register, "c")
        code.append("SUB " + second_register)
        code.append("JNEG " + self.get_jump_length(code)) #when false, jump to else/end
        return code

class EqualsCondition(Condition):
    def generate_code(self, jump_length, register="a", second_register="b"):
        self.jump_length = jump_length
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 == self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + self.get_jump_length([])]
        code = load_two_values_to_registries(self.variable1, self.variable2, register, second_register, "c")
        code.append("SUB " + second_register)
        code.append("JZERO 2") #when false, jump to else/end
        code.append("JUMP " + self.get_jump_length(code))
        return code

class NotEqualsCondition(Condition):
    def generate_code(self, jump_length, register="a", second_register="b"):
        self.jump_length = jump_length
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 != self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + self.get_jump_length([])]
        code = load_two_values_to_registries(self.variable1, self.variable2, register, second_register, "c")
        code.append("SUB " + second_register)
        code.append("JZERO " + self.get_jump_length(code)) #when false, jump to else/end
        return code