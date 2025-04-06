import ply.lex as lex

# Lista de nombres de tokens
tokens = [
    # Palabras clave
    'ENTERO', 'FLOTANTE', 'STRING', 'IF', 'WHILE', 'RETURN', 'NULL', 
    'BREAK', 'SWITCH', 'CASE', 'DEFAULT', 'ARRAY', 'PRINT', 'IDENTIFIER', 'ENTERO', 'FLOTANTE', 'STRING',
    'PLUS_OP', 'MINUS_OP', 'MULT_OP', 'DIV_OP', 
    'ASSIGN_OP', 'EQ_OP', 'NE_OP', 'LE_OP', 'GE_OP',
    'IF', 'ELSE', 'WHILE', 'RETURN', 'BREAK',
    
    'SEMICOLON', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    # Caracteres especiales
    
    # Números hexadecimales
    'HEX_0', 'HEX_1', 'HEX_2', 'HEX_3', 'HEX_4', 'HEX_5', 'HEX_6', 
    'HEX_7', 'HEX_8', 'HEX_9', 'HEX_A', 'HEX_B', 'HEX_C', 
    'HEX_D', 'HEX_E', 'HEX_F',
    
    # Operadores
    'PLUS_OP', 'MINUS_OP', 'MULT_OP', 'DIV_OP', 'ASSIGN_OP',
    'EQ_OP', 'GE_OP', 'LE_OP', 'NE_OP',
    
    # Identificadores
    'IDENTIFIER',
    
    # Caracteres especiales (agrega todos los que necesites)
    'CHAR_SPECIAL'
]

# Palabras clave con sus lexemas correspondientes
keywords = {
    'WW': 'ENTERO',
    'WV': 'STRING',
    'Wv': 'IF',
    'wW': 'WHILE',
    'ww': 'RETURN',
    'wV': 'NULL',
    'wv': 'BREAK',
    'VW': 'SWITCH',
    'Vw': 'CASE',
    'VV': 'DEFAULT',
    'Vv': 'ARRAY',
    'vW': 'PRINT'
}

# Números hexadecimales con sus lexemas
hex_numbers = {
    'OO': 'HEX_0',
    'Oo': 'HEX_1',
    'OC': 'HEX_2',
    'Oc': 'HEX_3',
    'oO': 'HEX_4',
    'oo': 'HEX_5',
    'oC': 'HEX_6',
    'oc': 'HEX_7',
    'CO': 'HEX_8',
    'Co': 'HEX_9',
    'cO': 'HEX_A',
    'co': 'HEX_B',
    'cC': 'HEX_C',
    'cc': 'HEX_D'
}

# Operadores con sus lexemas
operators = {
    'II': 'PLUS_OP',
    'IL': 'MINUS_OP',
    'IT': 'MULT_OP',
    'LI': 'DIV_OP',
    'LL': 'ASSIGN_OP',
    'LT': 'EQ_OP',
    'TI': 'GE_OP',
    'TL': 'LE_OP',
    'TT': 'NE_OP'
}

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# En lexer.py, modifica la función t_error para manejar excepciones específicas
def t_error(t):
    # TokenInvalidoException - Carácter no reconocido
    print(f"TokenInvalidoException: Carácter '{t.value[0]}' no válido en línea {t.lineno}")
    t.lexer.skip(1)

# Agrega estas funciones para validar tokens específicos
def validate_identifier(t):
    if not all(c in 'bd' for c in t.value):
        print(f"IdentificadorInvalidCharException: '{t.value}' contiene caracteres no válidos (solo permitidos b,d) en línea {t.lineno}")
        t.lexer.skip(len(t.value))
        return None
    t.type = 'IDENTIFIER'
    return t

def validate_number(t):
    if len(t.value) % 2 != 0:
        print(f"NumeroInvalidSizeException: '{t.value}' tiene tamaño impar (debe ser par) en línea {t.lineno}")
        t.lexer.skip(len(t.value))
        return None
    if not all(c.upper() in ['O', 'C'] for c in t.value):
        print(f"NumeroInvalidCharException: '{t.value}' contiene caracteres no válidos (solo O,o,C,c) en línea {t.lineno}")
        t.lexer.skip(len(t.value))
        return None
    
    # Asignar el tipo de token correcto basado en el valor hexadecimal
    if t.value in hex_numbers:
        t.type = hex_numbers[t.value]
    else:
        print(f"NumeroInvalidHexException: '{t.value}' no es un valor hexadecimal válido en línea {t.lineno}")
        return None
    return t

def validate_keyword(t):
    if len(t.value) != 2:
        print(f"KeywordInvalidSizeException: '{t.value}' no tiene 2 caracteres en línea {t.lineno}")
        t.lexer.skip(len(t.value))
        return None
    if not all(c.upper() in ['W', 'V'] for c in t.value):
        print(f"KeywordInvalidCharException: '{t.value}' contiene caracteres no válidos (solo W,w,V,v) en línea {t.lineno}")
        t.lexer.skip(len(t.value))
        return None
    
    # Asignar el tipo de token correcto basado en el diccionario de keywords
    if t.value in keywords:
        t.type = keywords[t.value]
    else:
        print(f"KeywordInvalidException: '{t.value}' no es una palabra clave válida en línea {t.lineno}")
        return None
    return t

def validate_char(t):
    if len(t.value) != 8:
        print(f"CharInvalidSizeException: '{t.value}' no tiene 8 caracteres en línea {t.lineno}")
        t.lexer.skip(len(t.value))
        return None
    if not all(c.upper() in ['Z'] for c in t.value):
        print(f"CharInvalidCharException: '{t.value}' contiene caracteres no válidos (solo Z,z) en línea {t.lineno}")
        t.lexer.skip(len(t.value))
        return None
    t.type = 'CHAR_SPECIAL'
    return t

def validate_operator(t):
    if len(t.value) != 2:
        print(f"OperatorInvalidSizeException: '{t.value}' no tiene 2 caracteres en línea {t.lineno}")
        t.lexer.skip(len(t.value))
        return None
    if not all(c.upper() in ['I', 'L', 'T'] for c in t.value):
        print(f"OperatorInvalidCharException: '{t.value}' contiene caracteres no válidos (solo I,L,T) en línea {t.lineno}")
        t.lexer.skip(len(t.value))
        return None
    
    # Asignar el tipo de token correcto basado en el diccionario de operadores
    if t.value in operators:
        t.type = operators[t.value]
    else:
        print(f"OperatorInvalidException: '{t.value}' no es un operador válido en línea {t.lineno}")
        return None
    return t

# Modifica las reglas de los tokens para usar estas validaciones
def t_IDENTIFIER(t):
    r'[bd]+'
    return validate_identifier(t)

def t_NUMBER(t):
    r'[OoCc]{2,}'
    return validate_number(t)

def t_KEYWORD(t):
    r'[WwVv]{2}'
    return validate_keyword(t)

def t_CHAR(t):
    r'[Zz]{8}'
    return validate_char(t)

def t_OPERATOR(t):
    r'[ILT]{2}'
    return validate_operator(t)

# Construir el lexer
lexer = lex.lex()

# Prueba del lexer
if __name__ == '__main__':
    data = "WW wW bbdbb LL OO II ( )"
    lexer.input(data)
    for tok in lexer:
        print(tok)