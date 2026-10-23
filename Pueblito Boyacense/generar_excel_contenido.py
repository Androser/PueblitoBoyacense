import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
from datetime import datetime

wb = openpyxl.Workbook()

# ===== COLORES =====
NAVY = '1a365d'
NAVY_LIGHT = '2c5282'
GOLD = 'c5a028'
GOLD_LIGHT = 'fef3c7'
GREEN_LIGHT = 'e8f5e9'
RED_LIGHT = 'fee2e2'
SLATE = '475569'
SLATE_LIGHT = 'f8fafc'
BORDER = 'e2e8f0'

# ===== ESTILOS =====
header_fill = PatternFill(start_color=NAVY, end_color=NAVY, fill_type='solid')
header_font = Font(color='FFFFFF', bold=True, size=12, name='Calibri')
example_fill = PatternFill(start_color=GOLD_LIGHT, end_color=GOLD_LIGHT, fill_type='solid')
example_font = Font(italic=True, color=SLATE, name='Calibri')
alt_fill = PatternFill(start_color=SLATE_LIGHT, end_color=SLATE_LIGHT, fill_type='solid')
title_font = Font(size=24, bold=True, color=NAVY, name='Calibri')
subtitle_font = Font(size=14, bold=True, color=NAVY_LIGHT, name='Calibri')
body_font = Font(size=11, color=SLATE, name='Calibri')
small_font = Font(size=10, color=SLATE, name='Calibri')
center = Alignment(horizontal='center', vertical='center', wrap_text=True)
left = Alignment(horizontal='left', vertical='center', wrap_text=True)
border = Border(
    left=Side(style='thin', color=BORDER),
    right=Side(style='thin', color=BORDER),
    top=Side(style='thin', color=BORDER),
    bottom=Side(style='thin', color=BORDER)
)

# ===== AYUDAS =====
def header(ws):
    ws.row_dimensions[1].height = 36
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center
        cell.border = border

def comment(ws, cell, text):
    ws[cell].comment = Comment(text, "Asistente")

def example(ws, values, row):
    for col, val in enumerate(values, 1):
        c = ws.cell(row=row, column=col, value=val)
        c.fill = example_fill
        c.font = example_font
        c.border = border
        c.alignment = left

def zebra(ws, end=1000):
    for row in range(2, end + 1):
        if row % 2 == 0:
            for cell in ws[row]:
                if not cell.fill or cell.fill.fill_type is None:
                    cell.fill = alt_fill

def width(ws, min_w=18, max_w=60):
    for col in ws.columns:
        max_len = 0
        col_letter = None
        for cell in col:
            if col_letter is None and hasattr(cell, 'column_letter'):
                col_letter = cell.column_letter
            try:
                length = len(str(cell.value)) if cell.value else 0
                if length > max_len:
                    max_len = length
            except:
                pass
        if col_letter:
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, min_w), max_w)

def estado_validation(ws, rango):
    dv = DataValidation(type="list", formula1='"Activo,Inactivo"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(rango)
    ws.conditional_formatting.add(rango, CellIsRule(operator='equal', formula=['"Activo"'], fill=PatternFill(start_color=GREEN_LIGHT, end_color=GREEN_LIGHT, fill_type='solid')))
    ws.conditional_formatting.add(rango, CellIsRule(operator='equal', formula=['"Inactivo"'], fill=PatternFill(start_color=RED_LIGHT, end_color=RED_LIGHT, fill_type='solid')))

# ===== PORTADA =====
ws = wb.active
ws.title = "Portada"

try:
    img = XLImage('Pueblito Boyacense/ImagenesGemini/muneco_supersona_original.png')
    img.width = 200
    img.height = 267
    ws.add_image(img, 'B3')
except Exception as e:
    print(f"Imagen no cargada: {e}")

ws.column_dimensions['A'].width = 4
ws.column_dimensions['B'].width = 28
ws.column_dimensions['C'].width = 78

ws['C4'] = "ECOSISTEMA INTERACTIVO"
ws['C4'].font = Font(size=14, bold=True, color=GOLD, name='Calibri')
ws['C5'] = "Pueblito Boyacense"
ws['C5'].font = title_font
ws['C6'] = "Formulario sencillo para cargar comercios y servicios al catálogo digital"
ws['C6'].font = Font(size=13, color=SLATE, name='Calibri')
ws['C6'].alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
ws.merge_cells('C6:C8')

ws['C10'] = "Solo 3 pasos"
ws['C10'].font = subtitle_font
steps = [
    "1. Llene la hoja 'Mis Servicios' — una fila por cada servicio o producto.",
    "2. Si quiere que el chatbot responda preguntas, llene 'Preguntas Chatbot'.",
    "3. Revise las listas de 'Categorías y Manzanas' y ajústelas si es necesario.",
]
for i, s in enumerate(steps, 11):
    ws.cell(row=i, column=3, value=s).font = body_font
    ws.cell(row=i, column=3).alignment = left

ws['C16'] = "Consejos rápidos"
ws['C16'].font = subtitle_font
tips = [
    "• Las filas amarillas son ejemplos; bórrelas y escriba sus datos.",
    "• Los campos con * son obligatorios.",
    "• Use el mismo nombre de comercio cuando tenga varios servicios.",
    "• Para fotos, escriba el nombre exacto del archivo. Ej: cafe_latte.jpg",
]
for i, t in enumerate(tips, 17):
    ws.cell(row=i, column=3, value=t).font = small_font
    ws.cell(row=i, column=3).alignment = left

ws['C23'] = f"Generado el {datetime.now().strftime('%d/%m/%Y')}"
ws['C23'].font = Font(size=10, italic=True, color=SLATE, name='Calibri')

# ===== MIS SERVICIOS =====
ws = wb.create_sheet("Mis Servicios")
headers = [
    "Nombre del comercio*",
    "WhatsApp*",
    "Categoría*",
    "Manzana*",
    "Horario*",
    "Nombre del servicio*",
    "Descripción del servicio*",
    "Precio*",
    "Moneda*",
    "Foto principal*",
    "Más fotos o videos",
    "Tags",
    "Estado*"
]
ws.append(headers)
header(ws)

comentarios = {
    "Nombre del comercio*": "Nombre como aparecerá en el catálogo.",
    "WhatsApp*": "Número con código de país. Ej: 573001234567",
    "Categoría*": "Elija de la lista.",
    "Manzana*": "Elija de la lista.",
    "Horario*": "Ej: Lun-Dom 9am-8pm",
    "Nombre del servicio*": "Ej: Tour de 7 pueblos, Menú ejecutivo, Habitación doble.",
    "Descripción del servicio*": "Qué incluye el servicio, en 1 o 2 líneas.",
    "Precio*": "Solo números. Ej: 180000",
    "Moneda*": "COP o USD.",
    "Foto principal*": "Nombre del archivo. Ej: tour_7_pueblos.jpg",
    "Más fotos o videos": "Nombres separados por coma. Opcional.",
    "Tags": "Separados por coma. Ej: Familiar,Cultural,Activo",
    "Estado*": "Activo o Inactivo."
}
for i, h in enumerate(headers, 1):
    comment(ws, f"{get_column_letter(i)}1", comentarios.get(h, ""))

example(ws, [
    "Cafetería La Casona", "573001234567", "Gastronomía", "Manzana 1", "Lun-Dom 9am-8pm",
    "Tour de 7 pueblos", "Recorrido guiado de un día con almuerzo típico y transporte.",
    180000, "COP", "tour_7_pueblos.jpg", "tour_villa_leyva.jpg,tour_reel.mp4",
    "Familiar,Cultural,Activo", "Activo"
], 2)

example(ws, [
    "Cafetería La Casona", "573001234567", "Gastronomía", "Manzana 1", "Lun-Dom 9am-8pm",
    "Menú ejecutivo", "Sopa, plato fuerte y bebida. Incluye café de origen.",
    25000, "COP", "menu_ejecutivo.jpg", "",
    "Económico,Familiar", "Activo"
], 3)

example(ws, [
    "Hotel Villa de Leyva", "573009876543", "Hospedaje", "Manzana 2", "24 horas",
    "Habitación doble", "Habitación con cama doble, baño privado y desayuno incluido.",
    280000, "COP", "habitacion_doble.jpg", "habitacion_bano.jpg,hotel_reel.mp4",
    "Romántico,Premium", "Activo"
], 4)

zebra(ws)

# Validaciones
dv_cats = DataValidation(type="list", formula1="'Categorías y Manzanas'!$A$2:$A$20", allow_blank=False)
ws.add_data_validation(dv_cats)
dv_cats.add('C2:C1000')

dv_manz = DataValidation(type="list", formula1="'Categorías y Manzanas'!$C$2:$C$20", allow_blank=False)
ws.add_data_validation(dv_manz)
dv_manz.add('D2:D1000')

dv_moneda = DataValidation(type="list", formula1='"COP,USD"', allow_blank=False)
ws.add_data_validation(dv_moneda)
dv_moneda.add('I2:I1000')

estado_validation(ws, 'M2:M1000')

# Formato moneda
for row in range(2, 1000):
    ws.cell(row=row, column=8).number_format = '$#,##0'

width(ws)

# ===== PREGUNTAS CHATBOT =====
ws = wb.create_sheet("Preguntas Chatbot")
headers = ["Comercio*", "Pregunta*", "Respuesta*"]
ws.append(headers)
header(ws)

comment(ws, "A1", "Nombre del comercio. Use 'General' si aplica a todo el Pueblito.")
comment(ws, "B1", "Pregunta como la haría un visitante.")
comment(ws, "C1", "Respuesta clara y corta.")

example(ws, ["Cafetería La Casona", "¿A qué hora abren?", "Abrimos todos los días de 9:00 a.m. a 8:00 p.m."], 2)
example(ws, ["Cafetería La Casona", "¿Cuánto cuesta el tour?", "El tour cuesta $180.000 COP por persona."], 3)
example(ws, ["Hotel Villa de Leyva", "¿Incluyen desayuno?", "Sí, el desayuno está incluido en todas las habitaciones."], 4)
example(ws, ["General", "¿Dónde queda el Pueblito Boyacense?", "Estamos en la entrada norte de Duitama, Boyacá."], 5)

zebra(ws)
width(ws)

# ===== CATEGORÍAS Y MANZANAS =====
ws = wb.create_sheet("Categorías y Manzanas")
ws['A1'] = "Categorías"
ws['A1'].font = subtitle_font
cats = ["Gastronomía", "Hospedaje", "Artesanía", "Bienestar", "Tour", "Evento", "Capilla"]
for i, c in enumerate(cats, 2):
    ws.cell(row=i, column=1, value=c).font = body_font

ws['C1'] = "Manzanas"
ws['C1'].font = subtitle_font
manz = ["Manzana 1", "Manzana 2", "Manzana 3", "Manzana 4", "Manzana 5", "Manzana 6", "Manzana 7"]
for i, m in enumerate(manz, 2):
    ws.cell(row=i, column=3, value=m).font = body_font

ws['E1'] = "Tags sugeridos"
ws['E1'].font = subtitle_font
tags = ["Familiar", "Romántico", "Artesanal", "Cultural", "Activo", "Nocturno", "Económico", "Premium"]
for i, t in enumerate(tags, 2):
    ws.cell(row=i, column=5, value=t).font = body_font

for col in ['A', 'C', 'E']:
    ws.column_dimensions[col].width = 22

# ===== AJUSTES FINALES =====
for ws in wb.worksheets:
    if ws.title != "Portada":
        ws.freeze_panes = 'A2'
        ws.sheet_view.showGridLines = False

output_path = "Pueblito Boyacense/Contenido_Pueblito_Boyacense_simple.xlsx"
wb.save(output_path)
print(f"Excel generado: {output_path}")
print(f"Total de hojas: {len(wb.sheetnames)}")
print("Hojas:", ", ".join(wb.sheetnames))
