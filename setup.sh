#!/bin/bash
set -e

echo "=========================================="
echo "  EVENTLIVE - Script de Setup (Linux/macOS)"
echo "=========================================="
echo ""

# -------------------------------------------------------
# 0. Verificar que PostgreSQL este corriendo y la DB exista
# -------------------------------------------------------
echo "[0] Verificando PostgreSQL..."
echo ""
echo "  Antes de continuar, asegurate de tener PostgreSQL corriendo"
echo "  y haber creado la base de datos y el usuario ejecutando:"
echo ""
echo "    sudo -u postgres psql -c \""
echo "      CREATE DATABASE eventlive_db;"
echo "      CREATE USER eventlive_user WITH PASSWORD 'tu_contraseña_segura';"
echo "      ALTER ROLE eventlive_user SET client_encoding TO 'utf8';"
echo "      ALTER ROLE eventlive_user SET default_transaction_isolation TO 'read committed';"
echo "      ALTER ROLE eventlive_user SET timezone TO 'UTC';"
echo "      GRANT ALL PRIVILEGES ON DATABASE eventlive_db TO eventlive_user;"
echo "    \""
echo ""
read -p "  Presiona Enter para continuar cuando PostgreSQL este listo (o Ctrl+C para abortar)... "
echo ""

# -------------------------------------------------------
# 1. Crear archivo .env si no existe
# -------------------------------------------------------
echo "[1] Configurando archivo .env..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "  -> Archivo .env creado desde .env.example"
    echo "  -> IMPORTANTE: Edita .env con tus datos de PostgreSQL antes de continuar"
    echo "     DB_NAME=eventlive_db"
    echo "     DB_USER=eventlive_user"
    echo "     DB_PASSWORD=tu_contraseña_segura"
    echo ""
    read -p "  Edita el archivo .env y presiona Enter para continuar..."
else
    echo "  -> Archivo .env ya existe, omitiendo"
fi
echo ""

# -------------------------------------------------------
# 2. Crear entorno virtual
# -------------------------------------------------------
echo "[2] Creando entorno virtual..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "  -> Entorno virtual creado en .venv/"
else
    echo "  -> Entorno virtual ya existe, omitiendo"
fi
echo ""

# -------------------------------------------------------
# 3. Activar entorno virtual e instalar dependencias
# -------------------------------------------------------
echo "[3] Instalando dependencias..."
source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "  -> Dependencias instaladas correctamente"
echo ""

# -------------------------------------------------------
# 4. Ejecutar migraciones
# -------------------------------------------------------
echo "[4] Ejecutando migraciones de la base de datos..."
python manage.py migrate
echo "  -> Migraciones completadas"
echo ""

# -------------------------------------------------------
# 5. Cargar ciudades (puede tardar varios minutos)
# -------------------------------------------------------
echo "[5] Cargando datos geograficos (ciudades, provincias, paises)..."
echo "  -> Este proceso puede tardar varios minutos, por favor espera..."
python manage.py cities_light
echo "  -> Datos geograficos cargados"
echo ""

# -------------------------------------------------------
# 6. Cargar seeds de datos de prueba
# -------------------------------------------------------
echo "[6] Cargando datos de prueba (seeds)..."
python manage.py shell < seeds/seed_completo.py
echo "  -> Seeds cargados correctamente"
echo ""

# -------------------------------------------------------
# 7. Crear superusuario (opcional)
# -------------------------------------------------------
echo "[7] Crear usuario administrador (superuser)..."
read -p "  Queres crear un superuser ahora? (s/n): " crear_superuser
if [ "$crear_superuser" = "s" ] || [ "$crear_superuser" = "S" ]; then
    python manage.py createsuperuser
else
    echo "  -> Omitido. Podes crearlo despues con: python manage.py createsuperuser"
fi
echo ""

# -------------------------------------------------------
# Listo
# -------------------------------------------------------
echo "=========================================="
echo "  Setup completado!"
echo "=========================================="
echo ""
echo "  Para iniciar el servidor de desarrollo:"
echo ""
echo "    source .venv/bin/activate"
echo "    python manage.py runserver"
echo ""
echo "  Luego abri http://127.0.0.1:8000/"
echo ""
