class SimpleVariable:
    def __init__(self):
        pass

    def __init__(self, pidentifier, memory_number):
        self.pidentifier = pidentifier
        self.memory_number = memory_number
        self.is_initialized = False
        self.is_in_iterator = False
        self.reference_to_iterator = None
    
class VariableOfArray(SimpleVariable):
    def __init__(self, array, index):
        self.array = array
        self.index = index


class ArrayOfVariables(SimpleVariable):

    def __init__(self, pid, memory_location, start, end):
        if start > end:
            raise ArrayRangeError
        self.pidentifier = pid
        self.start = start
        self.end = end
        self.length = end - start + 1
        self.is_initialized = True
        self.memory_number = memory_location
        self.variables = dict()

    def at_index(self, index: int):
        if not self.start <= index <= self.end:
            raise IndexError
        my_index = index
        if my_index not in self.variables:
            self.variables[my_index] = SimpleVariable(self.pidentifier+"[" + str(my_index) + "]", self.memory_number+my_index)
            self.variables[my_index].is_initialized = True
        return self.variables[my_index]

class ArrayRangeError(Exception):
    pass

class VariableIterator(SimpleVariable):

    def __init__(self, pid, memory_location, start, end):
        self.pid = pid
        self.start = start
        self.end = end
        self.is_initialized = True
        self.memory_location = memory_location
        self.is_in_register = False #used?
        self.register_location = None #used?