import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from datetime import datetime

wb = openpyxl.Workbook()

# Estilos
header_fill = PatternFill(start_color="1a365d", end_color="1a365d", fill_type="solid")
header_font = Font(color="FFFFFF", bold=True, size=11)
subheader_fill = PatternFill(start_color="2c5282", end_color="2c5282", fill_type="solid")
subheader_font = Font(color="FFFFFF", bold=True, size=10)
example_fill = PatternFill(start_color="fffbeb", end_color="fffbeb", fill_type="solid")
thin_border = Border(
    left=Side(style='thin', color='e2e8f0'),
    right=Side(style='thin', color='e2e8f0'),
    top=Side(style='thin', color='e2e8f0'),
    bottom=Side(style='thin', color='e2e8f0')
)

def style_header(ws, row=1):
    for cell in ws[row]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = thin_border

def add_comment(ws, cell, text):
    ws[cell].comment = Comment(text, "Sistema Pueblito Boyacense")

def auto_width(ws, min_width=12, max_width=45):
    for col in ws.columns:
        max_length = 0
        column = None
        for cell in col:
            if column is None and hasattr(cell, 'column_letter'):
                column = cell.column_letter
            try:
                length = len(str(cell.value)) if cell.value else 0
                if length > max_length:
                    max_length = length
            except:
                pass
        if column:
            adjusted = min(max(max_length + 2, min_width), max_width)
            ws.column_dimensions[column].width = adjusted

def add_example_row(ws, values, row):
    for col, val in enumerate(values, 1):
        cell = ws.cell(row=row, column=col, value=val)
        cell.fill = example_fill
        cell.border = thin_border
        cell.font = Font(italic=True, color="475569")

# === HOJA 1: INSTRUCCIONES ===
ws = wb.active
ws.title = "Instrucciones"
ws['A1'] = "Guía para llenar el Excel de contenido — Pueblito Boyacense"
ws['A1'].font = Font(size=16, bold=True, color="1a365d")
ws.merge_cells('A1:D1')

instructions = [
    ("Hoja", "Para qué sirve", "Quién la llena", "Importancia"),
    ("Comercios", "Datos generales de cada negocio del complejo", "Administración o comerciante", "Alta"),
    ("Servicios", "Catálogo de productos o experiencias ofrecidas", "Cada comercio", "Alta"),
    ("Precios y Ofertas", "Precios actuales, promociones y descuentos", "Cada comercio", "Alta"),
    ("Multimedia", "Fotos, videos y descripción de cada archivo", "Cada comercio", "Alta"),
    ("FAQs Chatbot", "Preguntas frecuentes y respuestas para entrenar la IA", "Cada comercio", "Alta"),
    ("Categorías", "Lista de categorías permitidas", "Administración", "Media"),
    ("Tags", "Lista de etiquetas para filtros", "Administración", "Media"),
    ("Manzanas", "Ubicaciones dentro del complejo", "Administración", "Media"),
    ("Eventos", "Eventos, ferias y temporadas especiales", "Administración", "Media"),
    ("Usuarios Admin", "Personas que administrarán el sistema", "Administración", "Baja"),
]

for r, row_data in enumerate(instructions, 3):
    for c, val in enumerate(row_data, 1):
        ws.cell(row=r, column=c, value=val)

style_header(ws, 3)
ws['A3'].fill = subheader_fill
ws['A3'].font = subheader_font
auto_width(ws)

ws['A16'] = "Reglas generales:"
ws['A16'].font = Font(bold=True, size=12, color="1a365d")
rules = [
    "1. No modificar los nombres de las hojas ni de las columnas (son usadas por el sistema).",
    "2. Las filas de ejemplo están en color amarillo claro; bórralas antes de entregar el archivo final.",
    "3. Los campos marcados con * son obligatorios.",
    "4. Para fotos y videos, escriba el nombre exacto del archivo (ej: cafeteria_la_casona_fachada.jpg).",
    "5. Para el chatbot, mientras más preguntas y respuestas incluya, mejor atenderá el bot.",
    "6. Use el mismo nombre de comercio en todas las hojas para que el sistema los relacione.",
]
for i, rule in enumerate(rules, 17):
    ws.cell(row=i, column=1, value=rule)
    ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=4)

# === HOJA 2: COMERCIOS ===
ws = wb.create_sheet("Comercios")
headers = ["ID Comercio*", "Nombre del comercio*", "Categoría principal*", "Manzana / Ubicación*",
           "Nombre del responsable", "Teléfono WhatsApp*", "Teléfono llamada", "Correo electrónico",
           "Horario de atención*", "Descripción general", "Logo (archivo)", "Estado*"]
ws.append(headers)
style_header(ws)

for i, h in enumerate(headers, 1):
    add_comment(ws, f"{get_column_letter(i)}1", {
        "ID Comercio*": "Código único corto. Ej: casona01, artesania_maria",
        "Nombre del comercio*": "Nombre comercial como quieren que aparezca.",
        "Categoría principal*": "Debe coincidir con una categoría de la hoja Categorías.",
        "Manzana / Ubicación*": "Debe coincidir con una manzana de la hoja Manzanas.",
        "Nombre del responsable": "Persona de contacto dentro del comercio.",
        "Teléfono WhatsApp*": "Número con código de país. Ej: 573001234567",
        "Teléfono llamada": "Si es diferente al WhatsApp. Ej: 6011234567",
        "Correo electrónico": "Opcional.",
        "Horario de atención*": "Ej: Lunes a Domingo 9:00 a.m. - 8:00 p.m.",
        "Descripción general": "Breve historia o propuesta de valor del comercio.",
        "Logo (archivo)": "Nombre del archivo de logo. Ej: logo_casona.png",
        "Estado*": "Activo o Inactivo."
    }.get(h, ""))

add_example_row(ws, ["casona01", "Cafetería La Casona", "Gastronomía", "Manzana 1",
                     "María Gómez", "573001234567", "6011234567", "lacasona@email.com",
                     "Lun-Dom 9am-8pm", "Café de origen boyacense con postres artesanales.",
                     "logo_casona.png", "Activo"], 2)

# Validación de estado
dv_estado = DataValidation(type="list", formula1='"Activo,Inactivo"', allow_blank=False)
ws.add_data_validation(dv_estado)
dv_estado.add(f'L2:L1000')

auto_width(ws)

# === HOJA 3: SERVICIOS ===
ws = wb.create_sheet("Servicios")
headers = ["ID Servicio*", "Nombre del servicio*", "Comercio*", "Categoría*", "Manzana / Ubicación*",
           "Descripción corta*", "Descripción larga", "Incluye", "No incluye", "Duración / Capacidad",
           "Tags", "Destacado", "Estado*"]
ws.append(headers)
style_header(ws)

for i, h in enumerate(headers, 1):
    add_comment(ws, f"{get_column_letter(i)}1", {
        "ID Servicio*": "Código único. Ej: srv001, tour_villa_leyva",
        "Nombre del servicio*": "Nombre del producto o experiencia.",
        "Comercio*": "Debe coincidir con el nombre de la hoja Comercios.",
        "Categoría*": "Debe coincidir con la hoja Categorías.",
        "Manzana / Ubicación*": "Debe coincidir con la hoja Manzanas.",
        "Descripción corta*": "Texto de 1-2 líneas para el catálogo.",
        "Descripción larga": "Texto completo para la ficha del servicio.",
        "Incluye": "Ej: Bebida de bienvenida, guía, degustación.",
        "No incluye": "Ej: Transporte, propinas.",
        "Duración / Capacidad": "Ej: 2 horas, máximo 10 personas.",
        "Tags": "Separados por coma. Ej: Familiar,Romántico,Artesanal",
        "Destacado": "Sí o No. Aparece en sección destacada del catálogo.",
        "Estado*": "Activo o Inactivo."
    }.get(h, ""))

add_example_row(ws, ["srv001", "Tour de 7 pueblos", "Cafetería La Casona", "Tour",
                     "Manzana 1", "Recorrido guiado por Villa de Leyva, Tibasosa, Tenza y más.",
                     "Experiencia completa de un día con guía certificado, almuerzo típico y transporte.",
                     "Almuerzo, guía, transporte", "Propinas, souvenirs", "8 horas, máx 15 pers",
                     "Familiar,Cultural,Activo", "Sí", "Activo"], 2)

# Validaciones
dv_destacado = DataValidation(type="list", formula1='"Sí,No"', allow_blank=True)
ws.add_data_validation(dv_destacado)
dv_destacado.add(f'L2:L1000')

ws.add_data_validation(dv_estado)
dv_estado.add(f'M2:M1000')

auto_width(ws)

# === HOJA 4: PRECIOS Y OFERTAS ===
ws = wb.create_sheet("Precios y Ofertas")
headers = ["ID Servicio*", "Nombre del servicio*", "Precio normal*", "Precio oferta",
           "Moneda*", "Tipo de oferta", "Días aplicables", "Horario aplicable",
           "Vigencia desde", "Vigencia hasta", "Notas"]
ws.append(headers)
style_header(ws)

for i, h in enumerate(headers, 1):
    add_comment(ws, f"{get_column_letter(i)}1", {
        "ID Servicio*": "Debe coincidir con la hoja Servicios.",
        "Nombre del servicio*": "Nombre del servicio.",
        "Precio normal*": "Precio actual sin oferta. Solo números.",
        "Precio oferta": "Precio con descuento, si aplica.",
        "Moneda*": "COP, USD, etc.",
        "Tipo de oferta": "Ej: 2x1, 20% descuento, Happy Hour.",
        "Días aplicables": "Ej: Lunes a Miércoles, fines de semana.",
        "Horario aplicable": "Ej: 2pm-5pm.",
        "Vigencia desde": "Fecha inicio de la oferta (DD/MM/AAAA).",
        "Vigencia hasta": "Fecha fin de la oferta (DD/MM/AAAA).",
        "Notas": "Restricciones o condiciones adicionales."
    }.get(h, ""))

add_example_row(ws, ["srv001", "Tour de 7 pueblos", 180000, 150000, "COP",
                     "20% descuento", "Lunes a Jueves", "Salida 8:00 a.m.",
                     "01/11/2025", "30/11/2025", "Aplica para grupos de 4+ personas"], 2)

# Formato moneda para precios
for row in range(2, 1000):
    ws.cell(row=row, column=3).number_format = '#,##0'
    ws.cell(row=row, column=4).number_format = '#,##0'

auto_width(ws)

# === HOJA 5: MULTIMEDIA ===
ws = wb.create_sheet("Multimedia")
headers = ["ID Multimedia*", "ID Servicio*", "Comercio*", "Tipo*", "Nombre archivo*",
           "Descripción / texto alternativo*", "Es portada", "Orden"]
ws.append(headers)
style_header(ws)

for i, h in enumerate(headers, 1):
    add_comment(ws, f"{get_column_letter(i)}1", {
        "ID Multimedia*": "Código único. Ej: img001, vid001",
        "ID Servicio*": "Debe coincidir con la hoja Servicios.",
        "Comercio*": "Debe coincidir con la hoja Comercios.",
        "Tipo*": "Foto o Video.",
        "Nombre archivo*": "Nombre exacto del archivo. Ej: tour_villa_leyva_01.jpg",
        "Descripción / texto alternativo*": "Texto que describe la imagen o video.",
        "Es portada": "Sí o No. Solo una foto puede ser portada por servicio.",
        "Orden": "Número para ordenar las imágenes."
    }.get(h, ""))

add_example_row(ws, ["img001", "srv001", "Cafetería La Casona", "Foto",
                     "tour_villa_leyva_01.jpg", "Vista panorámica de Villa de Leyva en la mañana.",
                     "Sí", 1], 2)
add_example_row(ws, ["vid001", "srv001", "Cafetería La Casona", "Video",
                     "tour_7_pueblos_reel.mp4", "Video corto de 20 segundos del recorrido.",
                     "No", 2], 3)

# Validaciones
dv_tipo = DataValidation(type="list", formula1='"Foto,Video"', allow_blank=False)
ws.add_data_validation(dv_tipo)
dv_tipo.add(f'D2:D1000')

ws.add_data_validation(dv_destacado)
dv_destacado.add(f'G2:G1000')

auto_width(ws)

# === HOJA 6: FAQs CHATBOT ===
ws = wb.create_sheet("FAQs Chatbot")
headers = ["ID FAQ*", "Comercio*", "ID Servicio", "Pregunta*", "Respuesta*",
           "Palabras clave", "Categoría de pregunta*", "Prioridad"]
ws.append(headers)
style_header(ws)

for i, h in enumerate(headers, 1):
    add_comment(ws, f"{get_column_letter(i)}1", {
        "ID FAQ*": "Código único. Ej: faq001",
        "Comercio*": "Debe coincidir con la hoja Comercios.",
        "ID Servicio": "Opcional. Si aplica a un servicio específico.",
        "Pregunta*": "Pregunta como la haría un visitante.",
        "Respuesta*": "Respuesta clara y corta.",
        "Palabras clave": "Palabras separadas por coma para ayudar al bot. Ej: horario,abre,cerrado",
        "Categoría de pregunta*": "Ej: Horario, Precio, Ubicación, Servicio, Reserva.",
        "Prioridad": "Alta, Media o Baja."
    }.get(h, ""))

add_example_row(ws, ["faq001", "Cafetería La Casona", "srv001",
                     "¿A qué hora abren?", "Abrimos de lunes a domingo de 9:00 a.m. a 8:00 p.m.",
                     "horario,abre,cerrado,hora", "Horario", "Alta"], 2)
add_example_row(ws, ["faq002", "Cafetería La Casona", "srv001",
                     "¿Cuánto cuesta el tour?", "El tour de 7 pueblos tiene un precio de $180.000 COP por persona. En noviembre tiene 20% de descuento de lunes a jueves.",
                     "precio,cuesta,valor,tour", "Precio", "Alta"], 3)

# Validaciones
dv_prioridad = DataValidation(type="list", formula1='"Alta,Media,Baja"', allow_blank=True)
ws.add_data_validation(dv_prioridad)
dv_prioridad.add(f'H2:H1000')

auto_width(ws)

# === HOJA 7: CATEGORÍAS ===
ws = wb.create_sheet("Categorías")
headers = ["Categoría*", "Descripción", "Icono (emoji o nombre)", "Orden"]
ws.append(headers)
style_header(ws)

categories = [
    ("Gastronomía", "Restaurantes, cafeterías, dulces típicos", "🍽️", 1),
    ("Hospedaje", "Hoteles, hostales, casas de campo", "🏨", 2),
    ("Artesanía", "Productos artesanales y souvenires", "🎨", 3),
    ("Bienestar", "Spa, masajes, yoga", "🧘", 4),
    ("Tour", "Recorridos y experiencias guiadas", "🚶", 5),
    ("Evento", "Actividades especiales y programaciones", "🎉", 6),
    ("Capilla", "Servicios religiosos y espirituales", "⛪", 7),
]
for r, cat in enumerate(categories, 2):
    for c, val in enumerate(cat, 1):
        ws.cell(row=r, column=c, value=val)
        ws.cell(row=r, column=c).border = thin_border

auto_width(ws)

# === HOJA 8: TAGS ===
ws = wb.create_sheet("Tags")
headers = ["Tag*", "Descripción"]
ws.append(headers)
style_header(ws)

tags = [
    ("Familiar", "Apto para toda la familia"),
    ("Romántico", "Ideal para parejas"),
    ("Artesanal", "Productos hechos a mano"),
    ("Gastronomía", "Experiencias de comida y bebida"),
    ("Bienestar", "Relajación y cuidado personal"),
    ("Cultural", "Historias y tradiciones locales"),
    ("Activo", "Recorridos y actividades físicas"),
    ("Nocturno", "Actividades en la noche"),
    ("Económico", "Buena relación precio-valor"),
    ("Premium", "Experiencia de lujo"),
]
for r, tag in enumerate(tags, 2):
    for c, val in enumerate(tag, 1):
        ws.cell(row=r, column=c, value=val)
        ws.cell(row=r, column=c).border = thin_border

auto_width(ws)

# === HOJA 9: MANZANAS ===
ws = wb.create_sheet("Manzanas")
headers = ["Manzana*", "Descripción", "Punto de referencia"]
ws.append(headers)
style_header(ws)

manzanas = [
    ("Manzana 1", "Entrada principal, cafeterías y artesanías", "Plaza principal"),
    ("Manzana 2", "Hospedajes y restaurantes", "Cerca de la capilla"),
    ("Manzana 3", "Bienestar y experiencias", "Jardín central"),
    ("Manzana 4", "Eventos y actividades culturales", "Teatro al aire libre"),
    ("Manzana 5", "Zona de restaurantes típicos", "Parqueadero norte"),
    ("Manzana 6", "Tiendas de souvenires", "Entrada sur"),
    ("Manzana 7", "Zona de descanso y cafés", "Mirador"),
]
for r, man in enumerate(manzanas, 2):
    for c, val in enumerate(man, 1):
        ws.cell(row=r, column=c, value=val)
        ws.cell(row=r, column=c).border = thin_border

auto_width(ws)

# === HOJA 10: EVENTOS ===
ws = wb.create_sheet("Eventos")
headers = ["ID Evento*", "Nombre del evento*", "Fecha inicio*", "Fecha fin*", "Lugar*",
           "Descripción*", "Servicios relacionados", "Imagen (archivo)", "Estado*"]
ws.append(headers)
style_header(ws)

for i, h in enumerate(headers, 1):
    add_comment(ws, f"{get_column_letter(i)}1", {
        "ID Evento*": "Código único. Ej: evt001",
        "Nombre del evento*": "Nombre del evento o temporada.",
        "Fecha inicio*": "DD/MM/AAAA",
        "Fecha fin*": "DD/MM/AAAA",
        "Lugar*": "Ubicación dentro del complejo.",
        "Descripción*": "Información para visitantes.",
        "Servicios relacionados": "IDs de servicios separados por coma.",
        "Imagen (archivo)": "Nombre del archivo de imagen promocional.",
        "Estado*": "Activo o Inactivo."
    }.get(h, ""))

add_example_row(ws, ["evt001", "Bazarte Navideño", "15/12/2025", "23/12/2025",
                     "Plaza principal", "Mercado navideño con artesanías, comida típica y música en vivo.",
                     "srv001", "bazarte_navidad_2025.jpg", "Activo"], 2)

ws.add_data_validation(dv_estado)
dv_estado.add(f'I2:I1000')

auto_width(ws)

# === HOJA 11: USUARIOS ADMIN ===
ws = wb.create_sheet("Usuarios Admin")
headers = ["Nombre completo*", "Correo*", "Teléfono", "Rol*", "Comercios asignados", "Estado*"]
ws.append(headers)
style_header(ws)

for i, h in enumerate(headers, 1):
    add_comment(ws, f"{get_column_letter(i)}1", {
        "Nombre completo*": "Nombre del gestor digital o administrador.",
        "Correo*": "Correo para acceder al panel.",
        "Teléfono": "Opcional.",
        "Rol*": "Administrador, Editor o Comercio.",
        "Comercios asignados": "Si el rol es Comercio, liste los comercios separados por coma.",
        "Estado*": "Activo o Inactivo."
    }.get(h, ""))

add_example_row(ws, ["Evelyn Rodríguez", "evelyn@pueblitoboyacense.org", "573001234567",
                     "Administrador", "Todos", "Activo"], 2)
add_example_row(ws, ["Juan Pérez", "juan@lacasona.com", "573009876543",
                     "Comercio", "Cafetería La Casona", "Activo"], 3)

# Validación rol
dv_rol = DataValidation(type="list", formula1='"Administrador,Editor,Comercio"', allow_blank=False)
ws.add_data_validation(dv_rol)
dv_rol.add(f'D2:D1000')

ws.add_data_validation(dv_estado)
dv_estado.add(f'F2:F1000')

auto_width(ws)

# Congelar paneles en encabezados
for ws in wb.worksheets:
    if ws.title != "Instrucciones":
        ws.freeze_panes = 'A2'

# Guardar
output_path = "Pueblito Boyacense/Contenido_Pueblito_Boyacense.xlsx"
wb.save(output_path)
print(f"Excel generado: {output_path}")
print(f"Total de hojas: {len(wb.sheetnames)}")
print("Hojas:", ", ".join(wb.sheetnames))
