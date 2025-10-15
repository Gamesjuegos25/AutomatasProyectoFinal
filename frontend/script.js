function analizar() {
    const expr = document.getElementById("inputExpr").value.trim();
    
    // Limpiar ayuda antes del fetch
    document.getElementById("ayuda").innerHTML = "";
    
    fetch('http://localhost:5000/analizar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expresion: expr })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                document.getElementById("ayuda").textContent = data.error;
                document.getElementById('result').innerHTML = '';
            } else {
                let html = '<table><tr><th>Token</th><th>Tipo</th></tr>';
                data.tokens.forEach(tok => {
                    html += `<tr><td>${tok.valor}</td><td>${tok.tipo}</td></tr>`;
                });
                html += '</table>';
                document.getElementById('result').innerHTML = html;
            }
        })
        .catch(() => {
            document.getElementById("ayuda").textContent = 'Error en la conexión con el servidor.';
        });
}

function limpiar() {
    document.getElementById('inputExpr').value = '';
    document.getElementById('result').innerHTML = '';
    document.getElementById('ayuda').textContent = '';
}

function setEjemplo(expresion) {
    // Pegar la expresión en el textarea
    document.getElementById('inputExpr').value = expresion;
    // Limpiar resultados anteriores
    document.getElementById('result').innerHTML = '';
    document.getElementById('ayuda').textContent = '';
    // Analizar automáticamente
    analizar();
}