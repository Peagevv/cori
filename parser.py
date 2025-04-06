from lexer import tokens


# Precedencia de operadores
precedence = (
    ('left', 'PLUS_OP', 'MINUS_OP'),
    ('left', 'MULT_OP', 'DIV_OP'),
    ('nonassoc', 'EQ_OP', 'NE_OP', 'LE_OP', 'GE_OP'),
    ('right', 'UMINUS'),
)

# Tabla de símbolos para análisis semántico
symbol_table = {}

def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

def p_statement_list(p):
    '''statement_list : statement
                     | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : expression_statement
                | compound_statement
                | selection_statement
                | iteration_statement
                | jump_statement'''
    p[0] = p[1]

def p_expression_statement(p):
    '''expression_statement : expression ';' '''
    p[0] = ('expr_stmt', p[1])

def p_compound_statement(p):
    '''compound_statement : '{' statement_list '}' '''
    p[0] = ('compound_stmt', p[2])

def p_selection_statement(p):
    '''selection_statement : IF '(' expression ')' statement
                          | IF '(' expression ')' statement ELSE statement'''
    if len(p) == 6:
        p[0] = ('if_stmt', p[3], p[5])
    else:
        p[0] = ('if_else_stmt', p[3], p[5], p[7])

def p_iteration_statement(p):
    '''iteration_statement : WHILE '(' expression ')' statement'''
    p[0] = ('while_stmt', p[3], p[5])

def p_jump_statement(p):
    '''jump_statement : RETURN expression ';'
                     | BREAK ';'
                     | ';' '''
    if len(p) == 4:
        p[0] = ('return_stmt', p[2])
    elif len(p) == 3:
        p[0] = ('break_stmt',)
    else:
        p[0] = ('empty_stmt',)

def p_expression(p):
    '''expression : assignment_expression
                 | binary_expression
                 | unary_expression
                 | primary_expression'''
    p[0] = p[1]

def p_assignment_expression(p):
    '''assignment_expression : IDENTIFIER ASSIGN_OP expression'''
    try:
        if not all(c in 'bd' for c in p[1]):
            raise IdentificadorInvalidCharException(p.lineno(1), p[1])
        
        expr_type = get_expression_type(p[3])
        if expr_type == 'unknown':
            raise TypeError(p.lineno(2), "Tipo desconocido en asignación")
        
        symbol_table[p[1]] = expr_type
        p[0] = ('assign_expr', p[1], p[3])
    except Exception as e:
        print(e)
        raise SyntaxError

def p_binary_expression(p):
    '''binary_expression : expression PLUS_OP expression
                        | expression MINUS_OP expression
                        | expression MULT_OP expression
                        | expression DIV_OP expression
                        | expression EQ_OP expression
                        | expression NE_OP expression
                        | expression LE_OP expression
                        | expression GE_OP expression'''
    try:
        left_type = get_expression_type(p[1])
        right_type = get_expression_type(p[3])
        
        if p[2] == 'DIV_OP' and right_type == 'number' and is_zero(p[3]):
            raise ZeroDivisionError(p.lineno(2))
        
        if p[2] in ['PLUS_OP', 'MINUS_OP', 'MULT_OP', 'DIV_OP']:
            if left_type != 'number' or right_type != 'number':
                raise TypeError(p.lineno(2), "Operación aritmética requiere números")
        
        p[0] = ('binary_expr', p[2], p[1], p[3])
    except Exception as e:
        print(e)
        raise SyntaxError

def p_unary_expression(p):
    '''unary_expression : MINUS_OP expression %prec UMINUS'''
    try:
        expr_type = get_expression_type(p[2])
        if expr_type != 'number':
            raise TypeError(p.lineno(1), "Operador unario - requiere número")
        p[0] = ('unary_expr', p[1], p[2])
    except Exception as e:
        print(e)
        raise SyntaxError

def p_primary_expression(p):
    '''primary_expression : IDENTIFIER
                         | constant
                         | '(' expression ')' '''
    if len(p) == 2:
        if isinstance(p[1], str) and p[1] not in symbol_table:
            raise NameError(p.lineno(1), f"Identificador '{p[1]}' no declarado")
        p[0] = ('primary', p[1])
    else:
        p[0] = ('paren_expr', p[2])

def p_constant(p):
    '''constant : ENTERO
               | FLOTANTE
               | STRING
               | HEX_0 | HEX_1 | HEX_2 | HEX_3 | HEX_4 | HEX_5
               | HEX_6 | HEX_7 | HEX_8 | HEX_9 | HEX_A | HEX_B
               | HEX_C | HEX_D | HEX_E | HEX_F'''
    p[0] = ('constant', p[1])

def get_expression_type(expr):
    if expr[0] == 'constant':
        if isinstance(expr[1], str):
            return 'string'
        elif isinstance(expr[1], (int, float)):
            return 'number'
    elif expr[0] == 'primary' and isinstance(expr[1], str):
        return symbol_table.get(expr[1], 'unknown')
    elif expr[0] in ['binary_expr', 'unary_expr', 'assign_expr']:
        return get_expression_type(expr[2]) if expr[0] == 'unary_expr' else 'number'
    return 'unknown'

def is_zero(expr):
    if expr[0] == 'constant' and expr[1] == 0:
        return True
    return False

def p_error(p):
    if p:
        raise SyntaxError(f"Error de sintaxis en '{p.value}' en la línea {p.lineno}")
    else:
        raise SyntaxError("Error de sintaxis al final del archivo")

# Construir el parser
parser = yacc.yacc()

def parse_code(code, debug=False):
    try:
        return parser.parse(code, lexer=lexer, debug=debug)
    except Exception as e:
        print(f"Error durante el análisis: {str(e)}")
        return None

if __name__ == '__main__':
    # Ejemplo de uso con código de prueba
    test_code = """
    bd = OO;
    WHILE (bd < cc) {
        bd = bd + Oo;
        IF (bd == CO) {
            PRINT bd;
        }
    }
    """
    ast = parse_code(test_code, debug=True)
    if ast:
        print("AST generado exitosamente:")
        print(ast)