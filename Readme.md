# 🎫 **EVENTLIVE** - Sistema de Venta de Entradas

¡Bienvenido a **EVENTLIVE**! Esta es una aplicación web desarrollada en **Django** y **PostgreSQL** diseñada para la gestión y venta de entradas (tickets) para diferentes shows musicales, conciertos y obras de teatro.

[![Ver video en YouTube](https://img.youtube.com/vi/AthFxeFIi50/hqdefault.jpg)](https://youtu.be/AthFxeFIi50)
▶️ **[Haz clic para ver el video en YouTube](https://youtu.be/AthFxeFIi50)**

---

## 🚀 Requisitos Previos

Elegí cómo querés correr el proyecto:

### Opción A: Correr con Docker (recomendado)

Solo necesitás instalar:

| Requisito | Para verificar |
|---|---|
| **Docker Desktop** | `docker --version` |
| **Docker Compose** | `docker compose version` |

> Docker se encarga de todo el resto: Python, PostgreSQL, dependencias y base de datos.

### Opción B: Correr localmente (sin Docker)

Necesitás instalar en tu computadora:

| Requisito | Versión mínima | Para verificar |
|---|---|---|
| **Python** | 3.10+ | `python --version` |
| **PostgreSQL** | 14+ | `psql --version` |
| **Git** | cualquier versión | `git --version` |

---

## 🐳 Opción A: Correr con Docker

### 1. Clonar y levantar

```bash
git clone https://github.com/gonzalocabrera90/django-ticket.git
cd django-ticket
docker compose up --build
```

El contenedor ejecutará automáticamente las migraciones, cargará las ciudades y los datos de prueba la primera vez.

> Este setup automático lo hace `entrypoint.sh` que se ejecuta al iniciar el contenedor. No es necesario correr `setup.sh` ni `setup.ps1`, esos scripts son exclusivamente para setup local sin Docker.

### 2. Crear superuser (opcional)

En otra terminal, con los contenedores corriendo:

```bash
docker compose exec web python manage.py createsuperuser
```

### 3. Acceder

Abrí `http://127.0.0.1:8000/` en tu navegador.

### 4. Detener

```bash
docker compose down
```

---

## 💻 Opción B: Setup Local con Scripts

### 1. Crear la base de datos

Corré estos comandos en PostgreSQL una sola vez (`psql` o pgAdmin):

```sql
CREATE DATABASE eventlive_db;
CREATE USER eventlive_user WITH PASSWORD 'eventlive_password';
ALTER ROLE eventlive_user SET client_encoding TO 'utf8';
ALTER ROLE eventlive_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE eventlive_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE eventlive_db TO eventlive_user;
```

### 2. Clonar y ejecutar el script

El script hace todo automáticamente: crea el entorno virtual, instala dependencias, ejecuta migraciones, carga ciudades, seeds y opcionalmente crea el superuser.

* **Linux/macOS:**
```bash
git clone https://github.com/gonzalocabrera90/django-ticket.git
cd django-ticket
chmod +x setup.sh
./setup.sh
```

* **Windows (PowerShell):**
```powershell
git clone https://github.com/gonzalocabrera90/django-ticket.git
cd django-ticket
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

> Si en Windows aparece un error de permisos, ejecutá primero:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

### 3. Acceder

```bash

.venv\Scripts\activate

python manage.py runserver
```

Abrí `http://127.0.0.1:8000/` en tu navegador.

---

## 🔧 Configuración manual (referencia)

Si necesás hacer los pasos a mano en lugar de usar los scripts:

```bash
# Crear entorno virtual
python3 -m venv .venv          # Linux/macOS
python -m venv .venv           # Windows

# Activar entorno virtual
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Cargar ciudades (puede tardar varios minutos)
python manage.py cities_light

# Cargar datos de prueba
python manage.py shell < seeds/seed_completo.py              # Linux/macOS
python manage.py shell -c "import seeds.seed_completo"       # Windows

# Crear superuser
python manage.py createsuperuser
```

El archivo `.env` se configura automáticamente con los scripts. Si hacés los pasos a mano, copiá `.env.example` a `.env` y editá los datos de conexión a PostgreSQL.

---

## 💻 Uso de la Aplicación

### Admin de Django

Creá un superuser (si no lo hiciste con el script) y accedé a `http://127.0.0.1:8000/admin/`.

### Simulación de reserva de entradas

Para probar el flujo de compra con reservas vencidas:

```bash
python manage.py shell < seeds/seed_reserva.py
```

Para liberar las reservas expiradas:

```bash
python manage.py liberar_reservas
```

---

## 📋 Comandos útiles

| Comando | Descripción |
|---|---|
| `docker compose up --build` | Levantar con Docker (rebuild) |
| `docker compose down` | Detener Docker |
| `docker compose logs -f web` | Ver logs del contenedor web |
| `python manage.py runserver` | Iniciar servidor local |
| `python manage.py createsuperuser` | Crear usuario admin |
| `python manage.py liberar_reservas` | Liberar reservas vencidas |
| `python manage.py cities_light` | Recargar datos geográficos |
