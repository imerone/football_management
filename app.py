from flask import Flask, redirect, url_for
from dotenv import load_dotenv
from init import init_app

load_dotenv()
app = Flask(__name__)

# Initialize app with extensions and blueprints
init_app(app)

# Root route to redirect to login
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
