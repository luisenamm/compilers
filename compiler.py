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