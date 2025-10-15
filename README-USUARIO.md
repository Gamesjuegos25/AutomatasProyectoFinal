# Manual de Usuario - Analizador Léxico de Ecuaciones Aritméticas

## ¿Qué es esta aplicación?

El **Analizador Léxico de Ecuaciones Aritméticas** es una herramienta web que analiza expresiones matemáticas y las descompone en **tokens** (elementos básicos como números, operadores y paréntesis). 

Es perfecta para estudiantes de informática, programación o matemáticas que quieren entender cómo funcionan los analizadores léxicos.

---

## Cómo usar la aplicación

### 1. **Acceder a la aplicación**
   - Abre tu navegador web
   - Ve a: `http://localhost:5000`
   - Listo! Ya puedes usar el analizador

### 2. **Formas de introducir ecuaciones**

#### **Opción A: Escribir manualmente**
1. Haz click en el área de texto grande
2. Escribe tu ecuación (ej: `2.5 + 3.0`)
3. Presiona el botón **"Analizar"**

#### **Opción B: Usar ejemplos (Recomendado!)**
1. Busca las secciones de ejemplos
2. **Haz un solo click** en cualquier ejemplo
3. Se analiza automáticamente!

---

## Reglas para escribir ecuaciones válidas

### **Formato requerido:**
- **Solo números decimales:** `2.0`, `5.5`, `10.0` (Válido)
- **NO números enteros:** `2`, `5`, `10` (Inválido)
- **Operadores permitidos:** `+`, `-`, `*`, `/`
- **Paréntesis opcionales:** `(` y `)`

### **Ejemplos correctos:**
```
2.5 + 3.0
10.0 - 4.2
(5.5 * 2.0) / 3.0
((2.0 + 3.0) * 4.0) - 1.0
```

### **Ejemplos incorrectos:**
```
2 + 3      (faltan decimales: 2.0 + 3.0)
5.0 +      (falta número después del +)
+ 3.0      (no puede empezar con operador)
abc + 2.0  (no se permiten letras)
```

---

## Guía paso a paso

### **Paso 1: Probar ejemplos válidos** 
1. Ve a la sección **"Ejemplos válidos"**
2. Haz click en `2.5 + 3.7`
3. **Observa la tabla de tokens!**
4. Verás algo como:
   ```
   Token | Tipo
   ------|-------
   2.5   | NUM
   +     | OP  
   3.7   | NUM
   ```

### **Paso 2: Probar ejemplos con errores**
1. Ve a la sección **"Ejemplos de errores"**
2. Haz click en `5.0 +`
3. **Lee el mensaje de error específico!**
4. Verás: *"Falta: agregar un número después del operador"*

### **Paso 3: Crear tus propias ecuaciones**
1. Escribe en el área de texto: `(15.0 / 3.0) + 2.5`
2. Presiona **"Analizar"**
3. Experimenta con diferentes combinaciones!

---

## Entendiendo los resultados

### **Tabla de Tokens** 
Cuando analizas una ecuación válida, obtienes una tabla con:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| **Token** | El elemento encontrado | `2.5`, `+`, `(` |
| **Tipo** | Categoría del elemento | `NUM`, `OP`, `LPAREN` |

### **Tipos de Tokens:**
- **NUM:** Números decimales (`2.5`, `10.0`)
- **OP:** Operadores (`+`, `-`, `*`, `/`)
- **LPAREN:** Paréntesis abierto `(`
- **RPAREN:** Paréntesis cerrado `)`

---

## Solución de problemas comunes

### **"No pasa nada al hacer click"**
**Solución:** 
- Verifica que el servidor esté funcionando
- Ve a la terminal y ejecuta: `python app.py`
- Debe decir: `Running on http://127.0.0.1:5000`

### **"Sale error de conexión"**
**Solución:**
1. Cierra la aplicación web
2. En la terminal, presiona `Ctrl+C` para parar el servidor
3. Ejecuta nuevamente: `python app.py`
4. Recarga la página web

### **"Mi ecuación no funciona"**
**Solución:**
- Revisa que todos los números sean decimales (con .0)
- Verifica que no falten operadores entre números
- Asegúrate de que los paréntesis estén balanceados

---

## Consejos y trucos

### **Para aprender mejor:**
1. **Empieza con ejemplos simples:** `2.0 + 3.0`
2. **Progresa gradualmente:** `(2.0 + 3.0) * 4.0`
3. **Experimenta con errores:** Aprende de los mensajes específicos

### **Para usuarios avanzados:**
- Prueba expresiones complejas: `((6.0 * 2.0) + 3.0) / (4.0 + 1.0)`
- Combina todos los operadores: `2.5 + 3.0 * 4.0 - 1.0 / 2.0`
- Usa paréntesis anidados: `(((2.0 + 3.0) * 4.0) - 1.0)`

### **Para estudiantes:**
- **Observa los patrones** en la tokenización
- **Compara** expresiones similares
- **Entiende** por qué cada error ocurre

---

## Divertirse aprendiendo

Esta herramienta está diseñada para ser **educativa y fácil de usar**. No tengas miedo de experimentar: cada error te enseña algo nuevo sobre cómo funcionan los analizadores léxicos.

**¿Preguntas?** Los mensajes de error te guían paso a paso para arreglar cualquier problema.

---

*🔬 Desarrollado como proyecto educativo para entender el análisis léxico en la teoría de autómatas y lenguajes formales.*