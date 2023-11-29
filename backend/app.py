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

def store_file_metadata(filename, file_path):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("INSERT INTO files (filename, file_path) VALUES (%s, %s)", (filename, file_path))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

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


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file to a storage location
    # file_path = f'/path/to/storage/{file.filename}'
    # file.save(file_path)

    # Store file metadata in the database
    store_file_metadata(file.filename, 'test/path')

    return jsonify({'message': 'File uploaded successfully'})


@app.route('/delete/<int:file_id>', methods=['POST'])
def delete_file(file_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("DELETE FROM files WHERE id = %s", (file_id,))
        connection.commit()
        return jsonify({'message': 'File deleted successfully'}), 200
    except Exception as e:
        # Log the error
        print(f"Error deleting file with id {file_id}: {e}")
        return jsonify({'error': 'Failed to delete file'}), 500
    finally:
        cursor.close()
        connection.close()

# Run the HTTP server
if __name__ == '__main__':
    app.run(debug=True)