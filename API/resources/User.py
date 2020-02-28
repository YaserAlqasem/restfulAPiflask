from flask_restful import Resource
from flask import jsonify,json
from flask import flash, request
from models import db, User, UserSchema,RevokedToken
import bcrypt
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

try:
    from flask import _app_ctx_stack as ctx_stack
except ImportError:  
    from flask import _request_ctx_stack as ctx_stack

users_schema = UserSchema(many=True)
user_schema = UserSchema()


class SignUp(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
            
        user = User.query.filter_by(Username = json_data['Username']).first()
        if user is not None:
            return {'message': 'User already exists'}, 400
 
        else:
            user = User(
                Username=json_data['Username'],
                Email=json_data['Email'],
                Password=json_data['Password']
                )
            try:
                db.session.add(user)
                db.session.commit()
                return {
                    'message': 'User {} was created'.format(json_data['Username']),
                    }
            except:
                return {'message': 'Something went wrong'}, 500

class Login(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422

        print(json_data['Password'].encode('utf8'))
        print(json_data['Password'])
        found_user = User.query.filter_by(Username = json_data['Username']).first()
        
        if found_user:
            authenticated_user = bcrypt.checkpw(json_data['Password'].encode('utf8'),found_user.Password.encode("utf-8"))
            
            access_token = create_access_token(identity = json_data['Username'])
            refresh_token = create_refresh_token(identity = json_data['Username'])
            if authenticated_user:
                return {
                    'message': 'Logged in as {}'.format(found_user.Username),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    },200
            else:
                return {'message': 'Wrong credentials'}, 401

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti = jti)
            revoked_token.add()
            return {'message': 'logged out successfully'}
        except:
            return {'message': 'Something went wrong'}, 500

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti = jti)
            revoked_token.add()
            return {'message': 'logged out successfully'}
        except:
            return {'message': 'Something went wrong'}, 500

def get_raw_jwt():
    return getattr(ctx_stack.top, 'jwt', {})