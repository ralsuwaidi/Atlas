from flask import Blueprint, request, session, url_for, render_template, redirect, flash
from models.games.game import Game
from models.transmission import Transmission
import common.utils as utils
import subprocess

game_blueprint = Blueprint('games', __name__)


@game_blueprint.route('/random', methods=['POST', 'GET'])
def random():
    if request.method == 'POST':
        subprocess.call(request.form['exe_loc'])
    games = Game.random(6)

    return render_template('games/index.html', games=games, downloaded_games=utils.Utils.get_downloaded_games())


@game_blueprint.route('/<int:page>', methods=['POST', 'GET'])
@game_blueprint.route('/', methods=['POST', 'GET'])
def index(page=1):
    if request.method == 'POST':
        try:
            games = Game.search(request.form['search'])
            return render_template('games/index.html', games=games)
        except:
            pass
        try:
            subprocess.call(request.form['exe_loc'])
        except:
            pass
    all_games = Game.all()
    all_games.sort(key=lambda x: x.entry_date, reverse=True)
    games = all_games[page*6-6:page*6]
    total_pages = len(all_games)//6
    if len(all_games)%6!=0:
        total_pages+=1
    return render_template('games/index.html', games=games, page=page, total_pages=total_pages, downloaded_games=utils.Utils.get_downloaded_games())


@game_blueprint.route('/info/<string:game_id>', methods=['POST', 'GET'])
def info(game_id):
    if request.method == 'POST':
        subprocess.call(request.form['exe_loc'])
    # Transmission.download_from_id(magnet_link)
    game = Game.get_by_id(game_id)
    return render_template('games/info.html', game=game, downloaded_games=utils.Utils.get_downloaded_games())


@game_blueprint.route('/download/<string:game_id>')
def download(game_id):
    Transmission.download_from_id(game_id)
    flash(f'{Game.find_one_by("_id",game_id).title} has successfully started downloading', 'success')
    # game = Game.get_by_id(game_id)
    # return render_template('games/download.html', game=game)
    return redirect(url_for('.index'))

