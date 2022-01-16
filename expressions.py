from utils import *

class Expression:
    def __init__(self, variable1, variable2=None):
        self.variable1 = variable1
        self.variable2 = variable2

    def generate_code(self, registry):
        pass


class ValueExpression(Expression):
    def generate_code(self, registry,second_registry="b"):
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

class MulExpression(Expression):
    def generate_code(self, registry="a",second_registry = "b",third_registry="c", fourth_registry="d", fifth_registry="e", sixth_registry = "f"):
        if type(self.variable1) == int and type(self.variable2) == int:
            return load_value_to_registry(self.variable1 * self.variable2, registry, second_registry)
        elif isinstance(self.variable1, SimpleVariable) and type(self.variable2) == int:
            if self.variable2 == 1:
                return ValueExpression(self.variable1).generate_code(registry)
            elif self.variable2 == 0:
                return ["RESET " + registry]
        elif type(self.variable1) == int and isinstance(self.variable2, SimpleVariable):
            if self.variable1 == 1:
                return ValueExpression(self.variable2).generate_code(registry)
            elif self.variable1 == 0:
                return ["RESET " + registry]
        code = load_two_values_to_registries(
            self.variable1, self.variable2, registry, second_registry)
        
        
        # Checking if var1 == 0. If so, 0 is already in a registry so jump out of multiplication code.
        # Assuming we have val1 in a (be aware of that)
        code.append("RESET " + fourth_registry)
        code.append("JZERO 2") # TODO: adjust this number when all multiplication code is completed - jump to the end
        code.append("JUMP 3")
        code.append("RESET a")
        code.append("JUMP 53")
        code.append("JPOS 5")
        code.append("DEC d")
        code.append("RESET " + third_registry)
        code.append("SWAP " + third_registry)
        code.append("SUB " + third_registry)
        code.append("SWAP " + second_registry)
        # Checking if var2 == 0. If so, 0 is already in a registry so jump out of multiplication code.
        # Assuming we have val1 in a (be aware of that)
        code.append("JZERO 46") # TODO: adjust this number when all multiplication code is completed - jump to the end
        code.append("JUMP 3")
        code.append("RESET a")
        code.append("JUMP 43")
        code.append("JPOS 5")
        code.append("INC d")
        code.append("RESET " + third_registry)
        code.append("SWAP " + third_registry)
        code.append("SUB " + third_registry)
        code.append("SWAP " + second_registry)
        '''
        code.append("JPOS 6")# TODO: adjust this number when all multiplication code is completed - jump to dealing with positive numbers
        code.append("RESET " + fourth_registry)
        code.append("SWAP " + fourth_registry)
        code.append("SUB " + fourth_registry)
        code.append("RESET " + fourth_registry)
        code.append("INC " + fourth_registry) # One in e registry if the number was negative

        code.append("DEC " + registry) 
        #If |val1| is one
        code.append("JZERO 2")# TODO: adjust this number when all multiplication code is completed - jump to dealing with positive/negative
        code.append("JUMP 9") # |Val1| > 1 #TODO: Not sure if it should be 3. Should 9 in fact xd
        code.append("SWAP " + fourth_registry)
        code.append("JZERO 2") # Jump to positive number dealing
        code.append("JUMP 3") # TODO: to negative number dealing
        # Val1 == 1
        code.append("ADD " + second_registry)
        code.append("JUMP 54") # TODO: Jump out of multiplication code.
        # Val1 == -1
        code.append("RESET " + registry)
        code.append("SUB " + second_registry)
        code.append("JUMP 51") # TODO: Jump out of multiplication code.
        # |Val1| > 1
        code.append("INC " + registry) # restore val1
        code.append("SWAP " + second_registry)
        code.append("JPOS 10") # TODO: Jump behind dealing with fourth registry value.

        # Val2 < 0
        # Dealing with fourth_registry (sign flag) value
        code.append("SWAP " + fourth_registry)
        code.append("JPOS 2")
        # Fourth_registry was zero (val1 > 0)
        code.append("INC " + registry)
        code.append("JUMP 2")
        code.append("DEC " + registry)
        code.append("SWAP " + fourth_registry)
        # Making |val2|
        code.append("RESET " + third_registry)
        code.append("SWAP " + third_registry)
        code.append("SUB " + third_registry)

        # |Val2| == 1
        code.append("DEC " + registry) 
        #If val1 is one
        code.append("JZERO 2")# TODO: adjust this number when all multiplication code is completed - jump to dealing with positive/negative
        code.append("JUMP 9") # |Val1| > 1 #TODO: Not sure if it should be 3. Should 9 in fact xd
        code.append("SWAP " + fourth_registry)
        code.append("JZERO 2") # Jump to positive number dealing
        code.append("JUMP 3") # TODO: to negative number dealing
        # Val1 == 1
        code.append("ADD " + second_registry)
        code.append("JUMP 32") # TODO: Jump out of multiplication code.
        # Val1 == -1
        code.append("RESET " + registry)
        code.append("SUB " + second_registry)
        code.append("JUMP 29 ") # TODO: Jump out of multiplication code.
        # |Val1| > 1
        code.append("INC " + registry) # restore val1
        '''
        # Multiplication
        # 6th for storing result
        code.append("RESET " + sixth_registry)
        # 5th for original value
        # 1st (a) for shifted value
        code.append("RESET " + fifth_registry)
        code.append("SWAP " + fifth_registry)
        code.append("ADD " + fifth_registry)
        code.append("RESET " + third_registry)
        code.append("DEC " + third_registry)
        code.append("SHIFT " + third_registry)
        code.append("RESET " + third_registry)
        code.append("INC " + third_registry)
        code.append("SHIFT " + third_registry)
        code.append("SUB " + fifth_registry)
        code.append("JNEG 12") # Is odd  #========tu tez porpawic

        code.append("SWAP " + fifth_registry)

        code.append("RESET " + third_registry)
        code.append("DEC " + third_registry)
        code.append("SHIFT " + third_registry)

        code.append("SWAP " + second_registry)

        code.append("RESET " + third_registry)
        code.append("INC " + third_registry)
        code.append("SHIFT " + third_registry)

        code.append("SWAP " + second_registry)

        code.append("JZERO 9") #to jump to jump back EXIT
        code.append("JUMP -21") #to jump to jump back #==========popraw
        code.append("SWAP " + fifth_registry)
        code.append("SWAP " + second_registry)
        code.append("SWAP " + sixth_registry)
        code.append("ADD " + sixth_registry) # Val1 is now in 6th
        code.append("SWAP " + sixth_registry)
        code.append("SWAP " + second_registry)
        code.append("JUMP -16")  #===========tu tez ## zdaje ci sie
        code.append("SWAP " +fourth_registry)
        code.append("JZERO 4")
        code.append("RESET a")
        code.append("SUB " + sixth_registry)
        code.append("JUMP 2")
        code.append("SWAP " + sixth_registry)

        return code #😸😸😸😸😸😸😸😸😸😸

class DivExpression(Expression):
    def generate_code(self, registry="a",second_registry = "b",third_registry="c", fourth_registry="e", fifth_registry="f", sixth_registry = "g"):
        if type(self.variable1) == int and type(self.variable2) == int:
            if(self.variable2==0):
                return ["RESET " + registry]
            else:
                return load_value_to_registry(self.variable1 / self.variable2, registry, second_registry)
        elif isinstance(self.variable1, SimpleVariable) and type(self.variable2) == int:
            if self.variable2 == 1:
                return ValueExpression(self.variable1).generate_code(registry)
            elif self.variable2 == 0:
                return ["RESET " + registry]
        elif type(self.variable1) == int and isinstance(self.variable2, SimpleVariable):
            if self.variable1 == 0:
                return ["RESET " + registry]
        code = load_two_values_to_registries(
            self.variable1, self.variable2, registry, second_registry)

        # val1 in registry a
        # val2 in registry b

        code.append("RESET d")
        code.append("RESET e")
        code.append("RESET f")
        code.append("RESET g")
        code.append("INC g")
        code.append("RESET h")
        code.append("DEC h")
        code.append("INC e")
        
        # Checking if they are 0, positive or nnegative and putting them in registries I want xD
        # In registry f is sign of result; postitive if 0, else - negative
        code.append("JZERO 55")
        code.append("JPOS 5")
        code.append("DEC f")
        code.append("SWAP c")
        code.append("RESET a")
        code.append("SUB c")
        code.append("SWAP b")
        code.append("JZERO 48")
        code.append("JPOS 5")
        code.append("INC f")
        code.append("SWAP c")
        code.append("RESET a")
        code.append("SUB c")
        code.append("SWAP c")

        # WHile val1 > val2
        code.append("RESET a")
        code.append("ADD b")
        code.append("SUB c")
        code.append("JZERO 9") # Val1 == val2
        code.append("JNEG 8") # Val1 < val2
        code.append("SWAP c")
        code.append("SHIFT g")
        code.append("SWAP c")
        code.append("SWAP e")
        code.append("SHIFT g")
        code.append("SWAP e")
        code.append("JUMP -11")

        code.append("RESET a")
        code.append("ADD c")
        code.append("SUB b")
        code.append("JZERO 3")
        code.append("JNEG 2")
        code.append("JUMP 7")
        code.append("SWAP b")
        code.append("SUB c")
        code.append("SWAP b")
        code.append("SWAP d")
        code.append("ADD e")
        code.append("SWAP d")
        code.append("SWAP c")
        code.append("SHIFT h")
        code.append("SWAP c")
        code.append("SWAP e")
        code.append("SHIFT h")
        code.append("JZERO 3") # result in d, modulo in b (?)
        code.append("SWAP e")
        code.append("JUMP -19")

        code.append("SWAP f")
        code.append("JZERO 8")
        code.append("RESET a")
        code.append("SUB d")
        code.append("SWAP b")
        code.append("JZERO 2")
        code.append("DEC b")
        code.append("SWAP b")
        code.append("SWAP d")

        code.append("SWAP d")

        return code

class ModExpression(Expression):
    def generate_code(self, registry="a",second_registry = "b",third_registry="c", fourth_registry="e", fifth_registry="f", sixth_registry = "g"):
        if type(self.variable1) == int and type(self.variable2) == int:
            if(self.variable2==0):
                return ["RESET " + registry]
            else:
                return load_value_to_registry(self.variable1 / self.variable2, registry, second_registry)
        elif isinstance(self.variable1, SimpleVariable) and type(self.variable2) == int:
            if self.variable2 == 1:
                return ValueExpression(self.variable1).generate_code(registry)
            elif self.variable2 == 0:
                return ["RESET " + registry]
        elif type(self.variable1) == int and isinstance(self.variable2, SimpleVariable):
            if self.variable1 == 0:
                return ["RESET " + registry]
        code = load_two_values_to_registries(
            self.variable1, self.variable2, registry, second_registry)

        # val1 in registry a
        # val2 in registry b

        code.append("RESET d")
        code.append("RESET e")
        code.append("RESET f")
        code.append("RESET g")
        code.append("INC g")
        code.append("RESET h")
        code.append("DEC h")

        code.append("INC e")

        # Putting them in registries I want xD
        code.append("SWAP b")
        code.append("JZERO 100")
        code.append("JPOS 5")
        code.append("INC f")
        code.append("SWAP c")
        code.append("RESET a")
        code.append("SUB c")
        code.append("SWAP c")
        code.append("SWAP b")
        code.append("JPOS 10")
        code.append("SWAP f")
        code.append("JZERO 3")
        code.append("INC a") # flag from f is now in a
        code.append("JUMP 2")
        code.append("DEC a") # flag from f is now in a
        code.append("SWAP f") # flag from f is coming back to f from a
        code.append("SWAP b")
        code.append("RESET a")
        code.append("SUB b")
        code.append("SWAP b")


        # WHile val1 > val2
        code.append("RESET a")
        code.append("ADD b")
        code.append("SUB c")
        code.append("JZERO 9") # Val1 == val2
        code.append("JNEG 8") # Val1 < val2
        code.append("SWAP c")
        code.append("SHIFT g")
        code.append("SWAP c")
        code.append("SWAP e")
        code.append("SHIFT g")
        code.append("SWAP e")
        code.append("JUMP -11")

        code.append("RESET a")
        code.append("ADD c")
        code.append("SUB b")
        code.append("JZERO 3")
        code.append("JNEG 2")
        code.append("JUMP 7")
        code.append("SWAP b")
        code.append("SUB c")
        code.append("SWAP b")
        code.append("SWAP d")
        code.append("ADD e")
        code.append("SWAP d")
        code.append("SWAP c")
        code.append("SHIFT h")
        code.append("SWAP c")
        code.append("SWAP e")
        code.append("DEC a")
        code.append("JZERO 5") # result in d, modulo in b (?) #TODO:nnuber to end
        code.append("INC a")
        code.append("SHIFT h")
        code.append("SWAP e")
        code.append("JUMP -21")

        code.append("SWAP f")
        code.append("JZERO 15")
        code.append("JPOS 5")
        code.append("SWAP c")
        code.append("SUB b")
        code.append("SWAP b")
        code.append("JUMP 10")
        code.append("DEC a")
        code.append("JZERO 5")
        code.append("RESET a")
        code.append("SUB b")
        code.append("SWAP b")
        code.append("JUMP 4")
        code.append("SWAP b")
        code.append("SUB c")
        code.append("SWAP b")

        code.append("SWAP b")

        return code