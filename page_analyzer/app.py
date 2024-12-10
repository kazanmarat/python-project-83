from flask import Flask, request, render_template, url_for
import os


try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    address = request.args.get('address')
    return render_template(
        'index.html'
    )


@app.route('/urls')
def urls():
    return render_template(
        'urls.html'
    )
