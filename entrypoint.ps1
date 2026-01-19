Write-Host "Iniciando entrypoint (Windows)..." -ForegroundColor Cyan

$ErrorActionPreference = "Stop"

# 1. Carregar variáveis de ambiente do .env para o processo atual
if (Test-Path ".env") {
    Get-Content ".env" | Where-Object { $_ -match '^\s*[^#=]+\s*=' } | ForEach-Object {
        $parts = $_ -split '=', 2
        $key = $parts[0].Trim()
        $val = $parts[1].Trim()
        [Environment]::SetEnvironmentVariable($key, $val, "Process")
    }
}

# 2. Determinar Host e Porta do Postgres a partir da URL
$dbHost = "localhost"
$dbPort = 5432

# Tenta extrair host e porta da string de conexão (ex: postgresql://user:pass@host:port/db)
if ($env:DATABASE_URL -match "@([^:/]+):(\d+)/") {
    $dbHost = $matches[1]
    $dbPort = $matches[2]
} elseif ($env:DATABASE_URL -match "@([^:/]+)/") {
    $dbHost = $matches[1]
}

Write-Host "Aguardando Postgres em ${dbHost}:${dbPort}..."

# 3. Loop de espera (TcpClient)
$maxRetries = 30
$retry = 0
while ($retry -lt $maxRetries) {
    try {
        $tcp = New-Object System.Net.Sockets.TcpClient
        $connect = $tcp.BeginConnect($dbHost, $dbPort, $null, $null)
        # Timeout de 1 segundo para conexão
        if ($connect.AsyncWaitHandle.WaitOne(1000, $false)) {
            if ($tcp.Connected) {
                $tcp.EndConnect($connect)
                $tcp.Close()
                Write-Host "Postgres pronto!" -ForegroundColor Green
                break
            }
        }
        $tcp.Close()
    } catch {}
    
    Write-Host "." -NoNewline
    Start-Sleep -Seconds 1
    $retry++
}

if ($retry -eq $maxRetries) {
    Write-Host "`nAVISO: Timeout aguardando base de dados. Tentando continuar..." -ForegroundColor Yellow
} else {
    Write-Host "" # Nova linha após os pontos
}

# 4. Definir executáveis (usar do venv se existir)
$py = "python"
$fl = "flask"
if (Test-Path ".venv\Scripts\python.exe") {
    $py = ".\.venv\Scripts\python.exe"
    $fl = ".\.venv\Scripts\flask.exe"
}

# 5. Migrations
if (-not (Test-Path "migrations")) {
    Write-Host "Inicializando diretório de migrations..."
    & $fl db init
}

Write-Host "Verificando mudanças nos modelos..."
$ts = Get-Date -Format "yyyy-MM-dd_HH-mm"
# Usamos try/catch para ignorar erro se não houver mudanças (exit code do alembic)
try { 
    & $fl db migrate -m "Auto migration $ts" 
} catch {
    Write-Host "Nenhuma mudança detectada ou erro na migração." -ForegroundColor Gray
}

Write-Host "Atualizando base de dados..."
& $fl db upgrade

# 6. Iniciar Aplicação
Write-Host "Iniciando servidor Flask..."
& $py run.py
