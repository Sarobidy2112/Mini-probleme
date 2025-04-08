import os
from flask import Flask, jsonify, request
import requests
import psycopg2

app = Flask(__name__)

# Variables d'environnement
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mydb")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenue sur l'API Backend!"})

@app.route('/api/data', methods=['GET'])
def get_data():
    response = requests.get('http://data-service:5001/process')
    return jsonify(response.json())

@app.route('/api/db-test', methods=['GET'])
def db_test():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_table;")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"data": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
