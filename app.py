from flask import Flask, request, jsonify, send_from_directory
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


TOKEN_REGEX = [
    (r'\d+\.\d+', 'NUM'),     # Números decimales (válidos)
    (r'\d+', 'NUM_INT'),      # Números enteros (para detectar error)
    (r'[a-zA-Z]+', 'LETTER'), # Letras (para detectar error)
    (r'[+\-*/]', 'OP'),
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
]


def analizar_lexico(expr):
    tokens = []
    pos = 0
    while pos < len(expr):
        if expr[pos].isspace():
            pos += 1
            continue
        match = None
        for patron, tipo in TOKEN_REGEX:
            regex = re.compile(patron)
            m = regex.match(expr, pos)
            if m:
                valor = m.group(0)
                tokens.append({'tipo': tipo, 'valor': valor})
                pos = m.end()
                match = True
                break
        if not match:
            tokens.append({'tipo': 'ERROR', 'valor': expr[pos]})
            pos += 1
    return tokens

def es_ecuacion_aritmetica(tokens):
    """
    Valida que la expresión sea una ecuación aritmética válida con mensajes específicos.
    Cada error indica exactamente qué falta para que funcione.
    """
    if not tokens:
        return False, "EXPRESIÓN VACÍA: Falta toda la expresión. Agrega un número decimal, luego un operador (+, -, *, /), y otro número decimal. Ejemplo: 2.5 + 3.0"
    
    # Verificar errores específicos de tokens
    for token in tokens:
        if token['tipo'] == 'ERROR':
            char_invalido = token['valor']
            return False, f"SÍMBOLO NO VÁLIDO: El símbolo '{char_invalido}' no es reconocido. Falta: usar solo números decimales (2.5), operadores (+, -, *, /) o paréntesis ( )"
        elif token['tipo'] == 'NUM_INT':
            num_entero = token['valor']
            return False, f"FORMATO INCORRECTO: El número '{num_entero}' debe ser decimal. Falta: agregar .0 al final. Cambia '{num_entero}' por '{num_entero}.0'"
        elif token['tipo'] == 'LETTER':
            letras = token['valor']
            return False, f"CARÁCTER INVÁLIDO: Las letras '{letras}' no están permitidas. Falta: reemplazar '{letras}' por un número decimal (ej: 2.5) o quitar las letras completamente."
    
    # Verificar que hay al menos un operador
    operadores = [token for token in tokens if token['tipo'] == 'OP']
    numeros = [token for token in tokens if token['tipo'] == 'NUM']
    
    if len(operadores) == 0:
        if len(numeros) == 1:
            return False, f"FALTA OPERADOR: Solo tienes el número {numeros[0]['valor']}. Falta: agregar un operador (+, -, *, /) y otro número. Ejemplo: {numeros[0]['valor']} + 2.0"
        else:
            return False, "FALTAN OPERADORES: Tienes números pero sin operadores entre ellos. Falta: agregar operadores (+, -, *, /) entre los números."
    
    # Análisis específico por posición
    for i, token in enumerate(tokens):
        
        # PRIMER TOKEN
        if i == 0:
            if token['tipo'] == 'OP':
                return False, f"INICIO INCORRECTO: No puedes empezar con el operador '{token['valor']}'. Falta: poner un número decimal al inicio. Ejemplo: 2.5 {token['valor']} 3.0"
            elif token['tipo'] == 'RPAREN':
                return False, "PARÉNTESIS MAL UBICADO: No puedes empezar con ')'. Falta: poner '(' al inicio o quitar este ')'. Ejemplo: (2.5 + 3.0)"
        
        # ÚLTIMO TOKEN  
        if i == len(tokens) - 1:
            if token['tipo'] == 'OP':
                return False, f"EXPRESIÓN INCOMPLETA: La expresión termina con '{token['valor']}'. Falta: agregar un número decimal después del operador. Ejemplo: actual + 3.0"
            elif token['tipo'] == 'LPAREN':
                return False, "PARÉNTESIS SIN CERRAR: La expresión termina con '(' abierto. Falta: agregar contenido y cerrar con ')'. Ejemplo: (2.5 + 3.0)"
        
        # TOKENS CONSECUTIVOS
        if i < len(tokens) - 1:
            actual = tokens[i]
            siguiente = tokens[i + 1]
            
            # Dos operadores seguidos
            if actual['tipo'] == 'OP' and siguiente['tipo'] == 'OP':
                return False, f"OPERADORES CONSECUTIVOS: Tienes '{actual['valor']}' seguido de '{siguiente['valor']}'. Falta: poner un número decimal entre ellos. Ejemplo: 2.5 {actual['valor']} 3.0 {siguiente['valor']} 4.0"
            
            # Dos números seguidos
            if actual['tipo'] == 'NUM' and siguiente['tipo'] == 'NUM':
                return False, f"NÚMEROS SIN OPERADOR: Tienes '{actual['valor']}' seguido de '{siguiente['valor']}'. Falta: poner un operador (+, -, *, /) entre ellos. Ejemplo: {actual['valor']} + {siguiente['valor']}"
            
            # Número seguido de paréntesis abierto
            if actual['tipo'] == 'NUM' and siguiente['tipo'] == 'LPAREN':
                return False, f"FALTA OPERADOR: Entre '{actual['valor']}' y '(' falta un operador. Agrega: +, -, *, / antes del paréntesis. Ejemplo: {actual['valor']} + (2.0 * 3.0)"
            
            # Paréntesis cerrado seguido de número
            if actual['tipo'] == 'RPAREN' and siguiente['tipo'] == 'NUM':
                return False, f"FALTA OPERADOR: Entre ')' y '{siguiente['valor']}' falta un operador. Agrega: +, -, *, / después del paréntesis. Ejemplo: (2.0 + 3.0) * {siguiente['valor']}"
            
            # Operador seguido de paréntesis cerrado
            if actual['tipo'] == 'OP' and siguiente['tipo'] == 'RPAREN':
                return False, f"OPERADOR VACÍO: El operador '{actual['valor']}' no tiene número después. Falta: agregar un número antes del ')'. Ejemplo: 2.5 {actual['valor']} 3.0)"
            
            # Paréntesis abierto seguido de operador
            if actual['tipo'] == 'LPAREN' and siguiente['tipo'] == 'OP':
                return False, f"PARÉNTESIS VACÍO: Después de '(' tienes '{siguiente['valor']}'. Falta: poner un número decimal después del '('. Ejemplo: ({siguiente['valor']}2.5 + 3.0) → (2.5 {siguiente['valor']} 3.0)"
    
    # Verificar paréntesis balanceados
    balance_paren = 0
    paren_abiertos = 0
    for i, token in enumerate(tokens):
        if token['tipo'] == 'LPAREN':
            balance_paren += 1
            paren_abiertos += 1
        elif token['tipo'] == 'RPAREN':
            balance_paren -= 1
            if balance_paren < 0:
                # Encontrar qué ')' sobra
                pos = i + 1
                return False, f"PARÉNTESIS EXTRA: El ')' en la posición {pos} no tiene '(' correspondiente. Falta: agregar '(' al inicio o quitar este ')'"
    
    if balance_paren > 0:
        return False, f"PARÉNTESIS SIN CERRAR: Tienes {balance_paren} paréntesis '(' sin cerrar. Falta: agregar {balance_paren} paréntesis ')' al final de la expresión."
    
    return True, ""

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('frontend', filename)

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.get_json()
    expr = data.get('expresion', '') 
    expr = re.sub(r'\s+', '', expr)  
    
    if not expr:
        return jsonify({'error': 'ERROR: No se ha ingresado ninguna expresión. Por favor, escribe una ecuación aritmética válida usando números decimales, operadores (+, -, *, /) y paréntesis si es necesario. Ejemplo: 2.5 + 3 * (4 - 1)'})
    
    tokens = analizar_lexico(expr)
    
    # Validar que sea una ecuación aritmética
    es_valida, mensaje_error = es_ecuacion_aritmetica(tokens)
    if not es_valida:
        return jsonify({'error': mensaje_error})
    
    return jsonify({'tokens': tokens})

if __name__ == '__main__':
    app.run(debug=True)