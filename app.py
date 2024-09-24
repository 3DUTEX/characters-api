from flask import Flask, jsonify
from dotenv import load_dotenv

from src.routes import characters_route

load_dotenv()

# init flask
app = Flask(__name__)

# routes
app.register_blueprint(characters_route.characters_route, url_prefix='/characters')

# Middleware for catch exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Ocorreu um erro: {e}")

    return jsonify({
        "error": "Internal Server Error",
        "message": str(e)
    }), 500

if (__name__ == '__main__'):
    app.run()