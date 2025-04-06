class LexicalException(Exception):
    """Excepción base para errores léxicos"""
    pass

class TokenInvalidoException(LexicalException):
    """Cuando un carácter o secuencia no coincide con ninguna regla"""
    pass

class IdentificadorInvalidCharException(LexicalException):
    """Cuando un identificador contiene caracteres no permitidos"""
    pass

class NumeroInvalidSizeException(LexicalException):
    """Cuando un número no tiene el tamaño correcto"""
    pass

class NumeroInvalidCharException(LexicalException):
    """Cuando un número contiene caracteres no permitidos"""
    pass

class SemanticException(Exception):
    """Excepción base para errores semánticos"""
    pass

class ZeroDivisionError(SemanticException):
    """División entre cero"""
    pass

class TypeError(SemanticException):
    """Operación con tipos incorrectos"""
    pass

class ValueError(SemanticException):
    """Valor incorrecto para una operación"""
    pass

class IndexError(SemanticException):
    """Acceso a índice inválido"""
    pass