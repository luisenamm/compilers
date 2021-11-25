import ply.lex as lex
import ply.yacc as yacc

literals = ['=', '+', '-', '*', '-', '/', '^', '(', ')', '{', '}', ';']

reserved = (
	'bool', 
    'int', 
    'float', 
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