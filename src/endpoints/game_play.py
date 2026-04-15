from flask import Blueprint, request

__author__ = 'smok'

from model.game import Game
from model.game_bucket import GameBucket

games_api_blueprint = Blueprint('api/game', __name__)

games = GameBucket()
# app.cache.set('games', games)

@games_api_blueprint.route('/all', methods=['GET'])
def get_all_games():
    return games.json()

@games_api_blueprint.route('/<string:game_id>', methods=['GET'])
def get_game(game_id):
    if game_id not in games.games:
        return {"info": "Game not found"}

    return games.json_single(game_id)

@games_api_blueprint.route('/new', methods=['POST'])
def new_game():
    players = int(request.form['players'])
    if players is not None:
        game = Game()
        if type(players) is int and int(players) > 1:
            for i in range(1, players + 1):
                game.add_hand("New Player " + str(i))
        elif type(players) is list and len(players) > 1:
            names = request.form['players'].split()
            for name in names:
                game.add_hand(name)

        game.serve_all_hands()
        game_id = games.add_game(game)
        return games.json(game_id)

    return {"info": "Neither player names nor number of them specified, game is on hold until more players join"}

@games_api_blueprint.route('/<string:game_id>/add-player/<string:player_name>', methods=['POST'])
def add_player(game_id, player_name):
    if game_id is not None and game_id in games.games:
        game = games.games[game_id]
        game.add_hand(player_name if player_name is not None else "New Player " + str(len(game.hands) + 1))
        return games.json(game_id)

    return {"info": "Game not found"}

@games_api_blueprint.route('/<string:game_id>/replace-cards', methods=['POST'])
def replace_cards(game_id):
    game = games.get_game(game_id)
    if game is None:
        return {"info": "Game not found"}

    hand_name = request.form['hand-name']
    if hand_name in game.hands:
        hand = game.hands[hand_name]
        if hand is not None:
            card_indexes = request.form['card-indexes']
            input_list = [int(a) for a in card_indexes.split()]
            input_list[:] = [i - 1 for i in input_list]
            game.replace_cards(hand_name, input_list)
            return hand.json()

    return {"info": f"No such player {hand_name} in the game"}

@games_api_blueprint.route('/<string:game_id>/hand/<string:hand_name>/show', methods=['GET'])
def show_hand(game_id, hand_name):
    game = games.get_game(game_id)
    hand = game.hands[hand_name]
    return hand.json()

@games_api_blueprint.route('/<string:game_id>/reveal', methods=['GET'])
def show_hands(game_id):
    if game_id is not None and game_id in games.games:
        game = games.get_game(game_id)
        return game.json()

    return {"info": "Game not found"}

@games_api_blueprint.route('/<string:game_id>/resolve', methods=['POST'])
def resolve(game_id):
    if game_id is not None and game_id in games.games:
        game = games.get_game(game_id)
        game.resolve()
        return {"winner": game.winner[0], "hand": game.winner[1]+':'+str(game.winner[2])}

    return {"info": "Game not found"}