from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "banco.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            mensagem TEXT
        )
    """)
    conn.commit()
    conn.close()
    print(f"Banco de dados criado ou verificado em: {DB_PATH}")

@app.route("/")
def formulario():
    with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.route("/enviar", methods=["POST"])
def enviar():
    nome = request.form["nome"]
    email = request.form["email"]
    mensagem = request.form["mensagem"]

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO contatos (nome, email, mensagem) VALUES (?, ?, ?)", (nome, email, mensagem))
    conn.commit()
    conn.close()
    return f"<h2>Obrigado, {nome}! Sua mensagem foi enviada.</h2>"

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)