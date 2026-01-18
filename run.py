import os
import mimetypes

mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

from flask_migrate import upgrade
from app import create_app, db
from app.models.user import User
from app.schemas.user_schema import UserCreate

app = create_app()

PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('ALLOWED_HOSTS', 'localhost')

def boot_app():
    with app.app_context():
        #Executa migrations pendentes automaticamente
        print("Aplicando migrations no Postgres...")
        upgrade()
        print("Migrations aplicadas com sucesso.")
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Pydantic valida os dados antes da inserção
            admin_data = UserCreate(
                username="admin",
                email="admin@local.com",
                password="admin@123"
            )
            
            user_payload = admin_data.model_dump(
                exclude={'password'}
            )
            
            new_admin = User(**user_payload)
            
            new_admin.set_password(admin_data.password)
            
            db.session.add(new_admin)
            db.session.commit()
            print("Admin criado com sucesso.")

if __name__ == "__main__":
    boot_app()
    
    # Verifica a existência de certificados SSL para rodar em HTTPS
    ssl_context = None
    cert_path = 'cert.pem'
    key_path = 'key.pem'

    if os.path.exists(cert_path) and os.path.exists(key_path):
        ssl_context = (cert_path, key_path)
        print(f"Certificados SSL encontrados. A aceder em: https://{HOST}:{PORT}")
    else:
        print(f"Certificados SSL não encontrados. A aceder em: http://{HOST}:{PORT}")
        print("Atenção: A geolocalização pode não funcionar em HTTP. Gere certificados SSL para habilitar HTTPS.")

    app.run(host=HOST, port=PORT, ssl_context=ssl_context)