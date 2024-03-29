import os

from flask import Flask, render_template

from dotenv import load_dotenv

load_dotenv()

from libs.mailgun import Mailgun
from views.alerts import alert_blueprint
from views.stores import store_blueprint
from views.users import user_blueprint
from views.games import game_blueprint
import models.games.game as game


app = Flask(__name__)
app.secret_key = 'rashed'
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)


@app.route('/')
def home():
    return render_template('home.html')

app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix="/users")

app.register_blueprint(game_blueprint, url_prefix="/games")

if __name__ == "__main__":
    game.Game.init_database()
    app.run(debug=True)
