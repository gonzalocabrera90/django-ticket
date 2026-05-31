import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils import timezone
from django.utils.text import slugify

# Configuración del entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shows.models import Show, ShowPlace, Sector, ShowSector, Category

print("==== INICIANDO PROCESO DE SEED DATA (VERSION CATEGORÍAS) ====")

# 1. Limpieza preventiva profunda
print("Limpiando tablas de Shows y Categorías...")
Show.objects.all().delete()
Category.objects.all().delete()
print(" -> Base de datos comercial e historial limpiados.")
print("----------------------------------------------------")

# 2. Verificar estadios
estadios = ShowPlace.objects.all()
if not estadios.exists():
    print("❌ ERROR: No se encontraron estadios. Ejecutá primero el seed de estadios.")
    exit()

# 3. Creación de las Categorías Base en la DB
print("Creando categorías dinámicas...")
categorias_data = [
    {"name": "Rock", "icon": "bi-music-note-beamed", "color": "#dc3545"},      # Rojo
    {"name": "Pop", "icon": "bi-stars", "color": "#e83e8c"},                   # Rosa
    {"name": "Trap & Hip-Hop", "icon": "bi-lightning-fill", "color": "#6f42c1"},# Morado
    {"name": "Heavy Metal", "icon": "bi-activity", "color": "#343a40"},         # Oscuro
    {"name": "Electrónica", "icon": "bi-disc-fill", "color": "#007bff"},       # Azul
]

# Diccionario en memoria para asociar los objetos creados rápidamente
categorias_db = {}

for cat in categorias_data:
    obj = Category.objects.create(
        name=cat["name"],
        slug=slugify(cat["name"]),
        icon_class=cat["icon"],
        color_hex=cat["color"]
    )
    categorias_db[cat["name"]] = obj
    print(f" -> Categoría Creada: [{obj.name}] con color {obj.color_hex}")

print("----------------------------------------------------")

# 4. Listado de 30 Shows con su Categoría explícita asignada
shows_pool = [
    # --- NACIONALES ---
    {"title": "Duki - Americana Tour", "cat": "Trap & Hip-Hop", "desc": "El referente definitivo del trap argentino.", "dias": 15, "intl": False},
    {"title": "Wos - Descartable", "cat": "Rock", "desc": "Presentación oficial de su nuevo álbum con banda en vivo.", "dias": 20, "intl": False},
    {"title": "Babasónicos en Concierto", "cat": "Rock", "desc": "La banda más elegante del rock nacional repasa su discografía.", "dias": 25, "intl": False},
    {"title": "La Renga - Totalmente Poseídos", "cat": "Rock", "desc": "El banquete más esperado del año. Puro rock barrial.", "dias": 30, "intl": False},
    {"title": "Divididos - 35 Años", "cat": "Rock", "desc": "La aplanadora del rock celebra su trayectoria con un show demoledor.", "dias": 35, "intl": False},
    {"title": "Fito Páez - El Amor Después del Amor", "cat": "Rock", "desc": "El concierto histórico que celebra el disco más vendido de la historia nacional.", "dias": 40, "intl": False},
    {"title": "Airbag - Jinetes Cromados", "cat": "Rock", "desc": "Los hermanos Sardelli desatan su potencia eléctrica de guitarras.", "dias": 45, "intl": False},
    {"title": "Los Fabulosos Cadillacs", "cat": "Rock", "desc": "El regreso de una leyenda de los ritmos latinos, el ska y el rock.", "dias": 50, "intl": False},
    {"title": "Ciro y los Persas - Ritual 2026", "cat": "Rock", "desc": "Andrés Ciro Martínez revive los clásicos de Los Piojos.", "dias": 55, "intl": False},
    {"title": "Miranda! - Hotel Miranda VIP", "cat": "Pop", "desc": "El dúo pop más icónico de Latinoamérica transforma el estadio en una fiesta.", "dias": 60, "intl": False},
    {"title": "Nicki Nicole - Alma Tour", "cat": "Trap & Hip-Hop", "desc": "La artista rosarina despliega su talento y sensibilidad urbana.", "dias": 65, "intl": False},
    {"title": "Las Pastillas del Abuelo", "cat": "Rock", "desc": "Una velada de rock fusión y letras profundas barriales.", "dias": 70, "intl": False},
    {"title": "Cuarteto de Nos - Lámina Once", "cat": "Rock", "desc": "Los uruguayos regresan con sus letras filosas e ingeniosas.", "dias": 75, "intl": False},
    {"title": "El Kuelgue - Hola Precioso", "cat": "Pop", "desc": "Improvisación, absurdo y un despliegue musical exquisito.", "dias": 80, "intl": False},
    {"title": "Conociendo Rusia - Jet Love", "cat": "Rock", "desc": "El proyecto liderado por Mateo Sujatovich con su pop-rock clásico.", "dias": 85, "intl": False},
    
    # --- INTERNACIONALES ---
    {"title": "Coldplay - Music of the Spheres II", "cat": "Pop", "desc": "El regreso del fenómeno global con su despliegue de pulseras LED.", "dias": 90, "intl": True},
    {"title": "Metallica - M72 World Tour", "cat": "Heavy Metal", "desc": "Los gigantes del thrash metal llegan con su imponente escenario central 360.", "dias": 95, "intl": True},
    {"title": "The Weeknd - After Hours til Dawn", "cat": "Pop", "desc": "Un viaje conceptual a través del synth-pop y R&B espacial.", "dias": 100, "intl": True},
    {"title": "Arctic Monkeys - AM Tour", "cat": "Rock", "desc": "Alex Turner y compañía traen el rock alternativo de Sheffield con pura elegancia.", "dias": 105, "intl": True},
    {"title": "Green Day - The Saviors Tour", "cat": "Rock", "desc": "La banda ícono del punk rock celebra los aniversarios de Dookie.", "dias": 110, "intl": True},
    {"title": "Dua Lipa - Radical Optimism", "cat": "Pop", "desc": "La reina del pop británico llega para encender la pista con sus hits mundiales.", "dias": 115, "intl": True},
    {"title": "Iron Maiden - Run For Your Lives", "cat": "Heavy Metal", "desc": "La leyenda del heavy metal celebra 50 años de trayectoria junto a Eddie.", "dias": 120, "intl": True},
    {"title": "Bruno Mars - Live in Concert", "cat": "Pop", "desc": "El showman definitivo del funk y el pop despliega su carisma bailable.", "dias": 125, "intl": True},
    {"title": "Radiohead - Sonic Experience", "cat": "Rock", "desc": "Una experiencia sónica e introspectiva única de la mano de Thom Yorke.", "dias": 130, "intl": True},
    {"title": "Travis Scott - Utopia", "cat": "Trap & Hip-Hop", "desc": "El máximo exponente del trap mundial promete desatar los pogos más salvajes.", "dias": 135, "intl": True},
    {"title": "Foo Fighters - Electric Tour", "cat": "Rock", "desc": "Dave Grohl lidera la celebración eterna del rock de guitarras enérgico.", "dias": 140, "intl": True},
    {"title": "Depeche Mode - Memento Mori", "cat": "Electrónica", "desc": "Los pioneros del synth-rock regresan en una noche nostálgica y electrónica.", "dias": 145, "intl": True},
    {"title": "Pearl Jam - Dark Matter", "cat": "Rock", "desc": "Eddie Vedder y los suyos traen el espíritu intacto del grunge de Seattle.", "dias": 150, "intl": True},
    {"title": "Gorillaz - Cracker Island Live", "cat": "Pop", "desc": "Damon Albarn fusiona visuales animadas en pantallas con hip-hop y dub.", "dias": 155, "intl": True},
    {"title": "Eric Clapton", "description": "El espíritu intacto del rock del britanico, en un show enérgico y cambiante.", "dias_a_sumar": 150, "es_internacional": True},
    {"title": "Mark Knopfler", "description": "El regreso del escoses en una noche nostálgica y de alto impacto.", "dias_a_sumar": 145, "es_internacional": True}
]

# Plantillas de Precios
precios_nacionales = [{"popular": 15000, "campo": 28000, "platea_vip": 45000}, {"popular": 18000, "campo": 35000, "platea_vip": 60000}]
precios_internacionales = [{"popular": 35000, "campo": 65000, "platea_vip": 120000}, {"popular": 45000, "campo": 85000, "platea_vip": 160000}]

print("Viculando Shows con sus Categorías, Estadios y precios...")

for i, show_data in enumerate(shows_pool):
    estadio_asignado = estadios[i % estadios.count()]
    fecha_show = timezone.now() + timedelta(days=show_data["dias"])
    
    # Elegir matriz de precios
    precios = random.choice(precios_internacionales) if show_data["intl"] else random.choice(precios_nacionales)
    
    # Recuperamos el objeto Categoría correspondiente del diccionario mapeado en memoria
    categoria_objeto = categorias_db[show_data["cat"]]
    
    # Crear el Show asimilando la categoría
    show_obj = Show.objects.create(
        title=show_data["title"],
        description=f"{show_data['desc']} Espectáculo en vivo en {estadio_asignado.name}.",
        date=fecha_show,
        price=Decimal(str(precios["campo"])),
        image_url=f"https://picsum.photos/id/{150 + i}/800/600",
        category=categoria_objeto # <--- AQUÍ SE ASIGNA LA CATEGORÍA AL SHOW
    )
    
    # Generar la grilla de precios comerciales (ShowSector)
    sectores_del_estadio = Sector.objects.filter(place=estadio_asignado)
    for sec in sectores_del_estadio:
        nombre_lower = sec.name.lower()
        
        if "alta" in nombre_lower or "popular" in nombre_lower or "general" in nombre_lower:
            precio_final = precios["popular"]
        elif "vip" in nombre_lower or "central" in nombre_lower or "baja frontal" in nombre_lower:
            precio_final = precios["platea_vip"]
        else:
            precio_final = precios["campo"]
            
        entradas_vendidas = random.randint(0, int(sec.capacity * 0.10))
        entradas_reservadas = random.randint(0, int(sec.capacity * 0.03))
        
        ShowSector.objects.create(
            show=show_obj,
            sector=sec,
            price=Decimal(str(precio_final)),
            sold=entradas_vendidas,
            reserved=entradas_reservadas
        )

    print(f" -> Guardado: '{show_obj.title}' -> [{show_obj.category.name}] en {estadio_asignado.name}")

print(f"\n==== SEED FINALIZADO COMPLETAMENTE: {len(shows_pool)} SHOWS CON CATEGORÍAS DISPONIBLES ====")