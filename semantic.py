class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.errors = []
    
    def visit(self, node):
        try:
            if node is None:
                return
            
            # Nodo de programa
            if node[0] == 'program':
                for stmt in node[1]:
                    self.visit(stmt)
            
            # Asignación
            elif node[0] == 'assign_expr':
                var_name = node[1]
                value = self.visit(node[2])
                self.symbol_table[var_name] = value
            
            # Operaciones binarias
            elif node[0] == 'binary_expr':
                left = self.visit(node[2])
                right = self.visit(node[3])
                
                # ZeroDivisionError
                if node[1] == 'LI' and right == 0:
                    raise ZeroDivisionError(f"División entre cero en línea {node.lineno}")
                
                # TypeError
                if node[1] in ['II', 'IL', 'IT', 'LI'] and (isinstance(left, str) or isinstance(right, str)):
                    raise TypeError(f"Operación no válida entre tipos en línea {node.lineno}")
                
                # Realizar operación
                if node[1] == 'II':
                    return left + right
                elif node[1] == 'IL':
                    return left - right
                elif node[1] == 'IT':
                    return left * right
                elif node[1] == 'LI':
                    return left / right
                elif node[1] == 'LL':
                    return left == right
                elif node[1] == 'TT':
                    return left != right
                elif node[1] == 'TL':
                    return left <= right
                elif node[1] == 'TI':
                    return left >= right
            
            # ... (resto de las reglas)
            
        except ZeroDivisionError as e:
            self.errors.append(f"ZeroDivisionError: {str(e)}")
        except TypeError as e:
            self.errors.append(f"TypeError: {str(e)}")
        except ValueError as e:
            self.errors.append(f"ValueError: {str(e)}")
        except Exception as e:
            self.errors.append(f"Error semántico: {str(e)}")
    
    def analyze(self, ast):
        self.visit(ast)
        if self.errors:
            for error in self.errors:
                print(error)
            return False
        return True