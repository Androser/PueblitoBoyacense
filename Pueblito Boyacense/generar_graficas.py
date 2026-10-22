import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Configuración global
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 11

# Colores corporativos cálidos
COLOR_PRIMARIO = '#2E7D32'      # Verde bosque
COLOR_SECUNDARIO = '#F9A825'    # Amarillo/dorado
COLOR_TERCIARIO = '#D84315'     # Terracota
COLOR_NEUTRO = '#455A64'        # Gris azulado
COLOR_FONDO = '#FAFAFA'
COLOR_TEXTO = '#263238'

OUTPUT_DIR = 'Pueblito Boyacense/graficas'


def guardar(fig, nombre):
    ruta = f'{OUTPUT_DIR}/{nombre}'
    fig.savefig(ruta, dpi=150, bbox_inches='tight', facecolor=COLOR_FONDO)
    plt.close(fig)
    print(f'Guardado: {ruta}')


# ============================================================================
# 1. LÍNEA DE TIEMPO DE DESARROLLO
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 4))
ax.set_facecolor(COLOR_FONDO)
fig.patch.set_facecolor(COLOR_FONDO)

semanas = ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4']
hitos = [
    'Reunión de inicio\nEntrega de materiales\nConfiguración de cuentas',
    'Carga del catálogo\nConfiguración de Google Sheets',
    'Entrenamiento del chatbot\nIntegración de Supersona',
    'Pruebas, ajustes\nCapacitación\nEntrega operativa'
]
colores = [COLOR_PRIMARIO, COLOR_SECUNDARIO, COLOR_TERCIARIO, COLOR_PRIMARIO]

y_pos = np.zeros(len(semanas))
ax.plot(range(len(semanas)), y_pos, 'o-', color=COLOR_NEUTRO, linewidth=3, markersize=12,
        markerfacecolor=COLOR_PRIMARIO, markeredgecolor='white', markeredgewidth=2)

for i, (semana, hito, color) in enumerate(zip(semanas, hitos, colores)):
    offset = 0.25 if i % 2 == 0 else -0.25
    ax.annotate(semana, (i, 0), textcoords="offset points", xytext=(0, 20),
                ha='center', fontsize=11, fontweight='bold', color=COLOR_TEXTO)
    ax.annotate(hito, (i, 0), textcoords="offset points", xytext=(0, offset * 180),
                ha='center', fontsize=9, color=COLOR_TEXTO,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=color, linewidth=1.5))

ax.set_xlim(-0.5, len(semanas) - 0.5)
ax.set_ylim(-0.8, 0.8)
ax.axis('off')
ax.set_title('Línea de tiempo de desarrollo — Ecosistema Interactivo', fontweight='bold', color=COLOR_TEXTO, pad=20)

guardar(fig, '01_linea_tiempo_desarrollo.png')


# ============================================================================
# 2. LÍNEA DE TIEMPO DE PAGOS
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 5))
ax.set_facecolor(COLOR_FONDO)
fig.patch.set_facecolor(COLOR_FONDO)

meses = np.arange(0, 14)
pagos = [750000] + [580000] * 12 + [130000]
etiquetas = ['Pago 1\nSetup', '$580k\nmes 1', '$580k\nmes 2', '$580k\nmes 3', '$580k\nmes 4',
             '$580k\nmes 5', '$580k\nmes 6', '$580k\nmes 7', '$580k\nmes 8',
             '$580k\nmes 9', '$580k\nmes 10', '$580k\nmes 11', '$580k\nmes 12',
             '$130k\nbase']
colores_barras = [COLOR_PRIMARIO] + [COLOR_SECUNDARIO] * 12 + [COLOR_TERCIARIO]

bars = ax.bar(meses, pagos, color=colores_barras, edgecolor='white', linewidth=1.5, width=0.7)

# Línea de separación entre soporte y base
ax.axvline(x=12.5, color=COLOR_NEUTRO, linestyle='--', linewidth=2, alpha=0.7)
ax.text(12.7, max(pagos) * 0.9, 'Fin del\nsoporte anual', fontsize=9, color=COLOR_NEUTRO, ha='left')

for bar, etiqueta in zip(bars, etiquetas):
    altura = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., altura + 15000,
            etiqueta, ha='center', va='bottom', fontsize=8, color=COLOR_TEXTO)

ax.set_xticks(meses)
ax.set_xticklabels(['Firma'] + [f'M{i}' for i in range(1, 13)] + ['M13+'], fontsize=9)
ax.set_ylabel('Valor (COP)', fontweight='bold', color=COLOR_TEXTO)
ax.set_xlabel('Momento del contrato', fontweight='bold', color=COLOR_TEXTO)
ax.set_title('Línea de tiempo de pagos — Setup + 12 meses de soporte + costos base', fontweight='bold', color=COLOR_TEXTO, pad=20)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

leyenda = [
    mpatches.Patch(color=COLOR_PRIMARIO, label='Setup ($750k + $750k)'),
    mpatches.Patch(color=COLOR_SECUNDARIO, label='Mantenimiento + costos fijos ($580k/mes)'),
    mpatches.Patch(color=COLOR_TERCIARIO, label='Solo costos fijos base ($130k/mes)')
]
ax.legend(handles=leyenda, loc='upper right', frameon=True, facecolor='white')

guardar(fig, '02_linea_tiempo_pagos.png')


# ============================================================================
# 3. DIVISIÓN MENSUAL: COSTOS FIJOS VS MANTENIMIENTO
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.patch.set_facecolor(COLOR_FONDO)

# Torta
labels = ['Costos fijos\n(servidor, tokens,\nmensajes)', 'Mantenimiento y\nsoporte técnico']
sizes = [130000, 450000]
colores_torta = [COLOR_PRIMARIO, COLOR_SECUNDARIO]
explode = (0.05, 0)

ax1.set_facecolor(COLOR_FONDO)
wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, colors=colores_torta,
                                     autopct='%1.0f%%', startangle=90, textprops={'color': COLOR_TEXTO},
                                     wedgeprops={'edgecolor': 'white', 'linewidth': 2})
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(11)
ax1.set_title('División de la mensualidad\n$580.000 COP/mes', fontweight='bold', color=COLOR_TEXTO)

# Barras horizontales
ax2.set_facecolor(COLOR_FONDO)
categorias = ['Costos fijos\n$130.000', 'Mantenimiento\n$450.000']
valores = [130000, 450000]
bars = ax2.barh(categorias, valores, color=colores_torta, edgecolor='white', linewidth=2)
for bar, val in zip(bars, valores):
    ax2.text(val + 8000, bar.get_y() + bar.get_height()/2,
             f'${val/1000:.0f}k', va='center', fontweight='bold', color=COLOR_TEXTO)
ax2.set_xlim(0, 520000)
ax2.set_xlabel('Valor mensual (COP)', fontweight='bold', color=COLOR_TEXTO)
ax2.set_title('Desglose mensual', fontweight='bold', color=COLOR_TEXTO)
ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}k'))
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
guardar(fig, '03_division_mensual.png')


# ============================================================================
# 4. EVOLUCIÓN DEL COSTO MENSUAL
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor(COLOR_FONDO)
fig.patch.set_facecolor(COLOR_FONDO)

periodos = ['Meses 1-12\n(Soporte activo)', 'Mes 13 en adelante\n(Sin soporte)']
costos = [580000, 130000]
colores_evolucion = [COLOR_SECUNDARIO, COLOR_TERCIARIO]

bars = ax.bar(periodos, costos, color=colores_evolucion, edgecolor='white', linewidth=2, width=0.5)
for bar, val in zip(bars, costos):
    ax.text(bar.get_x() + bar.get_width()/2, val + 15000,
            f'${val/1000:.0f}k/mes', ha='center', va='bottom', fontweight='bold', fontsize=12, color=COLOR_TEXTO)

# Flecha de descenso
ax.annotate('', xy=(1, 160000), xytext=(0.15, 560000),
            arrowprops=dict(arrowstyle='->', color=COLOR_PRIMARIO, lw=3))
ax.text(0.5, 380000, 'Ahorro de\n$450.000/mes', ha='center', fontsize=10, color=COLOR_PRIMARIO, fontweight='bold')

ax.set_ylabel('Valor mensual (COP)', fontweight='bold', color=COLOR_TEXTO)
ax.set_title('Evolución del costo mensual después del primer año', fontweight='bold', color=COLOR_TEXTO, pad=20)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}k'))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(0, 700000)

guardar(fig, '04_evolucion_costos.png')


# ============================================================================
# 5. CUOTA DE COMERCIOS: FINANCIACIÓN DE LA MENSUALIDAD
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor(COLOR_FONDO)
fig.patch.set_facecolor(COLOR_FONDO)

escenarios = ['20 comercios\n$15k', '30 comercios\n$15k', '29 comercios\n$20k', '30 comercios\n$20k']
recaudo = [300000, 450000, 580000, 600000]
colores_cuota = [COLOR_TERCIARIO if r < 580000 else COLOR_PRIMARIO for r in recaudo]

bars = ax.bar(escenarios, recaudo, color=colores_cuota, edgecolor='white', linewidth=2, width=0.6)
for bar, val in zip(bars, recaudo):
    ax.text(bar.get_x() + bar.get_width()/2, val + 10000,
            f'${val/1000:.0f}k', ha='center', va='bottom', fontweight='bold', fontsize=10, color=COLOR_TEXTO)

# Línea de meta
ax.axhline(y=580000, color=COLOR_PRIMARIO, linestyle='--', linewidth=2, alpha=0.8)
ax.text(3.4, 600000, 'Meta: $580k', fontsize=10, color=COLOR_PRIMARIO, fontweight='bold', ha='right')

ax.set_ylabel('Recaudo mensual (COP)', fontweight='bold', color=COLOR_TEXTO)
ax.set_xlabel('Escenarios de participación de comercios', fontweight='bold', color=COLOR_TEXTO)
ax.set_title('¿Cuántos comercios se necesitan para cubrir la mensualidad?', fontweight='bold', color=COLOR_TEXTO, pad=20)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}k'))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(0, 700000)

leyenda = [
    mpatches.Patch(color=COLOR_TERCIARIO, label='No cubre la mensualidad'),
    mpatches.Patch(color=COLOR_PRIMARIO, label='Cubre o supera la mensualidad')
]
ax.legend(handles=leyenda, loc='upper left', frameon=True, facecolor='white')

guardar(fig, '05_cuota_comercios.png')


# ============================================================================
# 6. RESUMEN VISUAL DE LA INVERSIÓN TOTAL
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_facecolor(COLOR_FONDO)
fig.patch.set_facecolor(COLOR_FONDO)

conceptos = ['Setup\n(único)', 'Soporte 12 meses\n($450k x 12)', 'Costos fijos\n12 meses', 'Total primer año']
valores = [1500000, 450000 * 12, 130000 * 12, 1500000 + 450000 * 12 + 130000 * 12]
colores_resumen = [COLOR_PRIMARIO, COLOR_SECUNDARIO, COLOR_TERCIARIO, COLOR_NEUTRO]

bars = ax.bar(conceptos, valores, color=colores_resumen, edgecolor='white', linewidth=2, width=0.6)
for bar, val in zip(bars, valores):
    ax.text(bar.get_x() + bar.get_width()/2, val + 100000,
            f'${val/1e6:.2f}M', ha='center', va='bottom', fontweight='bold', fontsize=11, color=COLOR_TEXTO)

ax.set_ylabel('Valor (COP)', fontweight='bold', color=COLOR_TEXTO)
ax.set_title('Resumen de inversión total — Primer año', fontweight='bold', color=COLOR_TEXTO, pad=20)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

guardar(fig, '06_resumen_inversion.png')


print('\nTodas las gráficas fueron generadas exitosamente.')
