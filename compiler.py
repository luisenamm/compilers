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

tokens = ('NAME', 'INUMBER', 'FNUMBER', 'STRTEXT', 'EQUALS', 'NOTEQUALS', 'GREATER', 'LESS', 'GREATEREQUALS', 'LESSEQUALS') + reserved

# Tokens
reserved_map = {}
for r in reserved:
    reserved_map[r] = r

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

t_FNUMBER = r'-?\d+\.\d+' # Both positive and negative
t_INUMBER = r'-?\d+' # Both positive and negative
t_ignore = " \t"
t_EQUALS = r'=='
t_NOTEQUALS = r'!='
t_GREATER = r'>'
t_LESS = r'<'
t_GREATEREQUALS = r'>='
t_LESSEQUALS = r'<='

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
    '''block : statement block
			 | statement'''
	
def p_statement(p):
	'''statement : declare
			| assign'''

def p_type(p):
    ''' type : int | float | boolean | string'''
    p[0] = p[1]

def p_declare(p):
    '''declare : type NAME '; | type NAME '=' expr ';' '''
    if len(p) == 4:
        p[0] = p[2]
    else: 
        p[0] = p[4]

def p_assign(p):
    '''assign : NAME '=' expression ';' '''
	
def p_statement_print(p):
    '''statement : PRINT '(' expression ')' '''
    print(p[3])

def p_expression(p):
    '''expression : booleanexpression
		| numexpression
		| stringexpression'''

def p_boolexpression(p):
    '''boolexpression : '(' booleanexpression ')'
	            | boolval
				| NAME'''

def p_stringexpression(p):
    '''stringexpression : STRTEXT
	        | NAME'''
	