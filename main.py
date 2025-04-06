from lexer import lexer
from parser import parser
from semantic import SemanticAnalyzer
from exceptions import *

def main():
    print("=== Analizador Léxico y Semántico ===")
    print("Ingrese el código a analizar (escriba 'salir' para terminar):")
    
    while True:
        # Leer entrada del usuario
        data = input("> ")
        if data.lower() == 'salir':
            break
        
        try:
            # Análisis léxico
            print("\n=== Análisis Léxico ===")
            lexer.input(data)
            for token in lexer:
                print(token)
            
            # Análisis sintáctico
            print("\n=== Análisis Sintáctico ===")
            ast = parser.parse(data)
            print("Árbol de sintaxis abstracta:", ast)
            
            # Análisis semántico
            print("\n=== Análisis Semántico ===")
            analyzer = SemanticAnalyzer()
            if analyzer.analyze(ast):
                print("Análisis completado sin errores semánticos")
            
        except Exception as e:
            print(f"Error durante el análisis: {str(e)}")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()