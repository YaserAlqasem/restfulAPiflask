from flask_restful import Resource
from flask import jsonify,json
from flask import flash, request
from models import db, User, UserSchema


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