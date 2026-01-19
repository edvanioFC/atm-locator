Write-Host "Iniciando configuração do Localizador de ATM (Windows)..." -ForegroundColor Cyan

# 1. Criar ambiente virtual se não existir
if (-not (Test-Path ".venv")) {
    Write-Host "Criando ambiente virtual..."
    python -m venv .venv
}

# 2. Instalar dependências (chamando diretamente do venv para garantir o caminho)
Write-Host "Instalando dependências..."
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\pip.exe install -r requirements.txt

# 3. Configurar variáveis de ambiente (.env)
if (-not (Test-Path ".env")) {
    Write-Host "Criando ficheiro .env inicial..."
    
    # Gerar chave secreta usando python
    $secret = & .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(24))"
    
    $envContent = "FLASK_ENV=development`n" +
                "DATABASE_URL=postgresql://postgres:1234@localhost:5432/atm_db`n" +
                "SECRET_KEY=$secret`n" +
                "PORT=5000`n" +
                "ALLOWED_HOSTS=0.0.0.0"
    
    Set-Content .env $envContent -Encoding UTF8
    Write-Host "Nota: Edita o .env com as tuas credenciais do Postgres." -ForegroundColor Yellow
}

# 4. Gerar certificado SSL autoassinado
# Verifica se o OpenSSL está instalado (comum se tiver Git instalado)
if ((-not (Test-Path "cert.pem")) -or (-not (Test-Path "key.pem"))) {
    if (Get-Command openssl -ErrorAction SilentlyContinue) {
        Write-Host "Gerando certificado SSL autoassinado..."
        openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=localhost"
    } else {
        Write-Host "AVISO: OpenSSL não encontrado no PATH." -ForegroundColor Yellow
        Write-Host "O HTTPS pode não funcionar. Instale o Git Bash ou OpenSSL para Windows para gerar os certificados."
    }
}

# 5. Base de Dados
$env:FLASK_APP = "run.py"

Write-Host "Configurando base de dados..."
# O 'try' abafa o erro se o init já tiver sido feito
try { & .\.venv\Scripts\flask.exe db init *>$null } catch {}

& .\.venv\Scripts\flask.exe db migrate -m "Migracao inicial"
& .\.venv\Scripts\flask.exe db upgrade

Write-Host "Configuração concluída!" -ForegroundColor Green
Write-Host "Para iniciar use os comandos:"
Write-Host "  .\.venv\Scripts\activate"
Write-Host "  python run.py"