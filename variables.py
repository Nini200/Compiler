class SimpleVariable:
    def __init__(self) -> None:
        pass

    def __init__(self, pidentifier, memory_number) -> None:
        self.pidentifier = pidentifier
        self.memory_number = memory_number
        self.is_set = False
        self.is_in_iterator = False
    
class VariableOfArray(SimpleVariable):
    ()