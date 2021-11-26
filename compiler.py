import ply.lex as lex
import ply.yacc as yacc

# Lexer
literals = ['=', '+', '-', '*', '-', '/', '^', '(', ')', '{', '}', '"', ';']

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
    'print'
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
t_STRTEXT = r'\"([^\\\n]|(\\.))*?\"'
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
    if len(p) == 4:
        p[0] = Node('block', children = [p[1], p[3]])
    else:
        p[0] = p[1]       

def p_block_ctrl(p):
    '''
    block : loop block
        | condition block        
        | loop
        | condition '''
    if len(p) == 3:
        p[0] = Node('block', children = [p[1], p[2]])
    else:
        p[0] = p[1]


def p_statement(p):
    '''
    statement : NAME '=' expression
        | expression
        | declare '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('assign', children = [Node(p[1]), p[3]])

def p_statement_print(p):
    '''statement : print '(' expression ')' '''
    print(p[3])

def p_expression(p):
    ''' expression : stringexpression
        | numexpression
        | booleanexpression '''
    p[0] = p[1]


def p_stringexpression(p):
    ''' stringexpression : stringexpression '+' stringexpression '''
    p[0] = Node('conc', children = [p[1], p[3]])


def p_stringexpression_const(p):
    ''' stringexpression : STRTEXT
        | NAME '''    
    p[0] = Node('str')

def p_numexpression(p):
    ''' numexpression : number
        | numexpression '+' numexpression
        | numexpression '-' numexpression
        | numexpression '*' numexpression
        | numexpression '/' numexpression
        | numexpression '^' numexpression '''
    if len(p) == 2:
        p[0] = p[1] 
    else:
        p[0] = Node('binop', children = [p[1],p[3]])   


def p_number(p):
    ''' number : INUMBER
        | FNUMBER
        | NAME '''
    p[0] = Node(p[1])

def p_booleanexpression(p):
    ''' booleanexpression : boolval
        | boolcompare
        | booleanexpression and booleanexpression
        | booleanexpression or booleanexpression
        | '(' booleanexpression and booleanexpression ')'
        | '(' booleanexpression or booleanexpression ')' '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = Node('boolean', children = [p[1], p[3]])
    else:
        p[0] = Node('boolop', children = [p[2], p[4]])

def p_boolval(p):
    ''' boolval : NAME
        | true
        | false '''
    p[0] = Node(p[1])


def p_boolcompare(p):
    ''' boolcompare : number EQUAL number
        | number NOTEQUAL number
        | number GREATER number
        | number LESS number
        | number GREATEREQUAL number
        | number LESSEQUAL number
        | stringexpression EQUAL stringexpression
        | stringexpression NOTEQUAL stringexpression '''
    p[0] = Node('comp', children = [p[1], p[3]])


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
    if len(p) == 3:
        p[0] = Node('declaration', children = [Node(p[1]), Node(p[2])])
    else:
        assign = Node('assign', children = [Node(p[2]), p[4]])
        p[0] = Node('declaration', children = [Node(p[1]),assign])

def p_strdeclare(p):
    ''' strdeclare : string NAME
        | string NAME '=' stringexpression '''
    if len(p) == 3:
        p[0] = Node('declaration', children = [Node(p[1]), Node(p[2])])
    else:
        assign = Node('assign', children = [Node(p[2]), p[4]])
        p[0] = Node('declaration', children = [Node(p[1]), assign])


def p_booldeclare(p):
    ''' booldeclare : boolean NAME
        | boolean NAME '=' booleanexpression '''   
    if len(p) == 3:
        p[0] = Node('declaration', children = [Node(p[1]), Node(p[2])])
    else:
        assign = Node('assign', children = [Node(p[2]), p[4]])
        p[0] = Node('declaration', children = [Node(p[1]), assign])

def p_condition(p):
    ''' condition : if boolblock braceb
        | if boolblock braceb else braceb
        | if boolblock braceb conditionelif else braceb '''
    if len(p) == 4:
        p[0] = Node('if', children = [p[2],p[3]])
    elif len(p) == 6:
        p[0] = Node('if', children = [p[2], p[3], p[5]])
    else:
        p[0] = Node('if', children = [p[2], p[3], p[4], p[6]])

def p_conditionelif(p):
    ''' conditionelif : elif boolblock braceb
        | elif boolblock braceb conditionelif '''
    if len(p) == 4:
        p[0] = Node('elif', children = [p[2], p[3]])
    else:
        p[0] = Node('elif', children = [p[2], p[3], p[4]])


def p_boolblock(p):
    ''' boolblock : '(' booleanexpression ')' '''
    p[0] = p[2]

def p_braceb(p):
    ''' braceb : '{' block '}' '''
    p[0] = p[2]

def p_loop(p):
    '''
    loop : forctrl
        | whilectrl
        | dowhilectrl'''
    
    p[0] = p[1]


def p_forctrl(p):
    '''forctrl : for forcond braceb'''
    p[0] = Node('for', children=[p[2], p[3]])


def p_forcond(p):
    '''forcond : '(' statement ';' statement ';' statement ')' '''
    p[0] = Node('forcond', children=[p[2], p[4], p[6]])


def p_whilectrl(p):
    '''whilectrl : while boolblock braceb'''
    p[0] = Node('while', children=[p[2], p[3]])

def p_dowhilectrl(p):
    ''' dowhilectrl : do braceb while boolblock ';' '''
    p[0] = Node('dowhile', children=[p[4], p[2]])

def p_error(p):
    if p:
        print(p)
        print("Syntax error at line '%s' character '%s'" % (p.lineno, p.lexpos) )
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

class Node:
    def __init__(self, ntype, parent = None, children = []):
        self.ntype = ntype
        self.parent = parent
        self.children = children
        if len(self.children) > 0:
            self.add_children()

    def add_children(self):
        for child in self.children:
            child.parent = self

output = parser.parse(lexer= lexer,input=open("script.txt").read())
#print(output)


'''











'''

var = 0
label = 0
tac_str = ""
line = 0
label_stack = []

def wrt_ln(*argv):
	global tac_str
	global line

	for arg in argv:
		tac_str += (str(arg) + ' ')
	tac_str = tac_str[:-1]
	tac_str += '\n'
	line += 1

def get_var():
	global var
	var += 1
	return 'r' + str(var)

def get_label():
	global label
	label += 1
	return 'L' + str(label)

def tac(node):
	if not isinstance(node, Node):
		return node
	
	global line
	global label_stack
	c = node.children

	if node.ntype == 'block':
		tac(c[0])
		if len(c) == 2:
			tac(c[1])
	if node.ntype == 'declaration':
		wrt_ln(c[1], '=', tac(c[1]))		
	if node.ntype == 'boolean':
		return tac(c[0])
	if node.ntype == 'boolop':
		v = get_var()
		wrt_ln(v, '=', tac(c[0]), c[1], tac(c[2]))
		return v
	if node.ntype == 'comp':
		v = get_var()
		wrt_ln(v, '=', tac(c[0]),  tac(c[1]))
		return v
	if node.ntype == 'binop':
		v = get_var()
		wrt_ln(v, '=', tac(c[0]),  tac(c[1]))
		return v
	if node.ntype == 'conc':
		v = get_var()
		wrt_ln(v, '=', tac(c[0]), '+', tac(c[1]))
		return v
	if node.ntype == 'assign':
		wrt_ln(c[0], '=', tac(c[1]))
	if node.ntype == 'if':
		if len(c) == 4:
			label1 = get_label()
			label2 = get_label()
			label_stack.append(label2)

			wrt_ln('if', 'false', tac(c[0]), 'goto', label1)
			tac(c[1])
			wrt_ln('goto', label2)
			wrt_ln(label1)
			tac(c[2])
			tac(c[3])
			wrt_ln(label_stack.pop())			
		elif len(c) == 3:
			label1 = get_label()
			label2 = get_label()
			label_stack.append(label2)

			wrt_ln('if', 'false', tac(c[0]), 'goto', label1)
			tac(c[1])
			wrt_ln('goto', label2)
			wrt_ln(label1)
			tac(c[2])
			wrt_ln(label_stack.pop())
		else:
			label = get_label()
			wrt_ln('if', 'false', tac(c[0]), 'goto', label)
			tac(c[1])
			wrt_ln(label)
	if node.ntype == 'elif':
		if len(c) == 3:
			label = get_label()
			wrt_ln('if', 'false', tac(c[0]), 'goto', label)
			tac(c[1])
			wrt_ln('goto', label_stack[-1])
			wrt_ln(label)
			tac(c[2])
		else:
			label = get_label()
			wrt_ln('if', 'false', tac(c[0]), 'goto', label)
			tac(c[1])
			wrt_ln('goto', label_stack[-1])
			wrt_ln(label)
	if node.ntype == 'else':
		tac(c[0])

	if node.ntype == 'forcond':
		label1 = get_label()
		label2 = get_label()

		tac(c[0])
		wrt_ln(label1)
		wrt_ln('if', 'false', tac(c[1]), 'goto', label2)
		tac(c[3])
		tac(c[2])
		wrt_ln('goto', label1)
		wrt_ln(label2)
	if node.ntype == 'while':
		label1 = get_label()
		label2 = get_label()

		wrt_ln(label1)
		wrt_ln('if', 'false', tac(c[0]), 'goto', label2)
		tac(c[1])
		wrt_ln('goto', label1)
		wrt_ln(label2)
	if node.ntype == 'dowhile':
		label1 = get_label()
		label2 = get_label()

		wrt_ln(label1)
		tac(c[0])
		wrt_ln('if', 'false', tac(c[1]), 'goto', label2)
		wrt_ln('goto', label1)
		wrt_ln(label2)

tac(output)

f = open('output.txt', 'w')
f.write(tac_str)
f.close()
