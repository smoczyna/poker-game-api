from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort
import jwt

from common.decorators import requires_login
from src.common.errors import UserError
from src.model.user import User, LoggedUser

__author__ = 'smok'

auth_api_blueprint = Blueprint('api/auth', __name__)


@auth_api_blueprint.route('/register', methods=['POST'])
def register():
    if not request.form or (not 'username' in request.form
                            or not 'email' in request.form
                            or not 'user_type' in request.form
                            or not 'password' in request.form
                            or not 'confirm_password' in request.form):
        abort(400, {"response": "error", "description": "Unsatisfied call, mandatory stuff is missing"})
    else:
        username = request.form['username']
        email = request.form['email']
        user_type = request.form['user_type']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password.__eq__(confirm_password):
            try:
                if User.register(username, email, user_type, password):
                    return jsonify({"response": "success", "description": "registration successful"})
            except UserError as e:
                return jsonify({"response": "error", "description": e.message})
        else:
            return jsonify({"response": "error", "description": "Given passwords doesn't match"})


@auth_api_blueprint.route('/login', methods=['POST'])
def login():
    user_id = None
    if not request.args:
        abort(400, {"response": "error", "description": "Unsatisfied call, mandatory stuff is missing"})

    if 'username' in request.args and 'password' in request.args:
        username = request.args['username']
        password = request.args['password']
        try:
            user_id = User.is_login_valid1(username, password)
        except UserError as e:
            return abort(403, {"error": e.message})

    elif 'email' in request.args and 'password' in request.args:
        email = request.args['email']
        password = request.args['password']
        try:
            user_id = User.is_login_valid2(email, password)
        except UserError as e:
            return abort(403, {"error": e.message})

    else:
        abort(403, {"response": "error", "description": "Unsatisfied call, mandatory stuff is missing"})

    try:
        if user_id is not None:
            user = User.get_by_id(user_id)
            from src.app import JWT_SECRET
            from src.app import JWT_ALGORITHM
            from src.app import JWT_EXP_DELTA_SECONDS
            payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

            logged_user = LoggedUser(user, True, jwt_token)
            response = jsonify(logged_user.json())
            return response
    except UserError as e:
        return abort(500, {"response": "error", "description": e.message})


@auth_api_blueprint.route('/logout', methods=['POST'])
def logout():
    # global private_listener
    # try:
    #     if private_listener:
    #         private_listener.__exit__()
    # except NameError:
    #     pass

    return jsonify({"info": "You logged out now"})


@auth_api_blueprint.route('/profile/<string:user_id>', methods=['GET'])
@requires_login
def profile(user_id):
    logged_user = User.get_by_id(user_id)
    if logged_user is not None:
        # member = Member.get_by_user_id(user_id)
        # family = None
        # if member is not None:
        #     family = Family.get_by_id(member.family_id)

        return jsonify({"response": "success",
                        "description": "You successfully logged in"})
        # "member": "no member yet" if member is None else member.json(),
        # "family": "no family yet" if family is None else family.json()})
    else:
        return abort(404, {"response": "error", "description": "user not found"})


@auth_api_blueprint.route('/profile/<string:user_id>/logged-user', methods=['GET'])
@requires_login
def get_logged_user(user_id):
    logged_user = User.get_by_id(user_id)
    if logged_user is not None:
        return jsonify(logged_user.serializable_json())
    else:
        return abort(404, {"response": "error", "description": "user not found"})
