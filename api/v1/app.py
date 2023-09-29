#!/usr/bin/pyhton3
"""
main flask app
"""
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask
from flask_mail import Mail
import paystack

session_key = getenv('TK_SESSION_KEY')
paystack_key = getenv('TK_PAYSTACK_KEY')
email_address = getenv('TK_EMAIL_ADDRESS')
email_password = getenv('TK_EMAIL_PASSW')

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = email_address
app.config['MAIL_PASSWORD'] = email_password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

app.register_blueprint(app_views, url_prefix='/api/v1')

app.secret_key = session_key
#paystack_api = paystack.Paystack(secret_key=paystack_key)


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
