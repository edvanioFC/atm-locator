import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv

# Importamos o dicionário de configurações do arquivo config.py na raiz
from config import config_dict

# Carregar variáveis do .env
load_dotenv()

# Inicializar extensões
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
login_manager.login_view = 'auth.login'  # type: ignore
login_manager.login_message = "Por favor, faça login para aceder a esta página."

def create_app():
    app = Flask(__name__)

    # Obtemos o nome do ambiente da variável de sistema ou usamos 'default'
    config_name = os.getenv('FLASK_ENV', 'default')
    
    # Aplica as configurações
    app.config.from_object(config_dict[config_name])
    
    # Inicializar componentes no contexto do app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    with app.app_context():
        # Configurar o carregador de utilizador (User Loader)
        from app.models import User
        
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # Importar e Registar Blueprints (Controladores)
        # Importamos de app.routes assumindo que tens o __init__.py lá
        from app.routes.main import main_bp
        from app.routes.auth import auth_bp
        from app.routes.admin import admin_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(admin_bp)

    return app