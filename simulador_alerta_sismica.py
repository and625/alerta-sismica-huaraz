
import streamlit as st
import folium
from streamlit_folium import folium_static
import math
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulación de Alerta Sísmica - Huaraz y Conchucos", layout="wide")

st.title("🌍 Simulación de Sistema de Alerta Sísmica")
st.subheader("Zona: Huaraz y Callejón de Conchucos - Epicentro simulado en Huaraz")

# Coordenadas del epicentro simulado (cerca de Huaraz)
epicenter = {"lat": -9.5287, "lon": -77.5308}

# Sensores
sensors = [
    {"nombre": "Huaraz Centro", "lat": -9.5300, "lon": -77.5287},
    {"nombre": "Independencia", "lat": -9.5212, "lon": -77.5271},
    {"nombre": "Chavín", "lat": -9.5946, "lon": -77.1772},
    {"nombre": "San Marcos", "lat": -9.5924, "lon": -77.1601},
    {"nombre": "Huari", "lat": -9.6129, "lon": -77.0407},
    {"nombre": "Piscobamba", "lat": -8.9493, "lon": -77.3891},
    {"nombre": "Pomabamba", "lat": -8.9400, "lon": -77.6372},
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
for s in sensors:
    distancia = haversine(epicenter["lat"], epicenter["lon"], s["lat"], s["lon"])
    tiempo_llegada = distancia / wave_speed_kms
    anticipacion = max(0, round((distancia - 10) / distancia * 100, 2))
    resultados.append({
        "Sensor": s["nombre"],
        "Distancia (km)": round(distancia, 2),
        "Tiempo estimado llegada (s)": round(tiempo_llegada, 2),
        "% de anticipación estimado": anticipacion
    })

df = pd.DataFrame(resultados)

# Mostrar Mapa
st.markdown("### 🗺️ Mapa de sensores y epicentro")
m = folium.Map(location=[epicenter["lat"], epicenter["lon"]], zoom_start=9)
folium.Marker([epicenter["lat"], epicenter["lon"]], tooltip="Epicentro", icon=folium.Icon(color='red')).add_to(m)
for s in sensors:
    folium.Marker([s["lat"], s["lon"]], tooltip=s["nombre"], icon=folium.Icon(color='blue')).add_to(m)
folium_static(m, width=900, height=500)

# Tabla de resultados
st.markdown("### 📋 Tabla de resultados")
st.dataframe(df, use_container_width=True)

# Gráfico
st.markdown("### 📊 Porcentaje de anticipación por sensor")
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df["Sensor"], df["% de anticipación estimado"], color='teal')
ax.set_ylabel('% de anticipación')
ax.set_title('Anticipación estimada por sensor')
plt.xticks(rotation=45)
st.pyplot(fig)
