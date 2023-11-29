from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import mysql.connector
from urllib.parse import urlparse, parse_qs
import json
from datetime import datetime
from dotenv import load_dotenv
import re
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # Custom serialization for datetime objects
        if isinstance(obj, datetime):
            return obj.isoformat()

        # If the object is not a datetime, use the default encoder
        return super().default(obj)


@app.route('/files', methods=['GET'])
def get_all_files():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM files")
        rows = cursor.fetchall()
        return jsonify({'files': rows})
    finally:
        cursor.close()
        connection.close()


@app.route('/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM files WHERE id = %s", (file_id,))
        rows = cursor.fetchall()
        return jsonify({'files': rows})
    finally:
        cursor.close()
        connection.close()


# Run the HTTP server
if __name__ == '__main__':
    app.run(debug=True)