from flask import Flask, request, jsonify
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


TOKEN_REGEX = [
    (r'\d+(\.\d+)?', 'NUM'),
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

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.get_json()
    expr = data.get('expresion', '')
    expr = expr.replace(' ', '')  
    tokens = analizar_lexico(expr)
    return jsonify({'tokens': tokens})

if __name__ == '__main__':
    app.run(debug=True)
