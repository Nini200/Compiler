# Importing yacc
from typing import Generator
import ply.yacc as yacc
# Importing lexer
from lexer import *
#Importing generator
from generator import *
# Importing commands
from commands import *
# Importing expressions
from expressions import *
# Importing conditions
from conditions import *

# Globals
next_memory_number = 0
variables = {}
variables_to_check_later = []
error_flag = 0
output_file_name = ""

def get_error(message: str):
    global error_flag
    print("ERROR: " + message)
    exit()

def add_variable(pidentifier):
    global next_memory_number
    if pidentifier not in variables.keys():
        var = SimpleVariable(pidentifier, next_memory_number)
        next_memory_number += 1
        variables[var.pidentifier] = var
    else:
        get_error("Powtórna deklaracja zmiennej " + pidentifier )

def add_array_of_variables(pid, start, end):
    global next_memory_number
    if pid not in variables:
        try:
            var = ArrayOfVariables(pid, next_memory_number - start, start, end)
        except ArrayRangeError:
            get_error("Nieprawidłowy zakres tablicy")
        next_memory_number += var.length
        variables[var.pidentifier] = var
    else:
        get_error("Duplikat deklaracji " + pid )

def load_variable(pid):
    if pid not in variables:
        variables_to_check_later.append(pid)
        return pid
    if isinstance(variables[pid], ArrayOfVariables):
        get_error("Nieprawidłowe użycie zmiennej " + pid)
    return variables[pid]

def load_variable_from_array(pid, position):
    if pid not in variables:
        get_error("Brak deklaracji tablicy " + pid)
    if type(variables[pid]) == SimpleVariable:
        get_error("Nieprawidłowe użycie zmiennej " + pid)
    
    array = variables[pid]
        
    if type(position) == int:
        try:
            return array.at_index(position)
        except IndexError:
            get_error("Index poza zasięgiem")
    elif type(position) == str:
        position = load_variable(position)
        check_initialization(position)
        return VariableOfArray(array, position)

def initialize_variable(variable):
    if type(variable) == SimpleVariable:
        variable.is_initialized = True

def check_initialization(variable):
    if type(variable) == SimpleVariable:
        if not variable.is_initialized:
            get_error("Niezadeklarowana zmienna " + variable.pidentifier )

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'DIV', 'TIMES'),
)

# Grammar rules

# Program rules
def p_var_begin_end(p):
    '''program : VAR declarations BEGIN commands END'''
    generator = Generator(p[4], variables, next_memory_number, output_file_name)
    generator.generate_code()

def p_begin_end(p):
    '''program : BEGIN commands END'''
    generator = Generator(p[4], variables, next_memory_number, output_file_name)
    generator.generate_code()

# Value rules
def p_value_num(p):
    '''value : NUM'''
    p[0] = p[1]  # p[1] should be as int


def p_value_identifier(p):
    '''value : identifier'''
    p[0] = p[1]  # p[1] should be as Variable or str (when unknown variable - maybe iterator)

# Declaration rules
def p_declarations_pididentifier(p):
    '''declarations : declarations COMMA PIDENTIFIER'''
    add_variable(p[3])


def p_declarations_pididentifier_array(p):
    '''declarations : declarations COMMA PIDENTIFIER LB NUM COLON NUM RB'''
    add_array_of_variables(p[3], p[5], p[7])
    


def p_declare_pididentifier(p):
    '''declarations : PIDENTIFIER'''
    add_variable(p[1])


def p_declare_array(p):
    '''declarations : PIDENTIFIER LB NUM COLON NUM RB '''
    add_array_of_variables(p[1], p[3], p[5])
    
# Commands rules    
def p_commands_commands_command(p):
    '''commands : commands command'''
    p[0] = list(p[1]) if p[1] else []
    p[0].append(p[2])


def p_commands_command(p):
    '''commands : command'''
    p[0] = [p[1]]

# Command rules
def p_command_read(p):
    '''command : READ identifier SEMICOLON'''
    if type(p[2]) == str and p[2] in variables_to_check_later:
        get_error("Błąd operacji odczytu z: " + p[2])
    elif type(p[2]) == str:
        get_error("Błąd operacji odczytu z: " + p[2])
    initialize_variable(p[2])
    c = ReadCommand(p[2])
    p[0] = ReadCommand(p[2])

def p_command_write(p):
    '''command : WRITE value SEMICOLON'''
    check_initialization(p[2])
    c = WriteCommand(p[2])
    p[0] = WriteCommand(p[2])

def p_command_identifier_expression(p):
    '''command : identifier ASSIGN expression SEMICOLON'''
    if type(p[1]) == str and p[1] in variables_to_check_later:
        get_error("Błąd operacji przypisania do: " + p[1])
    elif type(p[1]) == str:
        get_error("Błąd operacji przypisania do: " + p[1])
    initialize_variable(p[1])
    p[0] = AssignCommand(p[1], p[3])


def p_command_if_then_else(p):
    '''command : IF condition THEN commands ELSE commands ENDIF'''
    p[0] = IfElseCommand(p[2], p[4], p[6])


def p_command_if_then(p):
    '''command : IF condition THEN commands ENDIF'''
    p[0] = IfCommand(p[2], p[4])


def p_command_while_do(p):
    '''command : WHILE condition DO commands ENDWHILE'''
    p[0] = WhileCommand(p[2], p[4])


def p_command_repeat_until(p):
    '''command : REPEAT commands UNTIL condition SEMICOLON'''
    p[0] = RepeatCommand(p[4], p[2])

def p_command_for_from_to_do(p):
    '''command : FOR PIDENTIFIER FROM value TO value DO commands ENDFOR'''
    while p[2] in variables_to_check_later:
        variables_to_check_later.remove(p[2])
    check_initialization(p[4])
    check_initialization(p[6])
    p[0] = ForCommand(p[2], p[4], p[6], p[8])

def p_command_for_from_downto_do(p):
    '''command : FOR PIDENTIFIER FROM value DOWNTO value DO commands ENDFOR'''
    while p[2] in variables_to_check_later:
        variables_to_check_later.remove(p[2])
    check_initialization(p[4])
    check_initialization(p[6])
    p[0] = ForDownCommand(p[2], p[4], p[6], p[8])


# Identifiers
def p_identifier_PIDENTIFIER(p):
    '''identifier : PIDENTIFIER'''
    p[0] = load_variable(p[1])

def p_identifier_array_PIDENTIFIER(p):
    '''identifier : PIDENTIFIER LB PIDENTIFIER RB'''
    p[0] = load_variable_from_array(p[1], p[3])

def p_identifier_array_num(p):
    '''identifier : PIDENTIFIER LB NUM RB'''
    p[0] = load_variable_from_array(p[1], p[3])


# Expression rules
def p_expression_value(p):
    '''expression : value'''
    check_initialization(p[1])
    p[0] = ValueExpression(p[1])

def p_expression_value_plus(p):
    '''expression : value PLUS value'''
    check_initialization(p[1])
    check_initialization(p[3])
    p[0] = AddExpression(p[1], p[3])

def p_expression_value_minus(p):
    '''expression : value MINUS value'''
    check_initialization(p[1])
    check_initialization(p[3])
    p[0] = SubExpression(p[1], p[3])

def p_expression_value_times(p):
    '''expression : value TIMES value'''
    check_initialization(p[1])
    check_initialization(p[3])
    p[0] = MulExpression(p[1], p[3])

def p_expression_value_div(p):
    '''expression : value DIV value'''
    check_initialization(p[1])
    check_initialization(p[3])
    p[0] = DivExpression(p[1], p[3])

def p_expression_value_mod(p):
    '''expression : value MOD value'''
    check_initialization(p[1])
    check_initialization(p[3])
    p[0] = ModExpression(p[1], p[3])

# Conditions
def p_condition_le(p):
    '''condition : value LE value'''
    p[0] = LessCondition(p[1], p[3])

def p_condition_ge(p):
    '''condition : value GE value'''
    p[0] = GreaterCondition(p[1], p[3])


def p_condition_leq(p):
    '''condition : value LEQ value'''
    p[0] = LessEqualsCondition(p[1], p[3])


def p_condition_geq(p):
    '''condition : value GEQ value'''
    p[0] = GreaterEqualsCondition(p[1], p[3])

def p_condition_eq(p):
    '''condition : value EQ value'''
    p[0] = EqualsCondition(p[1], p[3])

def p_condition_neq(p):
    '''condition : value NEQ value'''
    p[0] = NotEqualsCondition(p[1], p[3])

def p_error(p):
    if error_flag == 0:
        print("ERROR: Błąd składni")
        exit()

if __name__ == '__main__':
    from sys import argv

    lex.lex()
    yacc.yacc()
    data = ""
    with open(argv[1], "r") as file:
        data = file.read()
    output_file_name = argv[2]
    yacc.parse(data)