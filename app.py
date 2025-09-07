from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Pega a URL do banco no Render (configure no painel -> Environment Variables)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.route("/inserir", methods=["POST"])
def inserir():
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (nome, email))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Usuário inserido com sucesso!"})

@app.route("/listar", methods=["GET"])
def listar():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, email FROM usuarios")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    usuarios = [{"id": r[0], "nome": r[1], "email": r[2]} for r in rows]
    return jsonify(usuarios)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
