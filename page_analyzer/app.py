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


try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
DB = Database(DATABASE_URL)


@app.route('/')
def index_get():
    address = request.form.get('url', '')
    return render_template(
        'index.html',
        address=address,
    )


@app.post('/')
def index_post():
    address = request.form.get('url', '')
    clean_url = url_handler.clear_url(address)
    try:
        url_handler.check_url(clean_url)
    except (url_handler.URLTooLong, url_handler.URLNotValid):
        flash('Некорректный URL', 'danger')
        return redirect(url_for('index_get'), 302)

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
    address = DB.find_url_id(id)
    if not address:
        return 'Page not found', 404
    return render_template(
        'url.html',
        address=address
    )
