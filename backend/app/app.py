from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os

# Import routes
try:
    from routes.api import api_blueprint
    from routes.prosthetic_routes import prosthetic_blueprint
except ImportError as e:
    print(f"Error importing routes: {e}")
    api_blueprint = None
    prosthetic_blueprint = None

# Create Flask app
# Dynamically resolve the React build folder path
build_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../AI_Enabled_Prosthetic_Design/frontend/build")
)
app = Flask(__name__, static_folder=build_path, static_url_path="")

# Enable CORS for development purposes
CORS(app)

# Register blueprints
if api_blueprint:
    app.register_blueprint(api_blueprint, url_prefix='/api')
else:
    print("Warning: API blueprint not loaded.")

if prosthetic_blueprint:
    app.register_blueprint(prosthetic_blueprint, url_prefix='/prosthetic')
else:
    print("Warning: Prosthetic blueprint not loaded.")

# Serve the React app
@app.route("/")
def serve_react_app():
    """Serve the React build index.html."""
    index_path = os.path.join(app.static_folder, "index.html")
    if not os.path.exists(index_path):
        return jsonify({"error": "React build files not found. Please build the frontend."}), 500
    return send_from_directory(app.static_folder, "index.html")

@app.errorhandler(404)
def not_found(e):
    """Handle unknown routes by serving the React app."""
    index_path = os.path.join(app.static_folder, "index.html")
    if not os.path.exists(index_path):
        return jsonify({"error": "React build files not found. Please build the frontend."}), 500
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    print("Starting Flask server...")
    print(f"Serving React app from: {app.static_folder}")
    app.run(debug=True, host="0.0.0.0", port=5000)
