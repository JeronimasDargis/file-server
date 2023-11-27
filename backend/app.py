from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import mysql.connector
from urllib.parse import urlparse, parse_qs
import json
from datetime import datetime
from dotenv import load_dotenv

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


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL to get the path and query parameters
        url_parts = urlparse(self.path)
        path = url_parts.path
        query_params = parse_qs(url_parts.query)

        # Connect to the database
        connection = mysql.connector.connect(**db_config)

        try:
            # Create a cursor object
            cursor = connection.cursor(dictionary=True)

            # Handle different paths
            if path == '/files':
                # Example: Execute a SELECT query
                cursor.execute("SELECT * FROM files")

                # Fetch all rows
                rows = cursor.fetchall()

                 # Use the custom JSON encoder
                json_response = json.dumps({'files': rows}, cls=CustomJSONEncoder)

                # Send a JSON response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json_response.encode())

            else:
                # Send a 404 response for unknown paths
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Not Found')

        finally:
            # Close the cursor and connection
            cursor.close()
            connection.close()

# Run the HTTP server
def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print('Starting server on port 8000...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()