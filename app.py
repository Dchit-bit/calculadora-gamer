from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calculadora.db'
db = SQLAlchemy(app)

class Historico(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    numero_a  = db.Column(db.Float)
    numero_b  = db.Column(db.Float)
    operacao  = db.Column(db.String(20))
    resultado = db.Column(db.Float)
    data      = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("calculadora.html")

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

    registro = Historico(numero_a=a, numero_b=b, operacao=operacao, resultado=resultado)
    db.session.add(registro)
    db.session.commit()

    return jsonify({'resultado': resultado})

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
