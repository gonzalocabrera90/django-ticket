from django.utils.text import slugify
from decimal import Decimal
from shows.models import ShowPlace, Address, Sector, MapLayoutObject

print("==== INICIANDO PROCESO DE SEED DATA (MODELO SEPARADO) ====")

print("Vaciando tablas en PostgreSQL...")
cantidad_borrada, _ = ShowPlace.objects.all().delete()
print(f" -> Tablas limpiadas. Se eliminaron {cantidad_borrada} lugares previos.")
print("----------------------------------------------------")

estadios_data = [
    {
        "name": "Estadio José María Minella",
        "capacity": 42000,
        "viewbox": "0 0 1000 1000",
        "address": {"street": "Av. Mundial '78 y Olimpíadas", "city": "Mar del Plata", "state": "Buenos Aires", "zip_code": "B7600"},
        "sectors": [
            {"name": "Campo Frontal", "capacity": 8000, "geometry": {"type": "path", "d": "M703.5 505C700.457 559.271 693.413 583.853 668.349 614C621.818 629.332 585.394 632.393 509.5 632C441.378 631.773 405.42 628.976 349.651 614C324.522 582.688 315.868 558.735 310 505H703.5Z", "fill": "#1C7D88"}},
            {"name": "Campo Trasero", "capacity": 10000, "geometry": {"type": "path", "d": "M310 500C313.047 445.315 320.099 420.547 345.196 390.169C391.785 374.72 430.51 358.104 506.5 358.5C574.709 358.729 613.161 375.08 669 390.169C694.162 421.72 698.124 445.856 704 500H310Z", "fill": "#4D38AA"}},
            {"name": "Platea Central Destechada", "capacity": 9000, "geometry": {"type": "path", "d": "M292.5 238.5C461.882 162.772 555.906 164.867 722 243L672 383C538.258 335.878 466.814 335.918 346 383L292.5 238.5Z", "fill": "#B18484"}},
            {"name": "Platea Lateral Derecha", "capacity": 7300, "geometry": {"type": "path", "d": "M728.5 246C808.75 314.403 840.176 366.647 857 500C839.159 643.625 809.107 696.365 728.5 753L675.5 614C720.231 525.779 718.27 475.584 675.5 385L728.5 246Z", "fill": "#D82E2E"}},
            {"name": "Platea Lateral Izquierda", "capacity": 7300, "geometry": {"type": "path", "d": "M283.5 753C203.25 684.597 171.824 632.353 155 499C172.841 355.375 202.893 302.635 283.5 246L336.5 385C291.769 473.221 293.73 523.416 336.5 614L283.5 753Z", "fill": "#D82E2E"}}
        ],
        "layout_objects": [
            {"name": "ESCENARIO", "type": "STAGE", "geometry": {"type": "rect", "x": 422, "y": 635, "width": 174, "height": 59, "fill": "#222222"}}
        ]
    },
    {
        "name": "Movistar Arena",
        "capacity": 15000,
        "viewbox": "0 0 1000 1000",
        "address": {"street": "Humboldt 450", "city": "CABA", "state": "Buenos Aires", "zip_code": "C1414"},
        "sectors": [
            {"name": "Platea Baja Centro", "capacity": 500, "geometry": {"type": "path", "d": "M629.5 263.5L596 358.25H397.5L357 263.5H629.5Z", "fill": "#29B92E"}},
            {"name": "Platea Alta Centro", "capacity": 600, "geometry": {"type": "path", "d": "M666.5 195L643.5 259H351.5L325 195H666.5Z", "fill": "#B331C7"}},
            {"name": "Platea Baja Codo Derecho", "capacity": 360, "geometry": {"type": "path", "d": "M714 347.5L624 387.5L601 369L643.5 270L714 347.5Z", "fill": "#29B92E"}},
            {"name": "Platea Alta Codo Derecho", "capacity": 500, "geometry": {"type": "path", "d": "M677.5 202.5L790 316L737.5 347L646.5 263.5L677.5 202.5Z", "fill": "#B331C7"}},
            {"name": "Platea Baja Codo Izquierdo", "capacity": 360, "geometry": {"type": "path", "d": "M345.5 268.5L394 365.5L370 393L269 345.5L345.5 268.5Z", "fill": "#29B92E"}},
            {"name": "Platea Alta Codo Izquierdo", "capacity": 500, "geometry": {"type": "path", "d": "M312.5 202.5L345.5 263.5L263.5 344.5L202.5 315L312.5 202.5Z", "fill": "#B331C7"}},
            {"name": "Platea Baja Lateral Derecha", "capacity": 1900, "geometry": {"type": "path", "d": "M630.95 398.5L723.5 357V715L630.95 750.5V398.5Z", "fill": "#29B92E"}},
            {"name": "Platea Alta Lateral Derecha", "capacity": 2100, "geometry": {"type": "path", "d": "M735 355.5L795.5 322.5V701L735 728.5V355.5Z", "fill": "#B331C7"}},
            {"name": "Platea Baja Lateral Izquierda", "capacity": 1900, "geometry": {"type": "path", "d": "M270.5 355.5L366.5 401V747.5L270.5 718.5V355.5Z", "fill": "#29B92E"}},
            {"name": "Platea Alta Lateral Izquierdo", "capacity": 2100, "geometry": {"type": "path", "d": "M197.5 323L257 350V729.5L197.5 699.5V323Z", "fill": "#B331C7"}},
            {"name": "Campo VIP", "capacity": 1000, "geometry": {"type": "rect", "x": 384, "y": 662, "width": 231, "height": 76, "fill": "#1a427d"}},
            {"name": "Campo General", "capacity": 2300, "geometry": {"type": "rect", "x": 384, "y": 491, "width": 231, "height": 165, "fill": "#2056A7"}},
            {"name": "Campo Trasero", "capacity": 700, "geometry": {"type": "rect", "x": 384, "y": 391, "width": 231, "height": 92, "fill": "#2056A7"}},
        ],
        "layout_objects": [
            {"name": "ESCENARIO", "type": "STAGE", "geometry": {"type": "rect", "x": 439, "y": 744, "width": 123, "height": 55, "fill": "#222222"}}
        ]
    },
    {
        "name": "Estadio Luna Park",
        "capacity": 9000,
        "viewbox": "0 0 1000 1000",
        "address": {"street": "Av. Eduardo Madero 420", "city": "CABA", "state": "Buenos Aires", "zip_code": "C1106"},
        "sectors": [
            {"name": "Campo", "capacity": 3400, "geometry": {"type": "path", "d": "M249 414H771V608H249V414Z", "fill": "#50DF43"}},
            {"name": "Platea Lateral Madero", "capacity": 900, "geometry": {"type": "path", "d": "M789.5 480.5H923V622.5H789.5V480.5Z", "fill": "#3D41FF"}},
            {"name": "Platea Poolman Este", "capacity": 1180, "geometry": {"type": "path", "d": "M876.5 291L921.54 337.5V471.5H788V418.5L763.5 397H677.5V291H876.5Z", "fill": "#1417D2"}},
            {"name": "Super Poolman", "capacity": 1500, "geometry": {"type": "path", "d": "M347.5 280H671V397H347.5V280Z", "fill": "#400C99"}},
            {"name": "Platea Poolman Oeste", "capacity": 1180, "geometry": {"type": "path", "d": "M95 340.5L154.5 291H341V397H254L227 422V469.5H95V340.5Z", "fill": "#1417D2"}},
            {"name": "Platea Lateral Corrientes", "capacity": 900, "geometry": {"type": "rect", "x": 95, "y": 481, "width": 132, "height": 142, "fill": "#3D41FF"}},
            {"name": "Sector Discapacitados", "capacity": 150, "geometry": {"type": "rect", "x": 702, "y": 614, "width": 69, "height": 23, "fill": "#400C99"}}
        ],
        "layout_objects": [
            {"name": "ESCENARIO", "type": "STAGE", "geometry": {"type": "path", "d": "M382.5 637H629.5V706H382.5V637Z", "fill": "#222222"}}
        ]
    },
    {
        "name": "Estadio Mâs Monumental River Plate",
        "capacity": 84567,
        "viewbox": "0 0 1016 872",
        "address": {"street": "Av. Pres. Figueroa Alcorta 7597", "city": "CABA", "state": "Buenos Aires", "zip_code": "C1428"},
        "sectors": [
            {"name": "Sívori Alta", "capacity": 7000, "geometry": {"type": "path", "d": "M332.5 359.5C273.804 480.754 273.948 552.19 334.5 694L284.5 719.5C221.285 575.715 220 486 292 329.5L332.5 359.5Z", "fill": "#D50700"}},
            {"name": "San Martín Alta", "capacity": 5000, "geometry": {"type": "path", "d": "M718 321L670.5 349C549.66 225.518 459.294 229.941 336.5 348L296.5 321C425.682 156.882 582.995 157.935 718 321Z", "fill": "#D50700"}},
            {"name": "Centenario Alta", "capacity": 7000, "geometry": {"type": "path", "d": "M721.5 330.5C787.139 483.218 783.897 569.766 719 720.5L675 691.5C727.697 564.19 729.369 491.779 675 360.5L721.5 330.5Z", "fill": "#D50700"}},
            {"name": "Sívori Media", "capacity": 4000, "geometry": {"type": "path", "d": "M370 383.5C320.496 495.462 323.55 558.917 370 673L336.42 693C280.772 563.681 277.724 489.199 336.42 362L370 383.5Z", "fill": "#7B708C"}},
            {"name": "San Martín Media", "capacity": 3500, "geometry": {"type": "path", "d": "M666.5 351.951L632.5 375C552.535 280.185 464.391 280.162 375.5 373.039L340 349.009C460.102 230.707 551.216 227.231 666.5 351.951Z", "fill": "#7B708C"}},
            {"name": "Sívori Baja (Popular)", "capacity": 6000, "geometry": {"type": "path", "d": "M417 416V645.5L373 670.5C326.351 559.591 325.046 497.41 373 386.5L417 416Z", "fill": "#FF0505"}},
            {"name": "Belgrano Baja", "capacity": 3000, "geometry": {"type": "path", "d": "M630 377L590 405H419.5L377.5 376C469.713 279.486 548.514 284.168 630 377Z", "fill": "#FF0909"}},
            {"name": "Centenario Media", "capacity": 4000, "geometry": {"type": "path", "d": "M637.679 382.5L672.32 362C726.363 499.927 724.694 571.073 672.32 690L637.679 669.5C687.347 555.381 687.64 492.522 637.679 382.5Z", "fill": "#7B708C"}},
            {"name": "Centenario Baja", "capacity": 10000, "geometry": {"type": "path", "d": "M593.5 413L635 385C683.124 491.961 683.678 553.778 635 667.5L593.5 642.5V413Z", "fill": "#FF0909"}},
            {"name": "Campo Trasero", "capacity": 18000, "geometry": {"type": "rect", "x": 421, "y": 410, "width": 169, "height": 92, "fill": "#222222"}},
            {"name": "Campo VIP", "capacity": 12000, "geometry": {"type": "rect", "x": 421, "y": 508, "width": 169, "height": 89, "fill": "#7B708C"}}
        ],
        "layout_objects": [
             {"name": "ESCENARIO PRINCIPAL", "type": "STAGE", "geometry": {"type": "rect", "x": 426, "y": 604, "width": 159, "height": 35, "fill": "#000000"}}
            
        ]
    }
]

for estadio in estadios_data:
    place_obj = ShowPlace.objects.create(name=estadio["name"], capacity=estadio["capacity"], viewbox=estadio["viewbox"])
    
    addr = estadio["address"]
    Address.objects.create(place=place_obj, street=addr["street"], city=addr["city"], state=addr["state"], zip_code=addr["zip_code"])
    
    for sector in estadio["sectors"]:
        Sector.objects.create(place=place_obj, name=sector["name"], slug=slugify(sector["name"]), capacity=sector["capacity"], polygon_geometry=sector["geometry"])
    
    # NUEVO: Guardamos los objetos de diseño estructural
    for obj in estadio["layout_objects"]:
        geom = obj["geometry"]
        
        # Si es un rectángulo, calculamos matemáticamente el centro exacto para el texto (text_x, text_y)
        if geom["type"] == "rect":
            geom["text_x"] = geom["x"] + (geom["width"] / 2)
            geom["text_y"] = geom["y"] + (geom["height"] / 2) + 5  # +5 compensa la altura de la fuente
        
        # Para el Luna Park que tiene un escenario en Path, seteamos un centro manual estimado
        elif geom["type"] == "path" and obj["name"] == "ESCENARIO":
            geom["text_x"] = 506
            geom["text_y"] = 676

        MapLayoutObject.objects.create(place=place_obj, name=obj["name"], object_type=obj["type"], geometry=geom)
    
    print(f" -> Creado con éxito: {place_obj.name} (Sectores: {len(estadio['sectors'])}, Layout: {len(estadio['layout_objects'])})")

print("\n==== PROCESO FINALIZADO CON ÉXITO ====")