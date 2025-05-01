from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1234567890'

    # Import và đăng ký blueprint
    from website.views.routes import views  # views.py phải chứa biến views = Blueprint(...)
    from website.auth.routes import auth  # Đảm bảo đường dẫn đúng

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
