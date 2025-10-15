# Manual Técnico - Analizador Léxico de Ecuaciones Aritméticas

## Información General

### **Proyecto:** Analizador Léxico Web
### **Tecnologías:** Python (Flask), JavaScript, HTML5, CSS3
### **Propósito:** Demostración educativa de análisis léxico y validación sintáctica

---

## Arquitectura del Sistema

### **Patrón de Diseño:** Cliente-Servidor
- **Frontend:** Interfaz web (HTML/CSS/JS)
- **Backend:** API REST con Flask (Python)
- **Comunicación:** HTTP/JSON

```
┌─────────────┐    HTTP/JSON    ┌─────────────┐
│   Frontend  │ ──────────────> │   Backend   │
│ (Navegador) │ <────────────── │   (Flask)   │
└─────────────┘                 └─────────────┘
```

---

## Estructura de Archivos

```
AutomatasProyectoFinal/
├── app.py                 # Servidor Flask principal
├── requirements.txt       # Dependencias Python
├── README-USUARIO.md     # Manual de usuario
├── README-TECNICO.md     # Manual técnico (este archivo)
└── frontend/
    ├── index.html        # Interfaz de usuario
    ├── script.js         # Lógica del frontend
    └── style.css         # Estilos y diseño
```

---

## Backend (Python/Flask)

### **Archivo: `app.py`**

#### **1. Importaciones y Configuración**
```python
from flask import Flask, request, jsonify, send_from_directory
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite peticiones desde el frontend
```

#### **2. Definición de Tokens (Expresiones Regulares)**
```python
TOKEN_REGEX = [
    (r'\d+\.\d+', 'NUM'),     # Números decimales válidos (ej: 2.5, 10.0)
    (r'\d+', 'NUM_INT'),      # Números enteros para detectar errores
    (r'[a-zA-Z]+', 'LETTER'), # Letras para detectar errores
    (r'[+\-*/]', 'OP'),       # Operadores aritméticos
    (r'\(', 'LPAREN'),        # Paréntesis abierto
    (r'\)', 'RPAREN'),        # Paréntesis cerrado
]
```

**Explicación:**
- Usa **regex** para identificar patrones
- **Orden importante:** decimales antes que enteros
- **Tipos de error:** `NUM_INT`, `LETTER` para validación específica

#### **3. Analizador Léxico**
```python
def analizar_lexico(expr):
    tokens = []
    pos = 0
    while pos < len(expr):
        if expr[pos].isspace():  # Ignorar espacios
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
        
        if not match:  # Carácter no reconocido
            tokens.append({'tipo': 'ERROR', 'valor': expr[pos]})
            pos += 1
    
    return tokens
```

**Funcionamiento:**
1. **Recorre** carácter por carácter
2. **Aplica regex** en orden de prioridad
3. **Genera tokens** con tipo y valor
4. **Maneja errores** para caracteres no válidos

#### **4. Validador Sintáctico**
```python
def es_ecuacion_aritmetica(tokens):
    # Validación por categorías de error:
    
    # 1. Expresión vacía
    if not tokens:
        return False, "EXPRESIÓN VACÍA: Falta toda la expresión..."
    
    # 2. Tokens de error específicos
    for token in tokens:
        if token['tipo'] == 'NUM_INT':
            return False, f"FORMATO INCORRECTO: '{token['valor']}' debe ser decimal..."
        elif token['tipo'] == 'LETTER':
            return False, f"CARÁCTER INVÁLIDO: Las letras '{token['valor']}'..."
    
    # 3. Validación posicional
    for i, token in enumerate(tokens):
        # Validar primer y último token
        # Validar tokens consecutivos
        # Validar contexto específico
    
    # 4. Validación de paréntesis balanceados
    balance_paren = 0
    for token in tokens:
        if token['tipo'] == 'LPAREN': balance_paren += 1
        elif token['tipo'] == 'RPAREN': balance_paren -= 1
    
    return True, ""
```

**Estrategias de Validación:**
- **Mensajes específicos:** Cada error explica qué falta
- **Validación posicional:** Verifica contexto de cada token
- **Detección temprana:** Para errores de formato
- **Análisis estructural:** Para paréntesis y operadores

#### **5. Endpoints API**

```python
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
    expr = re.sub(r'\s+', '', expr)  # Remover espacios extra
    
    if not expr:
        return jsonify({'error': 'ERROR: No se ha ingresado...'})
    
    tokens = analizar_lexico(expr)
    es_valida, mensaje_error = es_ecuacion_aritmetica(tokens)
    
    if not es_valida:
        return jsonify({'error': mensaje_error})
    
    return jsonify({'tokens': tokens})
```

---

## Frontend (HTML/CSS/JavaScript)

### **Archivo: `index.html`**

#### **Estructura HTML:**
```html
<div class="container">
    <h1>Analizador Léxico...</h1>
    
    <!-- Descripción con instrucciones -->
    <div class="description">...</div>
    
    <!-- Ejemplos válidos clickeables -->
    <div class="ejemplos-container">
        <h3>Ejemplos válidos</h3>
        <div class="ejemplos-grid">
            <span class="ejemplo" onclick="setEjemplo('2.5 + 3.0')">...</span>
        </div>
    </div>
    
    <!-- Ejemplos de errores por categorías -->
    <div class="ejemplos-container error-container">
        <h4>Errores de Contenido:</h4>
        <h4>Errores de Posición:</h4>
        <h4>Errores de Paréntesis:</h4>
    </div>
    
    <!-- Interfaz de análisis -->
    <textarea id="inputExpr" placeholder="..."></textarea>
    <div class="botones">
        <button onclick="analizar()">Analizar</button>
        <button onclick="limpiar()">Limpiar</button>
    </div>
    
    <!-- Área de resultados -->
    <div id="ayuda"></div>
    <div id="result"></div>
</div>
```

### **Archivo: `script.js`**

#### **Función Principal de Análisis:**
```javascript
function analizar() {
    const expr = document.getElementById("inputExpr").value.trim();
    document.getElementById("ayuda").innerHTML = "";
    
    fetch('http://localhost:5000/analizar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expresion: expr })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            // Mostrar mensaje de error específico
            document.getElementById("ayuda").textContent = data.error;
            document.getElementById('result').innerHTML = '';
        } else {
            // Generar tabla de tokens
            let html = '<table><tr><th>Token</th><th>Tipo</th></tr>';
            data.tokens.forEach(tok => {
                html += `<tr><td>${tok.valor}</td><td>${tok.tipo}</td></tr>`;
            });
            html += '</table>';
            document.getElementById('result').innerHTML = html;
        }
    })
    .catch(() => {
        document.getElementById("ayuda").textContent = 'Error de conexión.';
    });
}
```

**Características:**
- **Sin validación frontend:** Todo se procesa en Python
- **Async/Await:** Para peticiones HTTP
- **Manejo de errores:** Conexión y respuesta
- **Generación dinámica:** Tabla HTML con tokens

#### **Sistema de Ejemplos Automáticos:**
```javascript
function setEjemplo(expresion) {
    document.getElementById('inputExpr').value = expresion;
    document.getElementById('result').innerHTML = '';
    document.getElementById('ayuda').textContent = '';
    analizar(); // Ejecuta automáticamente
}
```

### **Archivo: `style.css`**

#### **Diseño Moderno con Glass Morphism:**
```css
/* Fondo animado con gradientes */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Inter', sans-serif;
}

/* Contenedor principal con efecto glass */
.container {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* Botones con gradientes y animaciones */
button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    transition: all 0.3s ease;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}
```

**Características del Diseño:**
- **Glass Morphism:** Transparencias y blur effects
- **Animaciones CSS:** Hover effects y transiciones
- **Responsive:** Grid system adaptativo
- **Accesibilidad:** Contrastes y tamaños apropiados

---

## Flujo de Datos

### **1. Interacción del Usuario:**
```
Usuario hace click en ejemplo → setEjemplo() → analizar()
                                               ↓
Usuario escribe manual → analizar() → fetch('/analizar')
```

### **2. Procesamiento Backend:**
```
Recibir expresión → analizar_lexico() → generar tokens
                                              ↓
                    es_ecuacion_aritmetica() → validar sintaxis
                                              ↓
                    Responder: {tokens} o {error}
```

### **3. Renderizado Frontend:**
```
Recibir respuesta → ¿Es error? → Mostrar mensaje
                               ↓
                    ¿Es válido? → Generar tabla tokens
```

---

## Casos de Prueba

### **Casos Válidos:**
```javascript
// Básicos
"2.5 + 3.0" → [{tipo:'NUM', valor:'2.5'}, {tipo:'OP', valor:'+'}, {tipo:'NUM', valor:'3.0'}]

// Con paréntesis
"(2.0 + 3.0) * 4.0" → 7 tokens correctos

// Complejos
"((6.0 * 2.0) + 3.0) / (4.0 + 1.0)" → 17 tokens correctos
```

### **Casos de Error:**
```javascript
// Formato incorrecto
"5 + 3.0" → "FORMATO INCORRECTO: '5' debe ser decimal..."

// Posición incorrecta  
"+ 3.0" → "INICIO INCORRECTO: No puedes empezar con '+'"

// Paréntesis
"(2.0 + 3.0" → "PARÉNTESIS SIN CERRAR: Falta 1 paréntesis ')'"
```

---

## Instalación y Despliegue

### **Requisitos:**
```
Python 3.7+
Flask 2.0+
flask-cors
```

### **Instalación:**
```bash
# 1. Clonar/descargar proyecto
cd AutomatasProyectoFinal

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar servidor
python app.py

# 4. Abrir navegador
http://localhost:5000
```

### **Configuración de Desarrollo:**
```python
# En app.py, para desarrollo:
if __name__ == '__main__':
    app.run(debug=True)  # Auto-reload en cambios

# Para producción:
app.run(debug=False, host='0.0.0.0', port=5000)
```

---

## Personalización y Extensión

### **Agregar Nuevos Tokens:**
```python
# En TOKEN_REGEX, agregar nueva tupla:
(r'pattern_regex', 'NUEVO_TIPO'),

# En validación, manejar nuevo tipo:
elif token['tipo'] == 'NUEVO_TIPO':
    # Lógica de validación específica
```

### **Nuevos Operadores:**
```python
# Modificar regex de operadores:
(r'[+\-*/%^]', 'OP'),  # Agregado % y ^

# Actualizar validación si es necesario
```

### **Estilos Personalizados:**
```css
/* En style.css, cambiar colores principales: */
:root {
    --primary-gradient: linear-gradient(135deg, #nuevo1, #nuevo2);
    --accent-color: #nuevo-color;
}
```

---

## Métricas y Análisis

### **Complejidad Algorítmica:**
- **Análisis Léxico:** O(n) donde n = longitud de expresión
- **Validación Sintáctica:** O(n) donde n = número de tokens
- **Memoria:** O(n) para almacenar tokens

### **Performance:**
- **Expresiones típicas:** < 1ms de procesamiento
- **Respuesta HTTP:** < 10ms en local
- **Límites prácticos:** ~1000 caracteres por expresión

---

## Debugging y Troubleshooting

### **Errores Comunes:**

#### **1. CORS Error:**
```
Solución: Verificar que CORS(app) esté importado y configurado
```

#### **2. ModuleNotFoundError:**
```bash
pip install flask flask-cors
```

#### **3. Puerto en uso:**
```bash
# Cambiar puerto en app.py:
app.run(port=5001)  # Usar puerto diferente
```

### **Logs de Debug:**
```python
# Agregar logging en app.py:
import logging
logging.basicConfig(level=logging.DEBUG)

# En funciones críticas:
print(f"Tokens generados: {tokens}")
print(f"Validación: {es_valida}, {mensaje_error}")
```

---

## Recursos Adicionales

### **Conceptos Teóricos:**
- **Análisis Léxico:** Conversión de texto a tokens
- **Expresiones Regulares:** Patrones de reconocimiento
- **Autómatas Finitos:** Base teórica del analizador
- **Gramáticas Libres de Contexto:** Para análisis sintáctico

### **Referencias:**
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Regular Expressions Python](https://docs.python.org/3/library/re.html)
- [Compiler Design Principles](https://en.wikipedia.org/wiki/Lexical_analysis)

---

## Objetivos Educativos Cumplidos

### **Conceptos Demostrados:**
**Tokenización** con expresiones regulares  
**Validación sintáctica** por posición y contexto  
**Manejo de errores** específicos y educativos  
**Arquitectura cliente-servidor** con API REST  
**Interfaz interactiva** para experimentación  

### **Habilidades Desarrolladas:**
- Implementación de analizadores léxicos
- Validación y manejo de errores
- Desarrollo web full-stack
- Diseño de interfaces educativas
- Testing y casos de prueba

---

*Este proyecto demuestra los fundamentos del análisis léxico de manera práctica e interactiva, ideal para estudiantes de ciencias de la computación y programadores que quieren entender cómo funcionan los compiladores e intérpretes.*