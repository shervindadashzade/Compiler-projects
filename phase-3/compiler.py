# Compiler Course Project - Third Phase
# Team members : 
# M.Hossein Hashemi | Milad Zolfkhani | A.Hossein Dadashzade

import ply.lex as lex
import ply.yacc as yacc


symbol_table = []


def is_in_symbol_table(name):
    isin = False
    for val in symbol_table:
        if val.get('name') == name:
            isin =True
    if(isin == False):
        print("Semantic Error :: variable "+ name +" has not decleared yet but assagined.")

def add_to_symbol_table(token):
  isin = False
  for val in symbol_table:
    if val.get('name') == token.get('name'):
      isin = True
      print("Semantic Error :: duplicated variable")
  if isin == False:
    symbol_table.append(token)



t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_PERC = r'%'
t_LAND = r'&'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRAC = r'\{'
t_RBRAC = r'\}'
t_SLBRAC = r'\['
t_SRBRAC = r'\]'
t_ALBRAC = r'\<'
t_ARBRAC = r'\>'
t_SEMI = r'\;'
t_QUOT = r'\"'
t_COM = r'\,'
t_COL = r'\:'
t_DOT = r'\.'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_SHARP = r'\#'
t_CHARV = r'\'[a-zA-Z0-9_]\''
t_POW = r'\^'
t_NOT = r'\!'

key_words = {
    'if': "IF",
    'then': "THEN",
    'else': "ELSE",
    'while': "WHILE",
    'for': "FOR",
    'is': "IS",
    'true': "TRUE",
    'false': "FALSE",
    'int': "INT",
    'float': "FLOAT",
    'char' : "CHAR",
    'include': "INCLUDE",
    'return': "RETURN",
    'do' : "DO",
    'true' : "TRUE",
    'false' : "FALSE"
}

tokens = [
             'NAME', 'NUMBER', 'ID',
             'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'PERC', 'SEMI', 'QUOT', 'COM', 'COL',
             'LAND',
             'LPAREN', 'RPAREN', 'LBRAC', 'RBRAC', 'SLBRAC', 'SRBRAC', 'ALBRAC', 'ARBRAC', 'SHARP','DOT','CHARV', 'NEWLINE', 'POW', 'NOT'] + list(key_words.values())


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Check for reserved words
    t.type = key_words.get(t.value, 'ID')
    

    return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


#def t_COMMENT(t):
#    r'\*'
#    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    #t.type = key_words.get(t.value, 'NEWLINE')
    #return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


t_ignore = ' \t'


class Filereader:
    def __init__(self, filename):
        self.filename = filename
        self.lines = []

    def read(self):
        file = open(self.filename)
        self.lines = file.readlines()
        file.close()


# Build the lexer
lexer = lex.lex()

# Read Data
file = Filereader("programs/mix.c")
data = ''''''
file.read()
for line in file.lines:
    data += line

print('############################# raw input #####################################')

print(data)

print('######################## after lexical analysis #############################')

lexer.input(data)


while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
print('############################# YACC ##########################')

def p_error(p):
    print("Syntax Error")
    print(p)

def p_stmt_list(p):
    '''stmt_list : stmt
    | stmt_list stmt'''

def p_stmt(p):
    '''stmt : include 
    | vardec
    | assaign
    | if
    | while
    | do_while
    | for'''

def p_include(p):
    'include : SHARP INCLUDE ALBRAC ID DOT ID ARBRAC'
    print('INCLUDE DETECTED LIBRARY ' + p[4]+'.'+p[6])

def p_types(p):
    ''' types : INT 
    | FLOAT 
   | CHAR'''
    p[0] = p[1]

def p_values(p):
    '''values : NUMBER DOT NUMBER
    | NUMBER
    | CHARV
    '''
def p_var_dec(p):
    ''' vardec :  types ID vardec2'''
    print('VARIABLE '+ p[2] + ' HAS DECLEARED')
    add_to_symbol_table({'name':p[2], 'type':p[1]})
   
    
def p_var_dec2(p):
    ''' vardec2 : SEMI
    | EQUALS others_vardec2
    others_vardec2 : values SEMI
    | exp SEMI 
     '''

def p_calc_express1(p):
    '''exp : exp PLUS term
    | exp MINUS term
    | term'''
def p_calc_express2(p):
    '''term : term TIMES factor
    | term DIVIDE factor
    | term POW factor
    | factor
    '''
    if(len(p) > 3):
        print(p[3])
        print(p[1])
    else:
        p[0] = p[1]    
def p_calc_express3(p):
    '''factor : NUMBER
    | ID
    | LPAREN exp RPAREN
    '''
    if(len(p) > 3):
      p[0] = p[2]
    else:
      p[0] = p[1]
def p_condi_express1(p):
    '''con_exp : con_exp ALBRAC other_con_exp
    | con_exp ARBRAC other_con_exp
    | con_exp EQUALS EQUALS other_con_exp
    | con_exp NOT other_con_term2
    | con_term
    other_con_exp : con_term
    | EQUALS con_term
    other_con_term2 : ALBRAC other_con_exp 
    | ARBRAC other_con_exp
    | other_con_exp
    '''
def p_condi_express2(p):
    '''con_term : ID
    | NUMBER
    | LPAREN con_exp RPAREN
    | FALSE
    | TRUE
    '''
def p_assaign(p):
    '''assaign : ID EQUALS other_assaign
    other_assaign : values SEMI
    | exp SEMI
    '''
    if(len(p) > 3):
        print(p[1])
        is_in_symbol_table(p[1])
def p_if(p):
    ''' if : IF LPAREN con_exp RPAREN LBRAC stmt_list others_if
    others_if : RBRAC 
    | RBRAC ELSE LBRAC stmt_list RBRAC
    '''
def p_while(p):
    ''' while : WHILE LPAREN con_exp RPAREN LBRAC stmt_list RBRAC
    '''
def p_do_while(p):
    ''' do_while : DO LBRAC stmt_list RBRAC WHILE LPAREN con_exp RPAREN
    '''
def p_for(p):
    ''' for : FOR LPAREN foropt1 foropt2 foropt3 RPAREN LBRAC stmt_list RBRAC
    foropt1 : assaign
    | vardec
    | SEMI
    foropt2 : con_exp SEMI
    | SEMI
    foropt3 : assaign
    | SEMI
    ''' 
y = yacc.yacc()

y.parse(data)

print(symbol_table)