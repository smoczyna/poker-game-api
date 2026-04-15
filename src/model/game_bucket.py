import uuid
from model.game import Game

__author__ = 'smok'

class GameBucket(object):

    def __init__(self):
        self.games = {}

    def pretty_print(self):
        print("*** Game Bucket ***")
        for key in self.games.keys():
            print("Game id: " + key)
            game = self.games[key]
            print(game)
            print("***")
        return "*** end of bucket ***"

    def add_game(self, game=None):
        game_id = uuid.uuid4().hex
        self.games[game_id] = Game() if game is None else game
        return game_id

    def get_all_games(self):
        return self.games

    def get_game(self, key):
        if key in self.games:
            return self.games[key]
        return None

    def get_and_remove(self, key):
        return self.games.pop(key)

    def json(self, key=None):
        res = {}
        if key is not None and key in self.games:
            res = {key: self.games[key].json()}
        else:
            for k, v in self.games.items():
                game = self.games[k]
                res[k] = game.json()

        return res
