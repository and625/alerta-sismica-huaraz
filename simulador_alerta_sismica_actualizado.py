
import streamlit as st
import folium
from streamlit_folium import folium_static
import math
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulación de Sistema de Alerta Sísmica", layout="wide")

st.title("🌍 Simulación de Sistema de Alerta Sísmica")

# Descripción general
st.markdown("**Esta plataforma tiene como propósito registrar, visualizar y monitorear eventos sísmicos en las zonas de Huaraz, el Callejón de Conchucos y el Callejón de Huaylas.**")
st.markdown("El sistema considera una amplitud histórica y predictiva de hasta 5 años, permitiendo observar el tiempo estimado de llegada de las ondas sísmicas a cada sensor, así como el nivel de anticipación que podrían ofrecer en un escenario real.")

# Coordenadas del epicentro
epicenter = {"lat": -9.5287, "lon": -77.5308}

# Lista de sensores con zona especificada
sensors = [
    {"nombre": "Huaraz Centro", "lat": -9.5300, "lon": -77.5287, "zona": "Huaraz"},
    {"nombre": "Independencia", "lat": -9.5212, "lon": -77.5271, "zona": "Huaraz"},
    {"nombre": "Caraz", "lat": -9.0503, "lon": -77.8167, "zona": "Callejón de Huaylas"},
    {"nombre": "Yungay", "lat": -9.1441, "lon": -77.7415, "zona": "Callejón de Huaylas"},
    {"nombre": "Chavín", "lat": -9.5946, "lon": -77.1772, "zona": "Callejón de Conchucos"},
    {"nombre": "San Marcos", "lat": -9.5924, "lon": -77.1601, "zona": "Callejón de Conchucos"},
    {"nombre": "Huari", "lat": -9.6129, "lon": -77.0407, "zona": "Callejón de Conchucos"},
]

wave_speed_kms = 6.0

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Cálculo
resultados = []
for idx, s in enumerate(sensors, 1):
    distancia = haversine(epicenter["lat"], epicenter["lon"], s["lat"], s["lon"])
    tiempo_llegada = distancia / wave_speed_kms
    anticipacion = round(max(0, (1 - (10 / distancia)) * 100), 2) if distancia > 10 else round((distancia / 10) * 100, 2)
    resultados.append({
        "N°": idx,
        "Sensor": s["nombre"],
        "Zona": s["zona"],
        "Distancia (km)": round(distancia, 2),
        "Tiempo estimado llegada (s)": round(tiempo_llegada, 2),
        "% de anticipación estimado": anticipacion
    })

df = pd.DataFrame(resultados)

# Mapa
st.markdown("### 🗺️ Mapa de sensores y epicentro")
m = folium.Map(location=[epicenter["lat"], epicenter["lon"]], zoom_start=9)
folium.Marker([epicenter["lat"], epicenter["lon"]], tooltip="Epicentro", icon=folium.Icon(color='red')).add_to(m)
for s in sensors:
    color = "blue" if s["zona"] == "Huaraz" else "green" if s["zona"] == "Callejón de Huaylas" else "orange"
    folium.Marker([s["lat"], s["lon"]], tooltip=f"{s['nombre']} ({s['zona']})", icon=folium.Icon(color=color)).add_to(m)
folium_static(m, width=900, height=500)

# Tabla
st.markdown("### 📋 Tabla de resultados")
st.dataframe(df, use_container_width=True)

# Porcentaje
st.markdown("### 📊 Porcentaje de anticipación por sensor")
st.markdown("El porcentaje de anticipación representa cuánto tiempo antes un sensor podría detectar una onda sísmica antes de que esta llegue a su ubicación. A mayor porcentaje, mayor tiempo para actuar.")

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df["Sensor"], df["% de anticipación estimado"], color='darkcyan')
ax.set_ylabel('% de anticipación')
ax.set_title('Anticipación estimada por sensor')
plt.xticks(rotation=45)
st.pyplot(fig)

# Contacto
st.markdown("---")
st.markdown("### 📞 Contacto")
st.markdown("Para consultas, sugerencias o información adicional:")
st.markdown("- 📧 Correo: sismoshuaraz@alertaperu.org")
st.markdown("- 📱 Teléfono: +51 958479979")

# Sugerencias
st.markdown("### 📬 Caja de Sugerencias")
sugerencia = st.text_area("Déjanos tu sugerencia o reporte anónimo aquí:")
if st.button("Enviar sugerencia"):
    if sugerencia.strip():
        st.success("¡Gracias por tu comentario! Será revisado por nuestro equipo.")
    else:
        st.warning("Por favor escribe algo antes de enviar.")

# Advertencia sobre el timbre
st.markdown("---")
st.markdown("GRACIAS POR VISITARNOS")
