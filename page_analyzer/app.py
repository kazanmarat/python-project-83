from flask import Flask
import os


try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def hello_world():
    return 'Welcome to Flask!'
