from flask import Flask
import psycopg2

app = Flask(__name__)

def connect_db():
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="user",
        password="password",
        host="db",
        port="5432"
    )
    return conn

@app.route('/')
def hello():
    try:
        conn = connect_db()
        return "Connexion à la base de données réussie !"
    except Exception as e:
        return f"Erreur de connexion : {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
