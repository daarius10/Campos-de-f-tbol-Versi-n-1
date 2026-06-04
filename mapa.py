import json
import folium
from folium.plugins import Fullscreen

# 1. Configuración de rutas de archivos de datos
ruta_geojson = r"D:\Proyecto página web\proyecto-mapa-v1\campos-de-futbol.geojson"

# 2. Inicialización del Mapa centrado en Zaragoza
mapa = folium.Map(location=[41.6488, -0.8891], zoom_start=13, zoom_control=True)
Fullscreen(position="topleft", title="Ver en pantalla completa", title_cancel="Salir de pantalla completa").add_to(mapa)

with open(ruta_geojson, "r", encoding="utf-8") as f:
    datos = json.load(f)

lista_campos_js = []
distritos_unicos = set()
clubes_unicos = set()

# MAPEO ESTRICTO CON LOS NOMBRES OFICIALES DE LOS CLUBES SOLICITADOS
mapeo_clubes = {
    # Asignaciones específicas solicitadas por instalación
    "Campo Municipal de Fútbol Torre Ramona": "El Santo Domingo Juventud",
    "Campo Municipal de Fútbol Hernán Cortés": "Hernán Cortés",
    "Campo Municipal de Fútbol Santa Isabel": "Santa Isabel",
    "Campo Municipal de Fútbol San Juan de Mozarrifar": "Monzarrifar",
    "Campo de Fútbol Picarral": "UD Balsas Picarral",
    "Campo Municipal de Fútbol Peñaflor": "Peñaflor",
    "Campo Municipal de Fútbol José Luis Violeta": "Montecarlo",
    "Campo Municipal de Fútbol Juslibol": "Amistad",
    "Campo Municipal de Fútbol La Almozara": "Ebro",
    "Campo de Fútbol San Gregorio": "San Gregorio",
    "Campo Municipal de Fútbol Movera": "Movera",
    "Campo Municipal de Fútbol Monzalbarba": "Monzalbarba",
    "Campo Municipal de Fútbol Parque Oliver": "CD Oliver",
    
    # Sedes exclusivas del Real Zaragoza
    "Campo Municipal de Fútbol Romareda": "Real Zaragoza",
    "Ciudad Deportiva Real Zaragoza": "Real Zaragoza",
    
    # Resto de instalaciones del GeoJSON con su club correspondiente
    "Campo Municipal de Fútbol El Rabal": "Zaragoza CFF",
    "Campo Municipal de Fútbol San José": "UD San José",
    "Campo Municipal de Fútbol La Cartuja": "La Cartuja",
    "Campo Municipal de Fútbol Actur Benjamín Mustieles": "Actur Pablo Iglesias",
    "Campo Municipal de Fútbol Ranillas": "CD Ranillas",
    "Campo Municipal de Fútbol Valdefierro": "CD Valdefierro",
    "Campo Municipal de Fútbol Fleta": "CD Fleta",
    "Campo de Fútbol CMP Venecia": "Stadium Venecia",
    "Campo de Fútbol El Salvador": "CD El Salvador"
}

def agregar_marcador_al_mapa(nombre_campo, club, direccion, telefono, distrito, lat, lon):
    distritos_unicos.add(distrito)
    clubes_unicos.add(club)
    
    url_ruta = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
    
    # Construcción limpia de HTML para evitar romper las cadenas de Python
    popup_html = (
        f"<div style=\"font-family: 'Inter', sans-serif; min-width: 250px; padding: 3px; color: #1e293b;\">"
        f"<div style=\"text-transform: uppercase; font-size: 10px; font-weight: 800; color: #10b981; letter-spacing: 1px; margin-bottom: 2px;\">{club}</div>"
        f"<h4 style=\"margin: 0 0 12px 0; color: #0f172a; font-size: 15px; font-weight: 700; line-height: 1.3;\">{nombre_campo}</h4>"
        f"<div style=\"display: flex; flex-direction: column; gap: 6px; font-size: 12px; border-top: 1px solid #e2e8f0; padding-top: 8px; margin-bottom: 14px;\">"
        f"<div style=\"display: flex; align-items: flex-start; gap: 6px;\"><span>📍</span> <span><b>Dirección:</b> {direccion}</span></div>"
        f"<div style=\"display: flex; align-items: center; gap: 6px;\"><span>📞</span> <span><b>Teléfono:</b> {telefono}</span></div>"
        f"<div style=\"display: flex; align-items: center; gap: 6px;\"><span>🛡️</span> <span><b>Distrito:</b> <span style=\"background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 11px;\">{distrito}</span></span></div>"
        f"</div>"
        f"<a href=\"{url_ruta}\" target=\"_blank\" style=\"display: block; text-align: center; padding: 10px; background: #0f172a; color: #ffffff; text-decoration: none; border-radius: 6px; font-size: 12px; font-weight: 700;\">🚀 CÓMO LLEGAR</a>"
        f"</div>"
    )
    
    marcador = folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=350),
        icon=folium.Icon(color="blue", icon="soccer-ball", prefix="fa")
    )
    marcador.add_to(mapa)
    
    lista_campos_js.append({
        "id": marcador.get_name(),
        "nombre": nombre_campo.lower(),
        "club": club.lower(),
        "club_exacto": club,
        "distrito": distrito
    })

print("📦 Leyendo el GeoJSON...")
for feature in datos["features"]:
    try:
        propiedades = feature.get("properties", {})
        nombre_campo = propiedades.get("title", "Campo de Fútbol")
        
        if nombre_campo in ["Colegio San Agustín", "Ciudad Deportiva Real Zaragoza", "Estadio Miralbueno El Olivar", "Stadium Casablanca"]:
            continue
            
        direccion = propiedades.get("streetAddress", "Zaragoza")
        distrito = propiedades.get("distritoId", "Otros")
        
        club_asociado = mapeo_clubes.get(nombre_campo, nombre_campo.replace("Campo Municipal de Fútbol ", ""))
        
        telefono = propiedades.get("telephone", "No disponible")
        if not telefono or telefono in ["null", "None"]:
            telefono = "No disponible"
            
        lat, lon = float(propiedades["latitud"]), float(propiedades["longitud"])
        agregar_marcador_al_mapa(nombre_campo, club_asociado, direccion, telefono, distrito, lat, lon)
    except:
        continue

print("➕ Añadiendo complejos manuales...")
campos_manuales = [
    {"nombre": "Colegio San Agustín", "club": "San Agustín", "direccion": "Camino de las Torres, 79", "telefono": "976 224 825", "distrito": "Centro", "latitud": 41.6414, "longitud": -0.8824},
    {"nombre": "Ciudad Deportiva Real Zaragoza", "club": "Real Zaragoza", "direccion": "Carretera de Valencia, KM 8", "telefono": "976 567 777", "distrito": "Cuarte", "latitud": 41.594722, "longitud": -0.948889},
    {"nombre": "Estadio Miralbueno El Olivar", "club": "EM El Olivar", "direccion": "Calle Argualas, 50", "telefono": "976 306 336", "distrito": "Casablanca", "latitud": 41.6278, "longitud": -0.9162},
    {"nombre": "Stadium Casablanca", "club": "Stadium Casablanca", "direccion": "Vía Ibérica, 69-77", "telefono": "976 754 100", "distrito": "Casablanca", "latitud": 41.6236953, "longitud": -0.9089993}
]

for c in campos_manuales:
    agregar_marcador_al_mapa(c["nombre"], c["club"], c["direccion"], c["telefono"], c["distrito"], c["latitud"], c["longitud"])

options_distritos = "".join([f'<option value="{d}">{d}</option>' for d in sorted(list(distritos_unicos))])
options_clubes = "".join([f'<option value="{c}">{c}</option>' for c in sorted(list(clubes_unicos))])

# Estructura HTML inyectada sin usar comillas triples complejas de Python
interfaz_html = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
    #app-sports-panel {
        position: absolute; top: 20px; left: 65px; z-index: 1000;
        background: rgba(15, 23, 42, 0.9); color: #ffffff; padding: 20px;
        border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        font-family: 'Inter', sans-serif; width: 310px; backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1); box-sizing: border-box;
    }
    .app-brand { font-size: 11px; font-weight: 800; color: #10b981; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px; }
    .app-title { margin: 0 0 4px 0; font-size: 18px; font-weight: 700; }
    .app-counter { font-size: 12px; color: #94a3b8; margin-bottom: 16px; display: block; font-weight: 500; }
    .label-filtro { font-size: 11px; font-weight: 600; color: #94a3b8; margin-bottom: 6px; display: block; text-transform: uppercase; }
    .input-pro { width: 100%; padding: 11px 14px; margin-bottom: 12px; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; box-sizing: border-box; font-size: 13px; background: rgba(255, 255, 255, 0.07); color: #ffffff; }
    .select-pro { width: 100%; padding: 11px 14px; margin-bottom: 12px; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; background: #1e293b; color: #ffffff; box-sizing: border-box; font-size: 13px; cursor: pointer; }
    .btn-gps { width: 100%; padding: 10px; background: #2563eb; color: #ffffff; border: none; border-radius: 8px; font-size: 12px; font-weight: 700; cursor: pointer; margin-top: 14px; display: flex; align-items: center; justify-content: center; gap: 6px; }
    option { background: #0f172a; color: #ffffff; }
</style>

<div id="app-sports-panel">
    <div class="app-brand">Zaragoza Football Map</div>
    <h2 class="app-title">Panel de Control</h2>
    <span class="app-counter" id="contadorCampos">Cargando instalaciones...</span>
    
    <span class="label-filtro">🔍 Buscar Club u Oficial</span>
    <input type="text" id="buscadorGlobal" class="input-pro" placeholder="Ej: Real Zaragoza, Ebro..." onkeyup="filtrarApp()">
    
    <span class="label-filtro">🛡️ Filtrar por Club</span>
    <select id="filtroClub" class="select-pro" onchange="filtrarApp()">
        <option value="todos">Todos los clubes oficiales</option>
        __OPCIONES_CLUBES__
    </select>
    
    <span class="label-filtro">📍 Filtrar por Barrio</span>
    <select id="filtroBarrio" class="select-pro" onchange="filtrarApp()">
        <option value="todos">Todos los distritos</option>
        __OPCIONES_DISTRITOS__
    </select>

    <button class="btn-gps" onclick="localizarUsuario()">🎯 ENCONTRAR MI UBICACIÓN</button>
</div>

<script>
    var datosCampos = __JSON_CAMPOS__;
    var mapaInstancia = null;
    var marcadorUsuario = null;

    document.addEventListener("DOMContentLoaded", function() {
        setTimeout(function() {
            mapaInstancia = __ID_MAPA__;
            actualizarContador(datosCampos.length);
        }, 300);
    });

    function actualizarContador(num) {
        document.getElementById('contadorCampos').innerText = "⚽ " + num + " clubes en el mapa";
    }

    function filtrarApp() {
        var consulta = document.getElementById('buscadorGlobal').value.toLowerCase();
        var clubSeleccionado = document.getElementById('filtroClub').value;
        var barrioSeleccionado = document.getElementById('filtroBarrio').value;
        var visibles = 0;
        
        datosCampos.forEach(function(campo) {
            var markerInst = window[campo.id];
            if (markerInst) {
                var matchTexto = campo.nombre.includes(consulta) || campo.club.includes(consulta);
                var matchClub = (clubSeleccionado === 'todos' || campo.club_exacto === clubSeleccionado);
                var matchBarrio = (barrioSeleccionado === 'todos' || campo.distrito === barrioSeleccionado);
                
                if (matchTexto && matchClub && matchBarrio) {
                    markerInst.addTo(mapaInstancia);
                    visibles++;
                } else {
                    markerInst.remove();
                }
            }
        });
        actualizarContador(visibles);
    }

    function localizarUsuario() {
        if (!navigator.geolocation) { alert("Navegador no compatible."); return; }
        navigator.geolocation.getCurrentPosition(function(pos) {
            var lat = pos.coords.latitude; var lon = pos.coords.longitude;
            if (marcadorUsuario) { marcadorUsuario.remove(); }
            marcadorUsuario = L.marker([lat, lon]).addTo(mapaInstancia).bindPopup("<b>👋 ¡Estás aquí!</b>").openPopup();
            mapaInstancia.flyTo([lat, lon], 14);
        });
    }
</script>
"""

# Reemplazos y guardado seguro del archivo
interfaz_html = interfaz_html.replace("__OPCIONES_CLUBES__", options_clubes)
interfaz_html = interfaz_html.replace("__OPCIONES_DISTRITOS__", options_distritos)
interfaz_html = interfaz_html.replace("__JSON_CAMPOS__", json.dumps(lista_campos_js))
interfaz_html = interfaz_html.replace("__ID_MAPA__", mapa.get_name())

mapa.get_root().html.add_child(folium.Element(interfaz_html))
mapa.save(r"D:\Proyecto página web\proyecto-mapa-v1\index.html")
print("🔥 ¡ÉXITO! Mapa corregido y compilado de forma estable sin errores de sintaxis.")