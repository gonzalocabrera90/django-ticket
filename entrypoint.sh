#!/bin/bash
set -e

echo "=========================================="
echo "  EVENTLIVE - Iniciando contenedor..."
echo "=========================================="

# -------------------------------------------------------
# 1. Esperar a que PostgreSQL este disponible
# -------------------------------------------------------
echo "[1] Esperando a que PostgreSQL este listo..."
until python -c "import psycopg2; psycopg2.connect(dbname='$DB_NAME', host='$DB_HOST', port='$DB_PORT', user='$DB_USER', password='$DB_PASSWORD')" 2>/dev/null; do
    echo "  -> PostgreSQL no disponible, reintentando en 2 segundos..."
    sleep 2
done
echo "  -> PostgreSQL conectado"
echo ""
# -------------------------------------------------------
# 2. Ejecutar migraciones
# -------------------------------------------------------
echo "[2] Ejecutando migraciones..."
python manage.py migrate --noinput
echo "  -> Migraciones completadas"
echo ""

# -------------------------------------------------------
# 3. Cargar ciudades
# -------------------------------------------------------
echo "[3] Cargando datos geograficos..."
python manage.py cities_light
echo "  -> Datos geograficos cargados"
echo ""

# -------------------------------------------------------
# 4. Cargar seeds (solo si la tabla shows_show esta vacia)
# -------------------------------------------------------
echo "[4] Verificando datos de prueba..."
SEED_COUNT=$(python -c "import django, os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','ticket_project.settings'); django.setup(); from shows.models import Show; print(Show.objects.count())" 2>/dev/null || echo "0")
if [ "$SEED_COUNT" = "0" ]; then
    echo "  -> Tabla vacia, cargando seeds..."
    python manage.py shell < seeds/seed_completo.py
    echo "  -> Seeds cargados correctamente"
else
    echo "  -> Ya existen $SEED_COUNT shows, omitiendo seeds"
fi
echo ""

# -------------------------------------------------------
# 5. Ejecutar el comando original (CMD)
# -------------------------------------------------------
echo "=========================================="
echo "  Iniciando servidor Django..."
echo "=========================================="
exec "$@"
