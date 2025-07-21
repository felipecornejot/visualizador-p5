import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO
import requests

# --- Paleta de Colores ---
# Definición de colores en formato RGB (0-1) para Matplotlib
color_primario_1_rgb = (14/255, 69/255, 74/255) # 0E454A (Oscuro)
color_primario_2_rgb = (31/255, 255/255, 95/255) # 1FFF5F (Verde vibrante)
color_primario_3_rgb = (255/255, 255/255, 255/255) # FFFFFF (Blanco)

# Colores del logo de Sustrend para complementar
color_sustrend_1_rgb = (0/255, 155/255, 211/255) # 009BD3 (Azul claro)
color_sustrend_2_rgb = (0/255, 140/255, 207/255) # 008CCF (Azul medio)
color_sustrend_3_rgb = (0/255, 54/255, 110/255) # 00366E (Azul oscuro)

# Selección de colores para los gráficos
colors_for_charts = [color_primario_1_rgb, color_primario_2_rgb, color_sustrend_1_rgb, color_sustrend_3_rgb]

# --- Configuración de la página de Streamlit ---
st.set_page_config(layout="wide")

st.title('✨ Visualizador de Impactos - Proyecto P5')
st.subheader('Insect Based Food: Producción de proteína alternativa a partir de insectos')
st.markdown("""
    Ajusta los parámetros para explorar cómo las proyecciones de impacto ambiental y económico del proyecto
    varían con diferentes escenarios de volumen de residuos procesados, tasa de aprovechamiento, y factores de GEI.
""")

# --- 1. Widgets Interactivos para Parámetros (Streamlit) ---
st.sidebar.header('Parámetros de Simulación')

residuos_procesados = st.sidebar.slider(
    'Residuos Orgánicos Procesados (ton/año):',
    min_value=5,
    max_value=100,
    value=15,
    step=5,
    help="Volumen anual de residuos orgánicos procesados para la producción de proteína de insectos."
)

tasa_aprovechamiento = st.sidebar.slider(
    'Tasa de Aprovechamiento (%):',
    min_value=0.5,
    max_value=0.9,
    value=0.8,
    step=0.05,
    format='%.1f%%',
    help="Porcentaje de residuos orgánicos que se convierten efectivamente en proteína valorizada."
)

factor_gei_relleno = st.sidebar.slider(
    'Factor GEI Relleno Sanitario (tCO₂e/ton):',
    min_value=0.4,
    max_value=0.6,
    value=0.52,
    step=0.01,
    help="Emisiones de GEI evitadas por tonelada de residuo desviado de relleno sanitario."
)

factor_gei_sustitucion = st.sidebar.slider(
    'Factor GEI Sustitución Proteína (tCO₂e/ton):',
    min_value=1.5,
    max_value=2.5,
    value=2.0,
    step=0.1,
    help="Emisiones de GEI evitadas por tonelada de proteína convencional sustituida (carne o soya)."
)

precio_proteina = st.sidebar.slider(
    'Precio Proteína Equivalente (USD/ton):',
    min_value=1000,
    max_value=5000,
    value=2000,
    step=100,
    help="Precio de mercado de la proteína convencional que es sustituida por la proteína de insectos."
)

# --- 2. Cálculos de Indicadores ---
residuos_valorizados = residuos_procesados * tasa_aprovechamiento
gei_ev_relleno = residuos_procesados * factor_gei_relleno
gei_ev_sustitucion = residuos_valorizados * factor_gei_sustitucion
ingresos_estimados = residuos_valorizados * precio_proteina
empleos_generados = 2 # Valor fijo según la ficha
interacciones_cadena = 3 # Valor fijo según la ficha

st.header('Resultados Proyectados Anuales:')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="♻️ **Residuos Orgánicos Valorizados**", value=f"{residuos_valorizados:.2f} ton/año")
    st.caption("Volumen de residuos transformados en productos de valor.")
with col2:
    st.metric(label="🌎 **GEI Evitados (Relleno Sanitario)**", value=f"{gei_ev_relleno:.2f} tCO₂e/año")
    st.caption("Reducción de emisiones por desvío de residuos de rellenos sanitarios.")
with col3:
    st.metric(label="🌱 **GEI Evitados (Sustitución Proteína)**", value=f"{gei_ev_sustitucion:.2f} tCO₂e/año")
    st.caption("Reducción de emisiones por reemplazo de proteínas convencionales de alto impacto.")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(label="💰 **Ingresos Estimados**", value=f"USD {ingresos_estimados:,.2f}")
    st.caption("Ingresos potenciales por la comercialización de la proteína de insectos.")
with col5:
    st.metric(label="👨‍👩‍👧‍👦 **Empleos Generados**", value=f"{empleos_generados}")
    st.caption("Estimación de empleos directos generados por el proyecto.")
with col6:
    st.metric(label="🤝 **Interacciones en Cadena de Suministro**", value=f"{interacciones_cadena}")
    st.caption("Número de alianzas y colaboraciones en la cadena de valor circular.")

st.markdown("---")

st.header('📊 Análisis Gráfico de Impactos')

# --- Visualización (Gráficos 2D con Matplotlib) ---
# Datos línea base (según ficha P5)
# Para este proyecto, la ficha no especifica una "línea base" en el sentido de un valor histórico de EVITACIÓN.
# Por lo tanto, para los GEI evitados y residuos valorizados, la "Línea Base" sin el proyecto es 0.
# Los ingresos base se establecen en un valor de ejemplo bajo si no se valorizan los residuos.
base_residuos = 0 # Asumimos 0 residuos valorizados sin el proyecto
base_gei_relleno = 0 # Asumimos 0 GEI evitados sin el proyecto
base_gei_sustitucion = 0 # Asumimos 0 GEI evitados sin el proyecto
base_ingresos = 0 # Asumimos 0 ingresos por valorización sin el proyecto

# Creamos una figura con 3 subplots (2D)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 7), facecolor=color_primario_3_rgb)
fig.patch.set_facecolor(color_primario_3_rgb)

# Definición de etiquetas y valores para los gráficos de barras 2D
labels = ['Línea Base', 'Proyección']
bar_width = 0.6
x = np.arange(len(labels))

# --- Gráfico 1: GEI Evitados Total (tCO₂e/año) ---
gei_total_proyeccion = gei_ev_relleno + gei_ev_sustitucion
gei_values = [base_gei_relleno + base_gei_sustitucion, gei_total_proyeccion]
bars1 = ax1.bar(x, gei_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax1.set_ylabel('tCO₂e/año', fontsize=12, color=colors_for_charts[3])
ax1.set_title('GEI Evitados Total', fontsize=14, color=colors_for_charts[3], pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax1.yaxis.set_tick_params(colors=colors_for_charts[0])
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.tick_params(axis='x', length=0)
max_gei_val = max(gei_values)
ax1.set_ylim(bottom=0, top=max(max_gei_val * 1.15, 1))
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])

# --- Gráfico 2: Residuos Valorizados (ton/año) ---
residuos_values = [base_residuos, residuos_valorizados]
bars2 = ax2.bar(x, residuos_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax2.set_ylabel('Toneladas/año', fontsize=12, color=colors_for_charts[0])
ax2.set_title('Residuos Orgánicos Valorizados', fontsize=14, color=colors_for_charts[3], pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax2.yaxis.set_tick_params(colors=colors_for_charts[0])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.tick_params(axis='x', length=0)
max_residuos_val = max(residuos_values)
ax2.set_ylim(bottom=0, top=max(max_residuos_val * 1.15, 1))
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])

# --- Gráfico 3: Ingresos Estimados (USD/año) ---
ingresos_values = [base_ingresos, ingresos_estimados]
bars3 = ax3.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax3.set_ylabel('USD/año', fontsize=12, color=colors_for_charts[3])
ax3.set_title('Ingresos Estimados', fontsize=14, color=colors_for_charts[3], pad=20)
ax3.set_xticks(x)
ax3.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax3.yaxis.set_tick_params(colors=colors_for_charts[0])
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.tick_params(axis='x', length=0)
max_ingresos_val = max(ingresos_values)
ax3.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 1000))
for bar in bars3:
    yval = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"${yval:,.0f}", ha='center', va='bottom', color=colors_for_charts[0])

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
st.pyplot(fig)

# --- Funcionalidad de descarga de cada gráfico ---
st.markdown("---")
st.subheader("Descargar Gráficos Individualmente")

# Función auxiliar para generar el botón de descarga
def download_button(fig, filename_prefix, key):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    st.download_button(
        label=f"Descargar {filename_prefix}.png",
        data=buf.getvalue(),
        file_name=f"{filename_prefix}.png",
        mime="image/png",
        key=key
    )

# Crear figuras individuales para cada gráfico para poder descargarlas
# Figura 1: GEI Evitados Total
fig_gei_total, ax_gei_total = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_gei_total.bar(x, gei_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax_gei_total.set_ylabel('tCO₂e/año', fontsize=12, color=colors_for_charts[3])
ax_gei_total.set_title('GEI Evitados Total', fontsize=14, color=colors_for_charts[3], pad=20)
ax_gei_total.set_xticks(x)
ax_gei_total.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_gei_total.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_gei_total.spines['top'].set_visible(False)
ax_gei_total.spines['right'].set_visible(False)
ax_gei_total.tick_params(axis='x', length=0)
ax_gei_total.set_ylim(bottom=0, top=max(max_gei_val * 1.15, 1))
for bar in ax_gei_total.patches:
    yval = bar.get_height()
    ax_gei_total.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_gei_total, "GEI_Evitados_Total", "download_gei_total")
plt.close(fig_gei_total)

# Figura 2: Residuos Valorizados
fig_residuos, ax_residuos = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_residuos.bar(x, residuos_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax_residuos.set_ylabel('Toneladas/año', fontsize=12, color=colors_for_charts[0])
ax_residuos.set_title('Residuos Orgánicos Valorizados', fontsize=14, color=colors_for_charts[3], pad=20)
ax_residuos.set_xticks(x)
ax_residuos.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_residuos.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_residuos.spines['top'].set_visible(False)
ax_residuos.spines['right'].set_visible(False)
ax_residuos.tick_params(axis='x', length=0)
ax_residuos.set_ylim(bottom=0, top=max(max_residuos_val * 1.15, 1))
for bar in ax_residuos.patches:
    yval = bar.get_height()
    ax_residuos.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_residuos, "Residuos_Valorizados", "download_residuos")
plt.close(fig_residuos)

# Figura 3: Ingresos Estimados
fig_ingresos, ax_ingresos = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_ingresos.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax_ingresos.set_ylabel('USD/año', fontsize=12, color=colors_for_charts[3])
ax_ingresos.set_title('Ingresos Estimados', fontsize=14, color=colors_for_charts[3], pad=20)
ax_ingresos.set_xticks(x)
ax_ingresos.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_ingresos.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_ingresos.spines['top'].set_visible(False)
ax_ingresos.spines['right'].set_visible(False)
ax_ingresos.tick_params(axis='x', length=0)
ax_ingresos.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 1000))
for bar in ax_ingresos.patches:
    yval = bar.get_height()
    ax_ingresos.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"${yval:,.0f}", ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_ingresos, "Ingresos_Estimados", "download_ingresos")
plt.close(fig_ingresos)


st.markdown("---")
st.markdown("### Información Adicional:")
st.markdown(f"- **Estado de Avance y Recomendaciones:** El proyecto ha mostrado resultados positivos en la calidad nutricional del producto final y en la capacidad de la tecnología para transformar residuos orgánicos en biomasa proteica. Se requiere profundizar en la caracterización de los residuos valorizados y formalizar protocolos de recolección, higiene y manejo previo a la bioconversión.")

st.markdown("---")
# Texto de atribución centrado
st.markdown("<div style='text-align: center;'>Visualizador Creado por el equipo Sustrend SpA en el marco del Proyecto TT GREEN Foods</div>", unsafe_allow_html=True)

# Aumentar el espaciado antes de los logos
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Mostrar Logos ---
col_logos_left, col_logos_center, col_logos_right = st.columns([1, 2, 1])

with col_logos_center:
    sustrend_logo_url = "https://drive.google.com/uc?id=1vx_znPU2VfdkzeDtl91dlpw_p9mmu4dd"
    ttgreenfoods_logo_url = "https://drive.google.com/uc?id=1uIQZQywjuQJz6Eokkj6dNSpBroJ8tQf8"

    try:
        sustrend_response = requests.get(sustrend_logo_url)
        sustrend_response.raise_for_status()
        sustrend_image = Image.open(BytesIO(sustrend_response.content))

        ttgreenfoods_response = requests.get(ttgreenfoods_logo_url)
        ttgreenfoods_response.raise_for_status()
        ttgreenfoods_image = Image.open(BytesIO(ttgreenfoods_response.content))

        st.image([sustrend_image, ttgreenfoods_image], width=100)
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar los logos desde las URLs. Por favor, verifica los enlaces: {e}")
    except Exception as e:
        st.error(f"Error inesperado al procesar las imágenes de los logos: {e}")

st.markdown("<div style='text-align: center; font-size: small; color: gray;'>Viña del Mar, Valparaíso, Chile</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='text-align: center; font-size: smaller; color: gray;'>Versión del Visualizador: 1.8</div>", unsafe_allow_html=True) # Actualizada la versión
st.sidebar.markdown(f"<div style='text-align: center; font-size: x-small; color: lightgray;'>Desarrollado con Streamlit</div>", unsafe_allow_html=True)
