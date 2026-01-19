# Localizador de ATM 

**O Localizador de ATM** é uma aplicação web completa desenvolvida em Flask que permite aos utilizadores encontrar caixas multibanco (ATMs) próximas, traçar rotas e gerir informações. A aplicação inclui um sistema robusto de autenticação, um painel de administração para gestão de dados e uma interface de mapa interativa.

---

##  Funcionalidades Principais

*   **Autenticação de Utilizadores:** Registo, login, logout, e recuperação de senha por email.
*   **Gestão de Perfil:** Os utilizadores podem editar o seu perfil e alterar a senha.
*   **Mapa Interativo:** Visualização de ATMs num mapa (usando Leaflet.js) com base na geolocalização do utilizador.
*   **Pesquisa e Filtragem:** Pesquisa dinâmica de ATMs por nome.
*   **Cálculo de Rota:** Traça a rota desde a localização do utilizador até ao ATM selecionado, mostrando a distância e o tempo estimado.
*   **Painel de Administração:**
    *   Gestão completa de ATMs (Adicionar, Editar, Apagar).
    *   Gestão de Utilizadores (Visualizar, Apagar).
*   **Segurança:** Hashing de senhas, proteção de rotas, validação de dados com Pydantic.
*   **Ambiente de Desenvolvimento:** Configuração automatizada com script `setup.sh` e suporte para HTTPS com certificados autoassinados.

---

##  Tecnologias Utilizadas

*   **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Migrate, Pydantic
*   **Base de Dados:** PostgreSQL
*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
*   **Mapas:** Leaflet.js, OpenStreetMap, Leaflet Routing Machine
*   **Servidor:** Werkzeug (para desenvolvimento)
*   **Outros:** python-dotenv, itsdangerous

---

##  Instalação e Configuração

Siga os passos abaixo para configurar e executar o projeto no seu ambiente local.

### 1. Pré-requisitos

*   **Python 3.8+** e `pip`
*   **PostgreSQL:** Uma instância a correr localmente ou remotamente.
*   **Git:** Para clonar o repositório.
*   **OpenSSL:** Para gerar os certificados SSL (geralmente já vem instalado em sistemas Linux/macOS).

### 2. Clonar o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd atm_locator
```

### 3. Configurar o Ambiente

O projeto inclui um script de configuração (`setup.sh`) que automatiza a maior parte do processo.

Execute o script:
```bash
bash setup.sh
```

O script irá realizar as seguintes ações:
1.  Criar um ambiente virtual (`.venv`).
2.  Instalar todas as dependências do `requirements.txt`.
3.  Criar um ficheiro `.env` a partir de um template.
4.  Gerar certificados SSL (`cert.pem` e `key.pem`) para permitir HTTPS, essencial para a geolocalização no navegador.
5.  Inicializar e aplicar as migrações da base de dados.

### 4. Configurar a Base de Dados

Após executar o `setup.sh`, abra o ficheiro `.env` que foi criado e edite a variável `DATABASE_URL` com as suas credenciais do PostgreSQL.

**Exemplo de `.env`:**
```env
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:1234@localhost:5432/atm_db
SECRET_KEY=uma_chave_secreta_super_longa_e_aleatoria
PORT=5000
ALLOWED_HOSTS=0.0.0.0

# Configuração de Email (opcional, para recuperação de senha)
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
```
**Nota:** Certifique-se de que a base de dados especificada em `DATABASE_URL` existe no seu servidor PostgreSQL.

---

##  Executar a Aplicação

Após a configuração, ative o ambiente virtual e inicie a aplicação:

```bash
source .venv/bin/activate
python run.py
```

A aplicação estará disponível em **`https://localhost:5000`**. O uso de `https` é ativado pelos certificados gerados.

### Credenciais de Administrador

Na primeira execução, um utilizador administrador padrão é criado:
*   **Email:** `admin@local.com`
*   **Senha:** `admin@123`

Use estas credenciais para aceder ao painel de administração em `/admin/dashboard`.

---

##  Estrutura do Projeto

```
.
├── app/                    # Módulo principal da aplicação Flask
│   ├── models/             # Modelos de dados (SQLAlchemy)
│   ├── routes/             # Definição das rotas (Blueprints)
│   ├── schemas/            # Esquemas de validação (Pydantic)
│   ├── static/             # Ficheiros estáticos (CSS, JS, Imagens)
│   ├── templates/          # Templates HTML (Jinja2)
│   └── __init__.py         # Fábrica da aplicação (create_app)
├── migrations/             # Ficheiros de migração (Alembic)
├── .env                    # Variáveis de ambiente (NÃO versionar)
├── config.py               # Configurações da aplicação
├── requirements.txt        # Dependências Python
├── run.py                  # Ponto de entrada para executar a app
├── setup.sh                # Script de configuração inicial
└── README.md               # Este ficheiro
```
