from variables import *

def generate_number(number: int, registry, second_registry):
    if number == 0:
        return["RESET " + registry]
    elif number == 1:
        return ["RESET " + registry, "INC " + registry]
    elif number == -1:
        return ["RESET " + registry, "DEC " + registry]
    elif number > 0:
        code = []
        # Consider second registry beeing a?
        code.append("RESET " + second_registry)
        code.append("RESET a")
        code.append("INC " + second_registry)
        binary_number = str(bin(number)[2:])
        for i in range(len(binary_number)):
            if binary_number[i] == "1":
                code.append("INC a")
            if i < len(binary_number) - 1:
                code.append("SHIFT "+ second_registry)
        if registry != "a":
            code.append("SWAP " + registry)
    else:
        code = []
        code.append("RESET " + second_registry)
        code.append("RESET a")
        code.append("INC " + second_registry)
        binary_number = str(bin(-number)[2:])
        for i in range(len(binary_number)):
            if binary_number[i] == "1":
                code.append("INC a")
            if i < len(binary_number) - 1:
                code.append("SHIFT "+ second_registry)
        code.append("DEC " + second_registry)
        code.append("SWAP " + second_registry)
        code.append("SUB " + second_registry)
        if registry != "a":
            code.append("SWAP " + registry)
    return code

def load_value_to_registry(value,registry="a",second_registry="b",third_registry = "c", do_variablearray_memory=False,):
    if type(value) == SimpleVariable:
        code = []
        code.extend(generate_number(value.memory_number, registry,second_registry))
        code.append("LOAD " + registry)
        
        if registry != "a":
            code.append("SWAP " + registry)
        return code
    elif type(value) == int:
        code = []
        code.extend(generate_number(value, registry, second_registry))
        return code
    elif type(value) == VariableOfArray:
        code = load_value_to_registry(value.array.memory_number, registry, second_registry)
        #code.append("PUT")
        code.append("SWAP " + third_registry)
        code.extend(load_value_to_registry(value.index, registry, second_registry))
        #code.append("PUT") # a: wartosc simplevariable, c: poczatek tablicy, d: wartosc do przypisania
        code.append("SWAP " + second_registry)
        code.append("RESET a")
        code.append("ADD " + third_registry )
        code.append("ADD "  + second_registry)
        #code.append("PUT") #&address tego tu -> tab[index]
        if not do_variablearray_memory:
            code.append("LOAD a")
            #code.append("PUT")
            '''
        code.append("PUT") #put a
        
        code.append("SWAP b") #put b
        code.append("PUT")
        code.append("SWAP b")

        code.append("SWAP c") #put c
        code.append("PUT")
        code.append("SWAP c")
        
        code.append("SWAP d")#put d
        code.append("PUT")
        code.append("SWAP d")
        '''
        return code
    else: 
        return ["Fuck it"]

def load_two_values_to_registries(value1, value2, registry1="a", registry2="b", registry3="c"):
    if (registry1 == "a" or registry2 == "a"):
        code = load_value_to_registry(value2, registry2, second_registry=registry3)
        code.extend(load_value_to_registry(
            value1, registry1, second_registry=registry3))
    else: # TODO: Rethink that
        code = load_value_to_registry(value1, registry1, second_registry=registry2)
        code.extend(load_value_to_registry(
            value2, registry2, second_registry=registry3))
    return code
    