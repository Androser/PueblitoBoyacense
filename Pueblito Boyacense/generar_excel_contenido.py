import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, NamedStyle
from openpyxl.comments import Comment
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
from datetime import datetime

wb = openpyxl.Workbook()

# ===== PALETA INSTITUCIONAL =====
COLORS = {
    'navy': '1a365d',
    'navy_light': '2c5282',
    'gold': 'c5a028',
    'gold_light': 'fef3c7',
    'green': '2e7d32',
    'green_light': 'e8f5e9',
    'red': '991b1b',
    'red_light': 'fee2e2',
    'slate': '475569',
    'slate_light': 'f8fafc',
    'border': 'e2e8f0',
    'white': 'ffffff'
}

# ===== ESTILOS =====
header_fill = PatternFill(start_color=COLORS['navy'], end_color=COLORS['navy'], fill_type='solid')
header_font = Font(color=COLORS['white'], bold=True, size=11, name='Calibri')
subheader_fill = PatternFill(start_color=COLORS['navy_light'], end_color=COLORS['navy_light'], fill_type='solid')
subheader_font = Font(color=COLORS['white'], bold=True, size=10, name='Calibri')
example_fill = PatternFill(start_color=COLORS['gold_light'], end_color=COLORS['gold_light'], fill_type='solid')
example_font = Font(italic=True, color=COLORS['slate'], name='Calibri')
alt_row_fill = PatternFill(start_color=COLORS['slate_light'], end_color=COLORS['slate_light'], fill_type='solid')

title_font = Font(size=22, bold=True, color=COLORS['navy'], name='Calibri')
subtitle_font = Font(size=14, bold=True, color=COLORS['navy_light'], name='Calibri')
body_font = Font(size=11, color=COLORS['slate'], name='Calibri')

center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
left_align = Alignment(horizontal='left', vertical='center', wrap_text=True)

thin_border = Border(
    left=Side(style='thin', color=COLORS['border']),
    right=Side(style='thin', color=COLORS['border']),
    top=Side(style='thin', color=COLORS['border']),
    bottom=Side(style='thin', color=COLORS['border'])
)

medium_border = Border(
    left=Side(style='medium', color=COLORS['navy']),
    right=Side(style='medium', color=COLORS['navy']),
    top=Side(style='medium', color=COLORS['navy']),
    bottom=Side(style='medium', color=COLORS['navy'])
)

# ===== FUNCIONES AUXILIARES =====
def style_header(ws, row=1):
    ws.row_dimensions[row].height = 32
    for cell in ws[row]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align
        cell.border = thin_border

def add_comment(ws, cell, text):
    ws[cell].comment = Comment(text, "Asistente Pueblito Boyacense")

def auto_width(ws, min_width=14, max_width=50):
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
            adjusted = min(max(max_length + 3, min_width), max_width)
            ws.column_dimensions[column].width = adjusted

def add_example_row(ws, values, row):
    for col, val in enumerate(values, 1):
        cell = ws.cell(row=row, column=col, value=val)
        cell.fill = example_fill
        cell.font = example_font
        cell.border = thin_border
        cell.alignment = left_align

def apply_zebra_striping(ws, start_row=2, end_row=1000):
    for row in range(start_row, end_row + 1):
        if row % 2 == 0:
            for cell in ws[row]:
                if not cell.fill or cell.fill.fill_type is None:
                    cell.fill = alt_row_fill

def add_section_title(ws, row, text, cols):
    cell = ws.cell(row=row, column=1, value=text)
    cell.font = subtitle_font
    cell.fill = PatternFill(start_color=COLORS['gold_light'], end_color=COLORS['gold_light'], fill_type='solid')
    cell.alignment = left_align
    cell.border = thin_border
    end_col = get_column_letter(cols)
    ws.merge_cells(f'A{row}:{end_col}{row}')
    ws.row_dimensions[row].height = 28

# ===== HOJA PORTADA =====
ws = wb.active
ws.title = "Portada"

# Insertar imagen de Supersona
try:
    img = XLImage('Pueblito Boyacense/ImagenesGemini/muneco_supersona_original.png')
    img.width = 260
    img.height = 346
    ws.add_image(img, 'B2')
except Exception as e:
    print(f"No se pudo cargar la imagen: {e}")

ws.column_dimensions['A'].width = 4
ws.column_dimensions['B'].width = 36
ws.column_dimensions['C'].width = 70
ws.column_dimensions['D'].width = 20

ws['C4'] = "ECOSISTEMA INTERACTIVO"
ws['C4'].font = Font(size=14, bold=True, color=COLORS['gold'], name='Calibri')

ws['C5'] = "Pueblito Boyacense"
ws['C5'].font = title_font

ws['C6'] = "Plantilla de contenido para catálogo digital, chatbot y administración"
ws['C6'].font = Font(size=13, color=COLORS['slate'], name='Calibri')
ws['C6'].alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
ws.merge_cells('C6:C8')

ws['C10'] = "Instrucciones rápidas"
ws['C10'].font = subtitle_font

quick_steps = [
    "1. No modifique los nombres de las hojas ni de las columnas.",
    "2. Las celdas con * son obligatorias.",
    "3. Las filas de ejemplo están en color amarillo; bórrelas antes de entregar.",
    "4. Use el mismo nombre de comercio en todas las hojas.",
    "5. Entre más preguntas incluya en FAQs Chatbot, mejor responderá el bot.",
]
for i, step in enumerate(quick_steps, 11):
    ws.cell(row=i, column=3, value=step).font = body_font
    ws.cell(row=i, column=3).alignment = left_align

ws['C18'] = "Hojas incluidas"
ws['C18'].font = subtitle_font

sheets_info = [
    ("Comercios", "Datos generales de cada negocio"),
    ("Servicios", "Catálogo de productos y experiencias"),
    ("Precios y Ofertas", "Precios, descuentos y vigencias"),
    ("Multimedia", "Fotos y videos por servicio"),
    ("FAQs Chatbot", "Preguntas y respuestas para la IA"),
    ("Categorías", "Lista maestra de categorías"),
    ("Tags", "Etiquetas para filtros"),
    ("Manzanas", "Ubicaciones dentro del complejo"),
    ("Eventos", "Eventos y temporadas especiales"),
    ("Usuarios Admin", "Gestores del sistema"),
]

for i, (sheet, desc) in enumerate(sheets_info, 19):
    ws.cell(row=i, column=3, value=sheet).font = Font(bold=True, size=11, color=COLORS['navy'], name='Calibri')
    ws.cell(row=i, column=4, value=desc).font = body_font

ws['C31'] = f"Generado el {datetime.now().strftime('%d/%m/%Y')}"
ws['C31'].font = Font(size=10, italic=True, color=COLORS['slate'], name='Calibri')

# ===== HOJA INSTRUCCIONES =====
ws = wb.create_sheet("Instrucciones")
ws['B2'] = "Guía detallada para llenar el contenido"
ws['B2'].font = subtitle_font

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

for r, row_data in enumerate(instructions, 4):
    for c, val in enumerate(row_data, 2):
        cell = ws.cell(row=r, column=c, value=val)
        if r == 4:
            cell.fill = subheader_fill
            cell.font = subheader_font
        else:
            cell.fill = PatternFill(start_color=COLORS['white'], end_color=COLORS['white'], fill_type='solid')
            cell.font = body_font
        cell.border = thin_border
        cell.alignment = left_align

ws.column_dimensions['B'].width = 22
ws.column_dimensions['C'].width = 50
ws.column_dimensions['D'].width = 32
ws.column_dimensions['E'].width = 16

ws['B17'] = "Reglas generales"
ws['B17'].font = subtitle_font

rules = [
    "1. No modificar los nombres de las hojas ni de las columnas (son usadas por el sistema).",
    "2. Las filas de ejemplo están en color amarillo claro; bórralas antes de entregar el archivo final.",
    "3. Los campos marcados con * son obligatorios.",
    "4. Para fotos y videos, escriba el nombre exacto del archivo (ej: cafeteria_la_casona_fachada.jpg).",
    "5. Para el chatbot, mientras más preguntas y respuestas incluya, mejor atenderá el bot.",
    "6. Use el mismo nombre de comercio en todas las hojas para que el sistema los relacione.",
    "7. Los estados 'Activo' e 'Inactivo' se marcan automáticamente con colores verde y rojo.",
]
for i, rule in enumerate(rules, 18):
    cell = ws.cell(row=i, column=2, value=rule)
    cell.font = body_font
    cell.alignment = left_align

# ===== COMERCIOS =====
ws = wb.create_sheet("Comercios")
headers = ["ID Comercio*", "Nombre del comercio*", "Categoría principal*", "Manzana / Ubicación*",
           "Nombre del responsable", "Teléfono WhatsApp*", "Teléfono llamada", "Correo electrónico",
           "Horario de atención*", "Descripción general", "Logo (archivo)", "Estado*"]
ws.append(headers)
style_header(ws)

comments = {
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
}
for i, h in enumerate(headers, 1):
    add_comment(ws, f"{get_column_letter(i)}1", comments.get(h, ""))

add_example_row(ws, ["casona01", "Cafetería La Casona", "Gastronomía", "Manzana 1",
                     "María Gómez", "573001234567", "6011234567", "lacasona@email.com",
                     "Lun-Dom 9am-8pm", "Café de origen boyacense con postres artesanales.",
                     "logo_casona.png", "Activo"], 2)

apply_zebra_striping(ws)

# Validación estado
dv_estado = DataValidation(type="list", formula1='"Activo,Inactivo"', allow_blank=False)
ws.add_data_validation(dv_estado)
dv_estado.add('L2:L1000')

# Formato condicional estado
ws.conditional_formatting.add('L2:L1000', CellIsRule(operator='equal', formula=['"Activo"'], fill=PatternFill(start_color=COLORS['green_light'], end_color=COLORS['green_light'], fill_type='solid')))
ws.conditional_formatting.add('L2:L1000', CellIsRule(operator='equal', formula=['"Inactivo"'], fill=PatternFill(start_color=COLORS['red_light'], end_color=COLORS['red_light'], fill_type='solid')))

auto_width(ws)

# ===== SERVICIOS =====
ws = wb.create_sheet("Servicios")
headers = ["ID Servicio*", "Nombre del servicio*", "Comercio*", "Categoría*", "Manzana / Ubicación*",
           "Descripción corta*", "Descripción larga", "Incluye", "No incluye", "Duración / Capacidad",
           "Tags", "Destacado", "Estado*"]
ws.append(headers)
style_header(ws)

comments = {
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
}
for i, h in enumerate(headers, 1):
    add_comment(ws, f"{get_column_letter(i)}1", comments.get(h, ""))

add_example_row(ws, ["srv001", "Tour de 7 pueblos", "Cafetería La Casona", "Tour",
                     "Manzana 1", "Recorrido guiado por Villa de Leyva, Tibasosa, Tenza y más.",
                     "Experiencia completa de un día con guía certificado, almuerzo típico y transporte.",
                     "Almuerzo, guía, transporte", "Propinas, souvenirs", "8 horas, máx 15 pers",
                     "Familiar,Cultural,Activo", "Sí", "Activo"], 2)

apply_zebra_striping(ws)

# Validaciones
dv_destacado = DataValidation(type="list", formula1='"Sí,No"', allow_blank=True)
ws.add_data_validation(dv_destacado)
dv_destacado.add('L2:L1000')

ws.add_data_validation(dv_estado)
dv_estado.add('M2:M1000')

ws.conditional_formatting.add('M2:M1000', CellIsRule(operator='equal', formula=['"Activo"'], fill=PatternFill(start_color=COLORS['green_light'], end_color=COLORS['green_light'], fill_type='solid')))
ws.conditional_formatting.add('M2:M1000', CellIsRule(operator='equal', formula=['"Inactivo"'], fill=PatternFill(start_color=COLORS['red_light'], end_color=COLORS['red_light'], fill_type='solid')))

auto_width(ws)

# ===== PRECIOS Y OFERTAS =====
ws = wb.create_sheet("Precios y Ofertas")
headers = ["ID Servicio*", "Nombre del servicio*", "Precio normal*", "Precio oferta",
           "Moneda*", "Tipo de oferta", "Días aplicables", "Horario aplicable",
           "Vigencia desde", "Vigencia hasta", "Notas"]
ws.append(headers)
style_header(ws)

comments = {
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
}
for i, h in enumerate(headers, 1):
    add_comment(ws, f"{get_column_letter(i)}1", comments.get(h, ""))

add_example_row(ws, ["srv001", "Tour de 7 pueblos", 180000, 150000, "COP",
                     "20% descuento", "Lunes a Jueves", "Salida 8:00 a.m.",
                     "01/11/2025", "30/11/2025", "Aplica para grupos de 4+ personas"], 2)

apply_zebra_striping(ws)

# Formato moneda para precios
for row in range(2, 1000):
    ws.cell(row=row, column=3).number_format = '$#,##0'
    ws.cell(row=row, column=4).number_format = '$#,##0'

auto_width(ws)

# ===== MULTIMEDIA =====
ws = wb.create_sheet("Multimedia")
headers = ["ID Multimedia*", "ID Servicio*", "Comercio*", "Tipo*", "Nombre archivo*",
           "Descripción / texto alternativo*", "Es portada", "Orden"]
ws.append(headers)
style_header(ws)

comments = {
    "ID Multimedia*": "Código único. Ej: img001, vid001",
    "ID Servicio*": "Debe coincidir con la hoja Servicios.",
    "Comercio*": "Debe coincidir con la hoja Comercios.",
    "Tipo*": "Foto o Video.",
    "Nombre archivo*": "Nombre exacto del archivo. Ej: tour_villa_leyva_01.jpg",
    "Descripción / texto alternativo*": "Texto que describe la imagen o video.",
    "Es portada": "Sí o No. Solo una foto puede ser portada por servicio.",
    "Orden": "Número para ordenar las imágenes."
}
for i, h in enumerate(headers, 1):
    add_comment(ws, f"{get_column_letter(i)}1", comments.get(h, ""))

add_example_row(ws, ["img001", "srv001", "Cafetería La Casona", "Foto",
                     "tour_villa_leyva_01.jpg", "Vista panorámica de Villa de Leyva en la mañana.",
                     "Sí", 1], 2)
add_example_row(ws, ["vid001", "srv001", "Cafetería La Casona", "Video",
                     "tour_7_pueblos_reel.mp4", "Video corto de 20 segundos del recorrido.",
                     "No", 2], 3)

apply_zebra_striping(ws)

# Validaciones
dv_tipo = DataValidation(type="list", formula1='"Foto,Video"', allow_blank=False)
ws.add_data_validation(dv_tipo)
dv_tipo.add('D2:D1000')

ws.add_data_validation(dv_destacado)
dv_destacado.add('G2:G1000')

auto_width(ws)

# ===== FAQs CHATBOT =====
ws = wb.create_sheet("FAQs Chatbot")
headers = ["ID FAQ*", "Comercio*", "ID Servicio", "Pregunta*", "Respuesta*",
           "Palabras clave", "Categoría de pregunta*", "Prioridad"]
ws.append(headers)
style_header(ws)

comments = {
    "ID FAQ*": "Código único. Ej: faq001",
    "Comercio*": "Debe coincidir con la hoja Comercios.",
    "ID Servicio": "Opcional. Si aplica a un servicio específico.",
    "Pregunta*": "Pregunta como la haría un visitante.",
    "Respuesta*": "Respuesta clara y corta.",
    "Palabras clave": "Palabras separadas por coma para ayudar al bot. Ej: horario,abre,cerrado",
    "Categoría de pregunta*": "Ej: Horario, Precio, Ubicación, Servicio, Reserva.",
    "Prioridad": "Alta, Media o Baja."
}
for i, h in enumerate(headers, 1):
    add_comment(ws, f"{get_column_letter(i)}1", comments.get(h, ""))

add_example_row(ws, ["faq001", "Cafetería La Casona", "srv001",
                     "¿A qué hora abren?", "Abrimos de lunes a domingo de 9:00 a.m. a 8:00 p.m.",
                     "horario,abre,cerrado,hora", "Horario", "Alta"], 2)
add_example_row(ws, ["faq002", "Cafetería La Casona", "srv001",
                     "¿Cuánto cuesta el tour?", "El tour de 7 pueblos tiene un precio de $180.000 COP por persona. En noviembre tiene 20% de descuento de lunes a jueves.",
                     "precio,cuesta,valor,tour", "Precio", "Alta"], 3)

apply_zebra_striping(ws)

# Validaciones
dv_prioridad = DataValidation(type="list", formula1='"Alta,Media,Baja"', allow_blank=True)
ws.add_data_validation(dv_prioridad)
dv_prioridad.add('H2:H1000')

auto_width(ws)

# ===== CATEGORÍAS =====
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
        cell = ws.cell(row=r, column=c, value=val)
        cell.border = thin_border
        cell.font = body_font
        cell.alignment = left_align
        if r % 2 == 0:
            cell.fill = alt_row_fill

auto_width(ws)

# ===== TAGS =====
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
        cell = ws.cell(row=r, column=c, value=val)
        cell.border = thin_border
        cell.font = body_font
        cell.alignment = left_align
        if r % 2 == 0:
            cell.fill = alt_row_fill

auto_width(ws)

# ===== MANZANAS =====
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
        cell = ws.cell(row=r, column=c, value=val)
        cell.border = thin_border
        cell.font = body_font
        cell.alignment = left_align
        if r % 2 == 0:
            cell.fill = alt_row_fill

auto_width(ws)

# ===== EVENTOS =====
ws = wb.create_sheet("Eventos")
headers = ["ID Evento*", "Nombre del evento*", "Fecha inicio*", "Fecha fin*", "Lugar*",
           "Descripción*", "Servicios relacionados", "Imagen (archivo)", "Estado*"]
ws.append(headers)
style_header(ws)

comments = {
    "ID Evento*": "Código único. Ej: evt001",
    "Nombre del evento*": "Nombre del evento o temporada.",
    "Fecha inicio*": "DD/MM/AAAA",
    "Fecha fin*": "DD/MM/AAAA",
    "Lugar*": "Ubicación dentro del complejo.",
    "Descripción*": "Información para visitantes.",
    "Servicios relacionados": "IDs de servicios separados por coma.",
    "Imagen (archivo)": "Nombre del archivo de imagen promocional.",
    "Estado*": "Activo o Inactivo."
}
for i, h in enumerate(headers, 1):
    add_comment(ws, f"{get_column_letter(i)}1", comments.get(h, ""))

add_example_row(ws, ["evt001", "Bazarte Navideño", "15/12/2025", "23/12/2025",
                     "Plaza principal", "Mercado navideño con artesanías, comida típica y música en vivo.",
                     "srv001", "bazarte_navidad_2025.jpg", "Activo"], 2)

apply_zebra_striping(ws)

ws.add_data_validation(dv_estado)
dv_estado.add('I2:I1000')

ws.conditional_formatting.add('I2:I1000', CellIsRule(operator='equal', formula=['"Activo"'], fill=PatternFill(start_color=COLORS['green_light'], end_color=COLORS['green_light'], fill_type='solid')))
ws.conditional_formatting.add('I2:I1000', CellIsRule(operator='equal', formula=['"Inactivo"'], fill=PatternFill(start_color=COLORS['red_light'], end_color=COLORS['red_light'], fill_type='solid')))

auto_width(ws)

# ===== USUARIOS ADMIN =====
ws = wb.create_sheet("Usuarios Admin")
headers = ["Nombre completo*", "Correo*", "Teléfono", "Rol*", "Comercios asignados", "Estado*"]
ws.append(headers)
style_header(ws)

comments = {
    "Nombre completo*": "Nombre del gestor digital o administrador.",
    "Correo*": "Correo para acceder al panel.",
    "Teléfono": "Opcional.",
    "Rol*": "Administrador, Editor o Comercio.",
    "Comercios asignados": "Si el rol es Comercio, liste los comercios separados por coma.",
    "Estado*": "Activo o Inactivo."
}
for i, h in enumerate(headers, 1):
    add_comment(ws, f"{get_column_letter(i)}1", comments.get(h, ""))

add_example_row(ws, ["Evelyn Rodríguez", "evelyn@pueblitoboyacense.org", "573001234567",
                     "Administrador", "Todos", "Activo"], 2)
add_example_row(ws, ["Juan Pérez", "juan@lacasona.com", "573009876543",
                     "Comercio", "Cafetería La Casona", "Activo"], 3)

apply_zebra_striping(ws)

# Validación rol
dv_rol = DataValidation(type="list", formula1='"Administrador,Editor,Comercio"', allow_blank=False)
ws.add_data_validation(dv_rol)
dv_rol.add('D2:D1000')

ws.add_data_validation(dv_estado)
dv_estado.add('F2:F1000')

ws.conditional_formatting.add('F2:F1000', CellIsRule(operator='equal', formula=['"Activo"'], fill=PatternFill(start_color=COLORS['green_light'], end_color=COLORS['green_light'], fill_type='solid')))
ws.conditional_formatting.add('F2:F1000', CellIsRule(operator='equal', formula=['"Inactivo"'], fill=PatternFill(start_color=COLORS['red_light'], end_color=COLORS['red_light'], fill_type='solid')))

auto_width(ws)

# ===== AJUSTES FINALES =====
for ws in wb.worksheets:
    if ws.title not in ["Portada", "Instrucciones"]:
        ws.freeze_panes = 'A2'
        ws.sheet_view.showGridLines = False

# Guardar
output_path = "Pueblito Boyacense/Contenido_Pueblito_Boyacense.xlsx"
wb.save(output_path)
print(f"Excel generado: {output_path}")
print(f"Total de hojas: {len(wb.sheetnames)}")
print("Hojas:", ", ".join(wb.sheetnames))
