#!/bin/bash

# Parar o script se qualquer comando falhar
set -e

# Esperar o Postgres ficar disponível
echo "Aguardando Postgres em $DATABASE_URL..."
# Usamos o comando 'timeout' para não ficar em loop infinito se o DB cair
while ! nc -z db 5432; do
  sleep 1
done
echo "Postgres pronto!"

# Inicializa o Flask-Migrate se necessário
if [ ! -d "migrations" ]; then
    echo "Inicializando diretório de migrations..."
    flask db init
fi

# Gera a migração
# Adicionamos a flag --allow-empty para evitar erro caso não existam mudanças
echo "Verificando mudanças nos modelos..."
flask db migrate -m "Auto migration $(date +%Y-%m-%d_%H-%M)" || echo "Nenhuma mudança detectada."

# Aplica no banco de dados
echo "Atualizando base de dados..."
flask db upgrade

# Inicia a aplicação
echo "Iniciando servidor Flask..."
exec python run.py