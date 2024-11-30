from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from routes.api import api_blueprint
from routes.prosthetic_routes import prosthetic_blueprint
import os

# Set static_folder to the React build folder
# Correct static folder path
# Get the absolute path of the React build folder
build_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../AI_Enabled_Prosthetic_Design/frontend/build"))

# Set static_folder to the absolute path
app = Flask(__name__, static_folder=build_path, static_url_path="")

CORS(app)  # Allow CORS for development

# Register API blueprints
app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(prosthetic_blueprint, url_prefix='/prosthetic')

# Serve React app
@app.route("/")
def serve_react_app():
    index_path = os.path.join(app.static_folder, "index.html")
    print(f"Looking for React build file at: {index_path}")
    if not os.path.exists(index_path):
        return jsonify({"error": "React build files not found. Please build the frontend."}), 500
    return send_from_directory(app.static_folder, "index.html")

@app.errorhandler(404)
def not_found(e):
    # Serve React's index.html for unknown routes
    index_path = os.path.join(app.static_folder, "index.html")
    if not os.path.exists(index_path):
        return jsonify({"error": "React build files not found. Please build the frontend."}), 500
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)
