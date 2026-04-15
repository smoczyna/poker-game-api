from flask import Blueprint, jsonify
from common.decorators import requires_login
from model.user import User

__author__ = 'smok'

user_api_blueprint = Blueprint('api/user', __name__)

@user_api_blueprint.route('/all')
@requires_login
def get_all_users():
    users = User.get_all()
    return jsonify([user.json_rest() for user in users])


@user_api_blueprint.route('/<string:user_id>')
@requires_login
def get_user_by_id(user_id):
    return jsonify([user.json_rest() for user in User.get_by_id(user_id)])


@user_api_blueprint.route('/<string:user_type>')
@requires_login
def get_user_by_type(user_type):
    return jsonify([user.json_rest() for user in User.get_by_type(user_type)])


@user_api_blueprint.route('/<string:user_type>')
@requires_login
def get_active_users_by_type(user_type):
    return jsonify([user.json_rest() for user in User.get_active_by_type(user_type)])
