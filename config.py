import os
from datetime import timedelta

try:
    from dotenv import load_dotenv  # type: ignore
    # Carrega o ficheiro .env se ele existir
    load_dotenv()
except ImportError:
    # python-dotenv não está instalado
    pass

class Config:
    """Configurações Base."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret@123456789#')
    
    # Base de Dados - Fallback para SQLite se o Postgres não for definido
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:1234@localhost:5432/atm_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Segurança de Sessão
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Configurações de Upload (se fores guardar fotos dos ATMs)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/static/uploads')

class DevelopmentConfig(Config):
    """Configurações para Desenvolvimento Local."""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """Configurações para Produção."""
    DEBUG = False
    ENV = 'production'
    # Em produção, o segredo DEVE vir do ambiente
    SECRET_KEY = os.getenv('SECRET_KEY')

# Dicionário para facilitar a seleção do ambiente no app/__init__.py
config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}