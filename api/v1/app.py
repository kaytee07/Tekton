#!/usr/bin/pyhton3
"""
main flask app
"""
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.register_blueprint(app_views, url_prefix='/api/v1')

session_key = getenv('TK_SESSION_KEY')

app.secret_key = session_key

@app.teardown_appcontext
def close_storage(error):
    """
    close storage when app is torn down
    """
    TK_ENV = getenv('TK_ENV')
    if TK_ENV == 'db':
        storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return {"error": " Not found"}


if __name__ == "__main__":
    host = getenv('TK_API_HOST')
    port = getenv('TK_API_PORT')
    app.run(host=host, port=port, threaded=True)
