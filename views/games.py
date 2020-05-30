from flask import Blueprint, request, session, url_for, render_template, redirect
from models.games.game import Game

game_blueprint = Blueprint('games', __name__)

@game_blueprint.route('/')
def index():
    games = Game.random(3)
    return render_template('games/index.html', games=games)
