#!/bin/bash
# setup.sh - Script de configuração inicial

echo "Iniciando configuração do Localizador de ATM..."

# 1. Criar ambiente virtual se não existir
if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv .venv
fi

# 2. Ativar venv e instalar dependências
source .venv/bin/activate
echo "Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente (.env)
if [ ! -f ".env" ]; then
    echo "Criando ficheiro .env inicial..."
    cat <<EOT >> .env
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:1234@localhost:5432/atm_db
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(24))')
PORT=5000
ALLOWED_HOSTS=0.0.0.0
EOT
    echo "Nota: Edita o .env com as tuas credenciais do Postgres."
fi

# 4. Dar permissão ao entrypoint
chmod +x entrypoint.sh

# 5. Gerar certificado SSL autoassinado para desenvolvimento
if [ ! -f "cert.pem" ] || [ ! -f "key.pem" ]; then
    echo "Gerando certificado SSL autoassinado..."
    openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=localhost"
fi

flask db init || echo "Migrations já inicializadas."
flask db migrate -m "Migracao inicial" || echo "Nenhuma mudança detectada."
flask db upgrade 

echo "Configuração concluída!"
echo "Para iniciar use: source .venv/bin/activate && python run.py"