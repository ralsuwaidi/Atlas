from flask import Blueprint, request, session, url_for, render_template, redirect
from models.games.game import Game
from models.transmission import Transmission

game_blueprint = Blueprint('games', __name__)

@game_blueprint.route('/')
def index():
    games = Game.random(6)
    return render_template('games/index.html', games=games)


@game_blueprint.route('/info/<string:game_id>')
def info(game_id):
    # Transmission.download_from_id(magnet_link)
    game = Game.get_by_id(game_id)
    return render_template('games/info.html', game=game)

@game_blueprint.route('/download/<string:game_id>')
def download(game_id):
    Transmission.download_from_id(game_id)
    # game = Game.get_by_id(game_id)
    # return render_template('games/download.html', game=game)
    return redirect(url_for('.index'))