from flask import Blueprint
from flask_restful import Api
from resources.User import SignUp,Login,UserLogoutAccess,UserLogoutRefresh,TokenRefresh

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(SignUp, '/register')
api.add_resource(Login, '/auth')
api.add_resource(UserLogoutAccess,'/logout1')
api.add_resource(UserLogoutRefresh,'/logout2')
api.add_resource(TokenRefresh,'/refreshToken')