from flask import Flask
from flask_jwt_extended import JWTManager

def create_app(config_filename):
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config.from_object(config_filename)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    jwt = JWTManager(app)
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from models import db
    db.init_app(app)

    return app

if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)