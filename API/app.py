from flask import Blueprint
from flask_restful import Api
from resources.User import SignUp,Login,UserLogoutAccess

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(SignUp, '/register')
api.add_resource(Login, '/auth')
api.add_resource(UserLogoutAccess,'/logout1')