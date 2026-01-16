# Variáveis
DC = docker-compose
EXEC_WEB = $(DC) exec web

.PHONY: up down restart build migrate rollback logs shell seed

# Iniciar o projeto
up:
	$(DC) up -d

# Parar o projeto
down:
	$(DC) down

# Reconstruir e iniciar
build:
	$(DC) up --build -d

# Ver logs em tempo real
logs:
	$(DC) logs -f

# --- Base de Dados (Alembic / Flask-Migrate) ---

# Gerar uma nova versão de migração após alterar um Model
migrate:
	$(EXEC_WEB) flask db migrate -m "$(msg)"

# Aplicar migrações pendentes
upgrade:
	$(EXEC_WEB) flask db upgrade

# Reverter a última migração (Rollback)
rollback:
	$(EXEC_WEB) flask db downgrade

# --- Utilidades ---

# Entrar no terminal do container Python
shell:
	$(EXEC_WEB) /bin/bash

# Popular a base de dados com ATMs de teste
seed:
	$(EXEC_WEB) python seed.py