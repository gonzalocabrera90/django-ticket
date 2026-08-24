# EVENTLIVE - Script de Setup (Windows PowerShell)
# Ejecutar desde la raiz del proyecto: .\setup.ps1

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  EVENTLIVE - Script de Setup (Windows)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# -------------------------------------------------------
# 0. Verificar que PostgreSQL este corriendo y la DB exista
# -------------------------------------------------------
Write-Host "[0] Verificando PostgreSQL..." -ForegroundColor Yellow
Write-Host ""
Write-Host "  Antes de continuar, asegurate de tener PostgreSQL corriendo"
Write-Host "  y haber creado la base de datos y el usuario ejecutando en psql:"
Write-Host ""
Write-Host "    CREATE DATABASE eventlive_db;"
Write-Host "    CREATE USER eventlive_user WITH PASSWORD 'tu_contraseña_segura';"
Write-Host "    ALTER ROLE eventlive_user SET client_encoding TO 'utf8';"
Write-Host "    ALTER ROLE eventlive_user SET default_transaction_isolation TO 'read committed';"
Write-Host "    ALTER ROLE eventlive_user SET timezone TO 'UTC';"
Write-Host "    GRANT ALL PRIVILEGES ON DATABASE eventlive_db TO eventlive_user;"
Write-Host ""
Read-Host "  Presiona Enter para continuar cuando PostgreSQL este listo (o Ctrl+C para abortar)"
Write-Host ""

# -------------------------------------------------------
# 1. Crear archivo .env si no existe
# -------------------------------------------------------
Write-Host "[1] Configurando archivo .env..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "  -> Archivo .env creado desde .env.example" -ForegroundColor Green
    Write-Host "  -> IMPORTANTE: Edita .env con tus datos de PostgreSQL antes de continuar"
    Write-Host "     DB_NAME=eventlive_db"
    Write-Host "     DB_USER=eventlive_user"
    Write-Host "     DB_PASSWORD=tu_contraseña_segura"
    Write-Host ""
    Read-Host "  Edita el archivo .env y presiona Enter para continuar"
} else {
    Write-Host "  -> Archivo .env ya existe, omitiendo" -ForegroundColor DarkGray
}
Write-Host ""

# -------------------------------------------------------
# 2. Crear entorno virtual
# -------------------------------------------------------
Write-Host "[2] Creando entorno virtual..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "  -> Entorno virtual creado en .venv\" -ForegroundColor Green
} else {
    Write-Host "  -> Entorno virtual ya existe, omitiendo" -ForegroundColor DarkGray
}
Write-Host ""

# -------------------------------------------------------
# 3. Activar entorno virtual e instalar dependencias
# -------------------------------------------------------
Write-Host "[3] Instalando dependencias..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q
Write-Host "  -> Dependencias instaladas correctamente" -ForegroundColor Green
Write-Host ""

# -------------------------------------------------------
# 4. Ejecutar migraciones
# -------------------------------------------------------
Write-Host "[4] Ejecutando migraciones de la base de datos..." -ForegroundColor Yellow
python manage.py migrate
Write-Host "  -> Migraciones completadas" -ForegroundColor Green
Write-Host ""

# -------------------------------------------------------
# 5. Cargar ciudades (puede tardar varios minutos)
# -------------------------------------------------------
Write-Host "[5] Cargando datos geograficos (ciudades, provincias, paises)..." -ForegroundColor Yellow
Write-Host "  -> Este proceso puede tardar varios minutos, por favor espera..." -ForegroundColor DarkGray
python manage.py cities_light
Write-Host "  -> Datos geograficos cargados" -ForegroundColor Green
Write-Host ""

# -------------------------------------------------------
# 6. Cargar seeds de datos de prueba
# -------------------------------------------------------
Write-Host "[6] Cargando datos de prueba (seeds)..." -ForegroundColor Yellow
python manage.py shell -c "import seeds.seed_completo"
Write-Host "  -> Seeds cargados correctamente" -ForegroundColor Green
Write-Host ""

# -------------------------------------------------------
# 7. Crear superusuario (opcional)
# -------------------------------------------------------
Write-Host "[7] Crear usuario administrador (superuser)..." -ForegroundColor Yellow
$crear_superuser = Read-Host "  Queres crear un superuser ahora? (s/n)"
if ($crear_superuser -eq "s" -or $crear_superuser -eq "S") {
    python manage.py createsuperuser
} else {
    Write-Host "  -> Omitido. Podes crearlo despues con: python manage.py createsuperuser" -ForegroundColor DarkGray
}
Write-Host ""

# -------------------------------------------------------
# Listo
# -------------------------------------------------------
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Setup completado!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Para iniciar el servidor de desarrollo:"
Write-Host ""
Write-Host "    .venv\Scripts\activate"
Write-Host "    python manage.py runserver"
Write-Host ""
Write-Host "  Luego abri http://127.0.0.1:8000/"
Write-Host ""
