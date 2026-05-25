import flask # type: ignore

app = flask.Flask(__name__)

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = flask.request.json
    a = dados['a']
    b = dados['b']
    operacao = dados['operacao']

    if operacao == 'soma':
        resultado = a + b
    elif operacao == 'subtracao':
        resultado = a - b
    elif operacao == 'multiplicacao':
        resultado = a * b
    elif operacao == 'divisao':
        if b == 0:
            return flask.jsonify({'erro': 'Não dá dividir por zero!'})
        resultado = a / b
    else:
        return flask.jsonify({'erro': 'Operação inválida'})

    return flask.jsonify({'resultado': resultado})

app.run(debug=True)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# configura o banco de dados (cria um arquivo calculadora.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calculadora.db'
db = SQLAlchemy(app)

# define a tabela de histórico
class Historico(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    numero_a  = db.Column(db.Float)
    numero_b  = db.Column(db.Float)
    operacao  = db.Column(db.String(20))
    resultado = db.Column(db.Float)
    data      = db.Column(db.DateTime, default=datetime.utcnow)

# cria a tabela se não existir
with app.app_context():
    db.create_all()

# rota para calcular e salvar
@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.json
    a = dados['a']
    b = dados['b']
    operacao = dados['operacao']

    if operacao == 'soma':
        resultado = a + b
    elif operacao == 'subtracao':
        resultado = a - b
    elif operacao == 'multiplicacao':
        resultado = a * b
    elif operacao == 'divisao':
        if b == 0:
            return jsonify({'erro': 'Não dá dividir por zero!'})
        resultado = a / b
    else:
        return jsonify({'erro': 'Operação inválida'})

    # salva no banco de dados
    registro = Historico(numero_a=a, numero_b=b, operacao=operacao, resultado=resultado)
    db.session.add(registro)
    db.session.commit()

    return jsonify({'resultado': resultado})


# rota para ver o histórico
@app.route('/historico', methods=['GET'])
def historico():
    registros = Historico.query.order_by(Historico.data.desc()).all()
    lista = []
    for r in registros:
        lista.append({
            'id':        r.id,
            'a':         r.numero_a,
            'b':         r.numero_b,
            'operacao':  r.operacao,
            'resultado': r.resultado,
            'data':      r.data.strftime('%d/%m/%Y %H:%M:%S')
        })
    return jsonify(lista)

<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">

import os
app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

const URL_SERVER = 'https://github.com/Dchit-bit/calculadora.py.git';



Crie uma animação CSS com @keyframes e aplique nos botões:
css@keyframes rgbBotao {
  0%   { border-color: red;    box-shadow: 0 0 6px red; }
  33%  { border-color: lime;   box-shadow: 0 0 6px lime; }
  66%  { border-color: cyan;   box-shadow: 0 0 6px cyan; }
  100% { border-color: red;    box-shadow: 0 0 6px red; }
button {}
  animation: rgbBotao 3s linear infinite;
    border : 2px solid black;
cssbutton:nth-child(1) { animation-delay: 0s; }
button:nth-child(2) { animation-delay: -0.3s; }
button:nth-child(3) { animation-delay: -0.6s; }
/* e assim por diante... */

@keyframes rgbBorda {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.moldura {
  padding: 3px; /* essa espessura vira a "borda" */
  border-radius: 16px;
  background: linear-gradient(45deg, red, yellow, lime, cyan, blue, magenta, red);
  background-size: 400% 400%;
  animation: rgbBorda 3s linear infinite;

  