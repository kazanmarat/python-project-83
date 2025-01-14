"""
Module for a Flask web application that interacts with a PostgreSQL database.

Imports:
- Flask: Web framework for creating the application.
- os: Operating system module for interacting with the operating system.
- Database: Custom class for interacting
    with a PostgreSQL database using psycopg2.
- url_handler: Module for handling URLs.
- requests: HTTP library for making requests.

Environment Setup:
- Loads environment variables from a .env file using dotenv.

Global Variables:
- app: Flask application instance.
- app.config['SECRET_KEY']: Secret key for the Flask application.
- DATABASE_URL: URL for connecting to the PostgreSQL database.
- DB: Instance of the Database class initialized with the DATABASE_URL.

Routes and Functions:
- index_get(): GET route for the homepage to render the index.html template.
- index_post(): POST route for processing form submission on the homepage.
- urls(): Route to display all URLs in the database.
- url(id): Route to display information about a specific URL.
- check_url(id): Route to check the content of a URL
    and save the results in the database.
"""
from flask import (Flask,
                   render_template,
                   request,
                   flash,
                   redirect,
                   url_for,
                   )
import os
from page_analyzer.db import Database
import page_analyzer.url_handler as url_handler
import requests
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
DB = Database(DATABASE_URL)


@app.route('/')
def index_get():
    return render_template(
        'index.html',
    )


@app.post('/')
def index_post():
    address = request.form.get('url', '')
    clean_url = url_handler.clear_url(address)
    try:
        url_handler.check_url(clean_url)
    except (url_handler.URLTooLong, url_handler.URLNotValid):
        flash('Некорректный URL', 'danger')
        return render_template(
            'index.html',
            search=address)

    id_url = DB.find_url_name(clean_url)
    if id_url:
        flash('Страница уже существует', 'success')
    else:
        id_url = DB.save_url(clean_url)
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url', id=id_url), code=302)


@app.route('/urls/')
def urls():
    addresses = DB.get_content()
    return render_template(
        'urls.html',
        addresses=addresses
    )


@app.route('/urls/<int:id>')
def url(id):
    address = DB.exist_url_id(id)
    if not address:
        return render_template('not_found.html'), 404
    urls_check = DB.get_content_check(id)
    return render_template(
        'url.html',
        address=address,
        urls_check=urls_check
    )


@app.post('/urls/<int:id>/check')
def check_url(id):
    url_name = DB.exist_url_id(id)['name']
    try:
        content = url_handler.get_content(url_name)
        content['url_id'] = id
        DB.save_url_check(content)
        flash('Страница успешно проверена', 'success')
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.ReadTimeout,):
        flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('url', id=id))
