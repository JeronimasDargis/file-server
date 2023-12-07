#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file, make_response
from flask_cors import CORS

import os
import mysql.connector
import json
import re

app = Flask(__name__)
CORS(app)

load_dotenv()


db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}


# Print database configuration to Apache error log
app.logger.error(f"DB_HOST: {os.getenv('DB_HOST')}")
app.logger.error(f"DB_USER: {os.getenv('DB_USER')}")
app.logger.error(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
app.logger.error(f"DB_NAME: {os.getenv('DB_NAME')}")

UPLOAD_FOLDER = os.getenv('UPLOAD_PATH') 

# @todo Review actual extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


# @todo extend to config init script
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    # return jsonify({'files': [{'name': "test"}]})
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
    filename = file.filename

    if filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # @todo create a function for name validation
   

    # Save the file to a storage location
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Store file metadata in the database
    store_file_metadata(filename, file_path)

    return jsonify({'message': 'File uploaded successfully'})


@app.route('/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    # @todo path is already stored in the metadata so no need to query the db again..

    try:
        cursor.execute("SELECT * FROM files WHERE id = %s", (file_id,))
        row = cursor.fetchone()
        file_path = row['file_path']
        filename = row['filename']
    finally:
        cursor.close()
        connection.close()

    if file_path == '':
        return jsonify({'error': 'Error finding file in the database'}), 400

    try:
        response = send_file(file_path, as_attachment=True)
        return response
    except FileNotFoundError:
        return jsonify({'error': 'Error finding file on the server'}), 500
   


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
    app.run()

