import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils import timezone

# Configuración del entorno de Django (ajustá 'config' por el nombre real de tu carpeta de proyecto)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shows.models import Show, ShowPlace, Sector, ShowSector

print("==== INICIANDO PROCESO DE SEED DATA PARA SHOWS ====")

# 1. Limpieza preventiva de shows anteriores (CASCADE eliminará los ShowSectors automáticamente)
print("Limpiando shows existentes...")
ShowSector.objects.all().delete()
Show.objects.all().delete()
print(" -> Tabla de Shows e inventarios comerciales limpiada.")
print("----------------------------------------------------")

# 2. Verificar que existan estadios en la base de datos
estadios = ShowPlace.objects.all()
if not estadios.exists():
    print("❌ ERROR: No se encontraron estadios en la base de datos. Por favor, ejecutá primero el seed de estadios.")
    exit()

# # 3. Listado masivo de 15 Shows realistas con su información base
# shows_pool = [
#     {"title": "Divididos - 35 Años", "description": "La aplanadora del rock celebra su trayectoria con un show de más de tres horas.", "dias_a_sumar": 35},
#     {"title": "Fito Páez - El Amor Después del Amor", "description": "El concierto histórico que celebra el disco más vendido de la música argentina.", "dias_a_sumar": 40},
#     {"title": "Airbag - Jinetes Cromados", "description": "Los hermanos Sardelli desatan su potencia eléctrica en un show cargado de solos de guitarra y energía.", "dias_a_sumar": 45},
#     {"title": "Los Fabulosos Cadillacs", "description": "El regreso de una leyenda de los ritmos latinos y el ska para bailar toda la noche.", "dias_a_sumar": 50},
#     {"title": "Ciro y los Persas - Ritual 2026", "description": "Andrés Ciro Martínez revive los clásicos de Los Piojos y recorre sus éxitos solistas con la energía de siempre.", "dias_a_sumar": 55},
#     {"title": "Miranda! - Hotel Miranda VIP", "description": "El dúo pop más icónico de Latinoamérica transforma el estadio en una verdadera fiesta bailable.", "dias_a_sumar": 60},
#     {"title": "Nicki Nicole - Alma Tour", "description": "La artista rosarina despliega su talento y sensibilidad en un show íntimo pero potente.", "dias_a_sumar": 65},
#     {"title": "Cuarteto de Nos - Lámina Once", "description": "Los uruguayos regresan con sus letras filosas e ingeniosas en una noche cargada de rock alternativo.", "dias_a_sumar": 75},
#     {"title": "Coldplay - Music of the Spheres II", "description": "El regreso del fenómeno global con su despliegue de luces, pulseras LED y un mensaje sustentable.", "dias_a_sumar": 90, "es_internacional": True},
#     {"title": "Metallica - M72 World Tour", "description": "Los gigantes del thrash metal llegan con su imponente escenario central 360 y una pared de sonido demoledora.", "dias_a_sumar": 95, "es_internacional": True},
#     {"title": "The Weeknd - After Hours til Dawn", "description": "Un viaje conceptual a través del synth-pop y R&B con una imponente escenografía post-apocalíptica.", "dias_a_sumar": 100, "es_internacional": True},
#     {"title": "Arctic Monkeys - Tranquility Base", "description": "Alex Turner y compañía traen el rock alternativo de Sheffield en una noche cargada de elegancia y riffs.", "dias_a_sumar": 105, "es_internacional": True},
#     {"title": "Green Day - The Saviors Tour", "description": "La banda ícono del punk rock celebra los aniversarios de Dookie y American Idiot en un show repleto de energía.", "dias_a_sumar": 110, "es_internacional": True},
#     {"title": "Dua Lipa - Radical Optimism Tour", "description": "La reina del pop británico llega para encender la pista con sus coreografías e hits mundiales.", "dias_a_sumar": 115, "es_internacional": True},
#     {"title": "Iron Maiden - Run For Your Lives Tour", "description": "La leyenda del heavy metal celebra 50 años de trayectoria junto a Bruce Dickinson y el infaltable Eddie.", "dias_a_sumar": 120, "es_internacional": True},
#     {"title": "Bruno Mars - Live in Concert", "description": "El showman definitivo del funk y el pop despliega su carisma, baile y banda en vivo impecable.", "dias_a_sumar": 125, "es_internacional": True},
#     {"title": "Radiohead - A Moon Shaped Tour", "description": "Una experiencia sónica e introspectiva única de la mano de Thom Yorke y Jonny Greenwood.", "dias_a_sumar": 130, "es_internacional": True},
#     {"title": "Travis Scott - Utopia Circus Maximus", "description": "El máximo exponente del trap mundial promete desatar los pogos más salvajes del planeta.", "dias_a_sumar": 135, "es_internacional": True},
#     {"title": "Foo Fighters - Everything or Nothing At All", "description": "Dave Grohl lidera la celebración eterna del rock de guitarras en un show cargado de pura pasión.", "dias_a_sumar": 140, "es_internacional": True},
#     {"title": "Depeche Mode - Memento Mori Tour", "description": "Los pioneros del synth-rock regresan en una noche nostálgica, electrónica y oscura de alto impacto.", "dias_a_sumar": 145, "es_internacional": True},
#     {"title": "Gorillaz - Cracker Island Live", "description": "Damon Albarn fusiona visuales animadas en pantallas gigantes con hip-hop, dub y pop alternativo.", "dias_a_sumar": 155, "es_internacional": True},
#     {"title": "Pearl Jam - Dark Matter World Tour", "description": "Eddie Vedder y los suyos traen el espíritu intacto del grunge de Seattle en un show enérgico y cambiante.", "dias_a_sumar": 150, "es_internacional": True},
#     {"title": "Daft Punk Tribute & David Guetta Live", "description": "Una noche dedicada a la música electrónica con un despliegue audiovisual de pantallas láser masivo.", "dias_a_sumar": 160, "es_internacional": True},
#     {"title": "Eric Clapton", "description": "El espíritu intacto del rock del britanico, en un show enérgico y cambiante.", "dias_a_sumar": 150, "es_internacional": True},
#     {"title": "Mark Knopler", "description": "El regreso del escoses en una noche nostálgica y de alto impacto.", "dias_a_sumar": 145, "es_internacional": True}
# ]

# # Rango de precios comerciales sugeridos según la jerarquía del evento
# # (VIP/Alta, Campo/Media, Popular/Baja)
# precios_templates = [
#     {"popular": 15000, "campo": 28000, "platea_vip": 45000},  # Show Estándar
#     {"popular": 18000, "campo": 35000, "platea_vip": 60000},  # Show Grande
#     {"popular": 25000, "campo": 48000, "platea_vip": 85000},  # Show Internacional / Mega VIP
# ]

# print("Asignando shows a lugares físicos y calculando precios sectorizados...")

# for i, show_data in enumerate(shows_pool):
#     # Asignamos los shows de forma cíclica entre los estadios cargados en la DB
#     estadio_asignado = estadios[i % estadios.count()]
    
#     # Creamos una fecha en el futuro partiendo desde hoy
#     fecha_show = timezone.now() + timedelta(days=show_data["dias_a_sumar"])
    
#     # Elegimos un combo de precios semi-aleatorio para darle variedad financiera
#     precios = random.choice(precios_templates)
    
#     # 4. Crear el Show base en la DB (precio general estimado como el de Campo)
#     show_obj = Show.objects.create(
#         title=show_data["title"],
#         description=f"{show_data['description']} Evento a realizarse en {estadio_asignado.name}.",
#         date=fecha_show,
#         price=Decimal(str(precios["campo"])),
#         image_url=f"https://picsum.photos/id/{100 + i}/800/600" # Imagen autogenerada placeholder
#     )
    
#     # 5. Buscar TODOS los sectores físicos reales que tiene este estadio asignado
#     sectores_del_estadio = Sector.objects.filter(place=estadio_asignado)
    
#     # 6. Conectamos cada sector al Show a través de la tabla intermedia 'ShowSector'
#     for sec in sectores_del_estadio:
#         # Evaluamos el nombre del sector para asignarle un precio lógico acorde
#         nombre_lower = sec.name.lower()
        
#         if "alta" in nombre_lower or "popular" in nombre_lower or "general" in nombre_lower:
#             precio_final = precios["popular"]
#         elif "vip" in nombre_lower or "central" in nombre_lower or "baja frontal" in nombre_lower:
#             precio_final = precios["platea_vip"]
#         else:
#             precio_final = precios["campo"] # Precio intermedio por defecto (Campos, Plateas Laterales, etc.)
            
#         # Generamos simulación de ventas aleatorias iniciales para testear barras de capacidad
#         entradas_vendidas = random.randint(0, int(sec.capacity * 0.15)) # Entre 0% y 15% vendido por defecto
#         entradas_reservadas = random.randint(0, int(sec.capacity * 0.05)) # Entre 0% y 5% reservado
        
#         # Guardamos en la tabla relacional de precios
#         ShowSector.objects.create(
#             show=show_obj,
#             sector=sec,
#             price=Decimal(str(precio_final)),
#             sold=entradas_vendidas,
#             reserved=entradas_reservadas
#             # Recordá que el método .save() calcula automáticamente los 'available'
#         )

#     print(f" -> Creado: '{show_obj.title}' en [{estadio_asignado.name}] con {sectores_del_estadio.count()} sectores vinculados.")

# print("\n==== PROCESO FINALIZADO CON ÉXITO: 15 SHOWS DISPONIBLES ====")