from commands import *

class Generator:
    variables = {}
    #iterators ={}
    next_memory = 0

    def __init__(self) -> None:
        pass

    def __init__(self, commands : list , variables: dict, next_memory: int, output_file: str) -> None:
        self.output_file = output_file
        self.commands = commands
        Generator.next_memory = next_memory
        Generator.variables = variables

    def add_command(self,command):
        self.commands.append(command)

    def generate_code(self):
        self.commands.append(EndCommand())
        output_code = ""
        for command in self.commands:
            if isinstance(command, BaseCommand):
                command.generate_code()
                output_code += "\n".join(command.code) + "\n"
        with open(self.output_file, 'w') as file:
            file.write(output_code)
