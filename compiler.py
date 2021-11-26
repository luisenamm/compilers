import ply.lex as lex
import ply.yacc as yacc

# Lexer
literals = ['=', '+', '-', '*', '-', '/', '^', '(', ')', '{', '}', ';']

reserved = (
	'int',          
    'float', 
    'boolean',
    'string',
    'true', 
    'false',
    'and', 
    'or',	
	'if', 
    'elif', 
    'else',
	'for', 
    'do', 
    'while',	
)

tokens = ('NAME', 'INUMBER', 'FNUMBER', 'STRTEXT', 'EQUAL', 'NOTEQUAL', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL') + reserved

# Tokens
reserved_map = {}
for r in reserved:
    reserved_map[r] = r

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved_map.get(t.value,"NAME")    # Check for reserved words
    return t

t_FNUMBER = r'-?\d+\.\d+' # Both positive and negative
t_INUMBER = r'-?\d+' # Both positive and negative
t_ignore = " \t"
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_GREATER = r'>'
t_LESS = r'<'
t_GREATEREQUAL = r'>='
t_LESSEQUAL = r'<='

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
	print("Illegal character %s" % repr(t.value[0]))
	t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parser
def p_block(p):
    '''
    block : statement ';' block
        | statement ';'
    '''


def p_block_ctrl(p):
    '''
    block : loop block
        | condition block        
        | loop
        | condition
    '''


def p_statement(p):
    '''
    statement : NAME '=' expression
        | expression
        | declare
    '''
    if len(p) == 2:
        p[0] = p[1]

#def p_statement_print(p):
 #   '''statement : PRINT '(' expression ')' '''
  #  print(p[3])'''

def p_expression(p):
    ''' expression : stringexpression
        | numexpression
        | booleanexpression '''
    p[0] = p[1]


def p_stringexpression(p):
    ''' stringexpression : stringexpression '+' stringexpression '''


def p_stringexpression_const(p):
    ''' stringexpression : STRTEXT
        | NAME '''    


def p_numexpression(p):
    ''' numexpression : number
        | numexpression '+' numexpression
        | numexpression '-' numexpression
        | numexpression '*' numexpression
        | numexpression '/' numexpression
        | numexpression '^' numexpression '''
    if len(p) == 2:
        p[0] = p[1] 


def p_number(p):
    ''' number : INUMBER
        | FNUMBER
        | NAME '''


def p_booleanxpression(p):
    ''' booleanxpression : boolval
        | boolcompare
        | booleanexpression and booleanexpression
        | booleanexpression or booleanexpression
        | '(' booleanexpression and booleanexpression ')'
        | '(' booleanexpression or booleanexpression ')' '''

def p_boolval(p):
    ''' boolval : NAME
        | true
        | false '''


def p_boolcompare(p):
    ''' boolcompare : number EQUAL number
        | number NOTEQUAL number
        | number GREATER number
        | number LESS number
        | number GREATEREQUAL number
        | number LESSEQUAL number
        | stringexpression EQUAL stringexpression
        | stringexpression NOTEQUAL stringexpression '''


def p_declare(p):
    ''' declare : numdeclare
        | strdeclare
        | booldeclare '''
    p[0] = p[1]


def p_numdeclare(p):
    ''' numdeclare : int NAME
        | float NAME
        | int NAME '=' numexpression
        | float NAME '=' numexpression '''

def p_strdeclare(p):
    ''' strdeclare : string NAME
        | string NAME '=' stringexpression '''


def p_booldeclare(p):
    ''' booldeclare : boolean NAME
        | boolean NAME '=' boolexpression '''   


def p_condition(p):
    ''' condition : if boolblock braceb
        | if boolblock braceb else braceb
        | if boolblock braceb conditionelif else braceb '''

def p_conditionelif(p):
    ''' conditionelif : elif boolblock braceb
        | elif boolblock braceb conditionelif '''


def p_boolblock(p):
    ''' boolblock : '(' boolexpression ')' '''
    p[0] = p[2]

def p_braceb(p):
    ''' braceb : '{' block '}' '''
    p[0] = p[2]

def p_loop(p):
    ''' loop : forctrl'''
    p[0] = p[1]

def p_forctrl(p):
    ''' forctrl : for forcondition braceb''' 

def p_forcondition(p):
    ''' forcondition : '(' statement ';' statement ';' statement ';' ')' '''

parser = yacc.yacc()

content = []
with open('script.txt') as file:
    content = file.readlines()

for line in content:
    yacc.parse(line)
