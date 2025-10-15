from flask import Flask, request, jsonify, send_from_directory
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


TOKEN_REGEX = [
    (r'\d+\.\d+', 'NUM'), 
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
    Valida que la expresión sea una ecuación aritmética válida.
    Debe contener al menos un operador aritmético y tener sintaxis correcta.
    """
    if not tokens:
        return False, "La expresión está vacía"
    
    # Verificar que no hay errores de tokens
    errores = [token for token in tokens if token['tipo'] == 'ERROR']
    if len(errores) > 0:
        return False, f"Carácter inválido: {errores[0]['valor']}"
    
    # Verificar que hay al menos un operador
    operadores = [token for token in tokens if token['tipo'] == 'OP']
    if len(operadores) == 0:
        return False, "La expresión debe contener al menos un operador aritmético (+, -, *, /)"
    
    # Validaciones sintácticas básicas
    
    # 1. No puede terminar con operador
    if tokens[-1]['tipo'] == 'OP':
        return False, "La expresión no puede terminar con un operador"
    
    # 2. No puede empezar con operador (excepto + o - unario, pero por simplicidad no los permitimos)
    if tokens[0]['tipo'] == 'OP':
        return False, "La expresión no puede empezar con un operador"
    
    # 3. Verificar paréntesis balanceados
    balance_paren = 0
    for token in tokens:
        if token['tipo'] == 'LPAREN':
            balance_paren += 1
        elif token['tipo'] == 'RPAREN':
            balance_paren -= 1
            if balance_paren < 0:
                return False, "Paréntesis desbalanceados"
    
    if balance_paren != 0:
        return False, "Paréntesis desbalanceados"
    
    # 4. Verificar que no haya operadores consecutivos
    for i in range(len(tokens) - 1):
        if tokens[i]['tipo'] == 'OP' and tokens[i + 1]['tipo'] == 'OP':
            return False, "No se permiten operadores consecutivos"
    
    # 5. Verificar que después de cada operador haya un operando o paréntesis abierto
    for i in range(len(tokens) - 1):
        if tokens[i]['tipo'] == 'OP':
            if tokens[i + 1]['tipo'] not in ['NUM', 'LPAREN']:
                return False, "Después de un operador debe haber un número o paréntesis abierto"
    
    # 6. Verificar que antes de cada operador haya un operando o paréntesis cerrado
    for i in range(1, len(tokens)):
        if tokens[i]['tipo'] == 'OP':
            if tokens[i - 1]['tipo'] not in ['NUM', 'RPAREN']:
                return False, "Antes de un operador debe haber un número o paréntesis cerrado"
    
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
        return jsonify({'error': 'Por favor, ingresa una expresión válida.'})
    
    tokens = analizar_lexico(expr)
    
    # Validar que sea una ecuación aritmética
    es_valida, mensaje_error = es_ecuacion_aritmetica(tokens)
    if not es_valida:
        return jsonify({'error': mensaje_error})
    
    return jsonify({'tokens': tokens})

if __name__ == '__main__':
    app.run(debug=True)