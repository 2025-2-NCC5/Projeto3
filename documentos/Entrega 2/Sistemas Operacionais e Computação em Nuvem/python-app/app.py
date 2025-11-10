import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

def conexao():
    return mysql.connector.connect(
        host="mysql_db",  
        user="admin",
        password="admin123",
        database="empresa",
        ssl_disabled=True
     )

@app.route("/")
def listar_funcionarios():
    db = conexao()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM funcionarios;")
    resultado = cursor.fetchall()
    db.close()
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)