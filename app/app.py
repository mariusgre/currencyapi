from flask import Flask, render_template
from quote import quote_app

def create_app():
    app = Flask(__name__)
    app.register_blueprint(quote_app)
    return app

app = create_app()

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
