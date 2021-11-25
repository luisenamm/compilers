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
    ''' type : int 
            | float 
            | boolean 
            | string'''
    p[0] = p[1]

def p_declare(p):
    '''declare : type NAME ';' 
        | type NAME '=' expression ';' '''
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

def p_booleanexpression(p):
    '''booleanexpression : '(' booleanexpression ')'
	            | boolval
				| NAME
                | numexpression compare numexpression
				| booleanexpression boolop booleanexpression'''

def p_numexpression(p):
    '''numexpression : '(' numexpression ')'
		    | INUMBER
			| FNUMBER
			| NAME
			| numexpression binop numexpression'''
    if len(p) == 4 and p[2] =='binop':
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
        elif p[2] == '^':
            p[0] = p[1] ** p[3]

def p_stringexpression(p):
    '''stringexpression : STRTEXT
	        | NAME
            | stringexpression '+' stringexpression
			| stringexpression '+' numexpression'''

def p_boolval(p):
    '''boolval : true
			| false'''  

def p_boolop(p):
    '''boolop : and
			  | or'''

def p_binop(p):
    '''binop : '+'
			 | '-'
			 | '*'
			 | '/'
			 | '^'
	''' 
	
def p_compare(p):
    '''compare : EQUALS
			| NOTEQUALS
			| GREATER
			| LESS
			| GREATEREQUALS
			| LESSEQUALS '''

def p_error(p):
    if p:
        print(p)
        print("Syntax error at line '%s' character '%s'" % (p.lineno, p.lexpos) )
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

content = []
with open('script.txt') as file:
    content = file.readlines()

for line in content:
    yacc.parse(line)
