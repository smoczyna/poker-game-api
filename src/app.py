from flask import Flask, jsonify
from flask_caching import Cache
from flask_cors import CORS
from common.database import Database
from endpoints.auth import auth_api_blueprint
from endpoints.game_play import games_api_blueprint
from endpoints.users import user_api_blueprint

__author__ = 'smok'

JWT_SECRET = 'N2d2ECghmy41RuFiU61ydG6FOwHyPJplnrHolgVqOJfVEQfHMfeKStIsjkCjPqkdJRwQpFffMV5A84Gpd4ebBg=='
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 30*60  # half an hour

config = {
    "DEBUG": True,
    "ENV": "dev",
    "SECRET_KEY": "'my secret stuff",
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)
cors = CORS(app, resources={"/api/*": {"origins": "*"}})
cache = Cache(app)
cache.init_app(app)

app.register_blueprint(auth_api_blueprint, url_prefix="/api/auth")
app.register_blueprint(user_api_blueprint, url_prefix="/api/user")
app.register_blueprint(games_api_blueprint, url_prefix="/api/game")
@app.route('/')
def home():
    return jsonify({"info": "This will be Poker Game API"})


if __name__ == '__main__':
    with app.app_context():
        Database.initialize()
        cache.clear()

    # app.run(port=8080) - port change, default is 5000
    app.run()