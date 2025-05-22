from flask import Flask
from flask_cors import CORS  # import thêm CORS

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1234567890'

    # Thiết lập CORS để hỗ trợ gửi cookie qua các domain (nếu cần)
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

    # Import và đăng ký blueprint
    from website.views.routes import views
    from website.auth.routes import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
