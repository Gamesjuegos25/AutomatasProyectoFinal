function analizar() {
    const expr = document.getElementById('inputExpr').value.trim();
    const ayuda = document.getElementById('ayuda');
    if (!expr) {
        document.getElementById('result').innerHTML = '';
        if (ayuda) ayuda.textContent = 'Por favor, ingresa una expresión válida.';
        return;
    } else {
        if (ayuda) ayuda.textContent = '';
    }
    fetch('http://localhost:5000/analizar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ expresion: expr })
    })
    .then(response => response.json())
    .then(data => {
        let html = '<table><tr><th>Token</th><th>Tipo</th></tr>';
        data.tokens.forEach(tok => {
            html += `<tr><td>${tok.valor}</td><td>${tok.tipo}</td></tr>`;
        });
        html += '</table>';
        document.getElementById('result').innerHTML = html;
    })
    .catch(err => {
        document.getElementById('result').innerHTML = 'Error en el análisis.';
    });
}

function limpiar() {
    document.getElementById('inputExpr').value = '';
    document.getElementById('result').innerHTML = '';
    var ayuda = document.getElementById('ayuda');
    if (ayuda) ayuda.textContent = '';
}
