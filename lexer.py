import ply.lex as lex;

#Additional state for comments
states = ( ('comment', 'exclusive'),)

#Tokens
tokens = (
    'VAR', 'BEGIN', 'END',

    'ASSIGN',

    'IF', 'THEN', 'ELSE', 'ENDIF',
    'WHILE', 'DO', 'ENDWHILE',
    'REPEAT','UNTIL',
    'FOR', 'FROM', 'TO', 'DOWNTO', 'ENDFOR',

    'PLUS', 'MINUS', 'TIMES', 'DIV', 'MOD',

    'EQ', 'NEQ', 'LE','GE', 'LEQ', 'GEQ',

    'NUM','PIDENTIFIER',

    'COLON','SEMICOLON', 'COMMA',
    'LB', 'RB', 

    'READ', 'WRITE'
)

# Rules

t_VAR = r'VAR'
t_BEGIN = r'BEGIN'
t_END = r'END'

t_ASSIGN = r'ASSIGN'

t_IF = r'IF'
t_THEN = r'THEN'
t_ELSE = r'ELSE'
t_ENDIF = r'ENDIF'

t_REPEAT = r'REPEAT'
t_UNTIL = r'UNTIL'

t_WHILE = r'WHILE'
t_DO = r'DO'
t_ENDWHILE = r'ENDWHILE'

t_FOR = r'FOR'
t_FROM = r'FROM'
t_TO = r'TO'
t_DOWNTO = r'DOWNTO'
t_ENDFOR = 'ENDFOR'

t_PLUS = r'PLUS'
t_MINUS = r'MINUS'
t_TIMES = r'TIMES'
t_DIV = r'DIV'
t_MOD = r'MOD'

t_EQ = r'EQ'
t_NEQ = r'NEQ'
t_LE = r'LE'
t_GE = r'GE'
t_LEQ = r'LEQ'
t_GEQ = r'GEQ'

t_PIDENTIFIER = r'[_a-z]+'

t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','

t_LB = r'\['
t_RB = r'\]'

t_READ = r'READ'
t_WRITE = r'WRITE'

# Dealing with comments
# Starts 'comment' state
def t_begin_comment(t):
    r'\('
    t.lexer.begin('comment')
    pass

# Ends 'comment' state
def t_comment_end(t):
    r'\)'
    t.lexer.begin('INITIAL')
    pass

# Annything in 'comment' state do nothing
def t_comment_any(t):
    r'.'
    pass

# Providing value associated wuth the token too
def t_NUM(t):
    r'[-]?[0-9]+'
    t.value = int(t.value)
    return t

# Getting line number
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# To ignore whitespaces
t_ignore = '  \t'


def t_error(t) :
    print("Illegal character '%s'" %t.value[0])
    t.lexer.skip(1)

def t_comment_error(t) :
    print("Illegal character in comment '%s'" %t.value[0])
    t.lexer.skip(1)

# Check later if that works too?
#def t_ANY_error(t) :
#    print("Illegal character '%s'" %t.value[0])
#    t.lexer.skip(1)