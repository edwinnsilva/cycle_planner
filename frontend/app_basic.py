import streamlit as st
import requests
from datetime import date

BACKEND_URL = "http://127.0.0.1:8000/events/"
COUNTRIES_API = "https://date.nager.at/api/v3/AvailableCountries"


# Configuración de la aplicación
st.set_page_config(page_title="Planificador de Eventos", page_icon="📅", layout="centered")

st.title("Planificador de Eventos")

# Formulario para ingresar datos del evento
with st.form("event_form"):
    event_name = st.text_input("Nombre del Evento", "Evento", max_chars=100)
    start_date = st.date_input("Fecha de Inicio", min_value=date.today())
    end_date = st.date_input("Fecha Final", value=date(date.today().year, 12, 31))
    frequency = st.number_input("Frecuencia (días)", min_value=1, value=6)

    # Obtener países disponibles de la API
    response = requests.get("https://date.nager.at/api/v3/AvailableCountries")
    if response.status_code == 200:
        countries = response.json()
        country_dict = {country["name"]: country["countryCode"] for country in countries}
        country_name = st.selectbox("Seleccionar País", options=list(country_dict.keys()))
        country_code = country_dict[country_name]
    else:
        st.error("Error al cargar la lista de países")
        country_code = ""

    # Calendario para seleccionar fechas adicionales inválidas
    extra_invalid_dates = st.text_area("Fechas adicionales no válidas (YYYY-MM-DD, separadas por comas)")

    submit_button = st.form_submit_button("Generar Fechas")

if submit_button:
    if not event_name or not country_code:
        st.error("Por favor complete todos los campos obligatorios")
    else:
        # Convertir fechas adicionales inválidas en una lista
        extra_dates_list = [d.strip() for d in extra_invalid_dates.split(",") if d.strip()]

        # Construcción del JSON para el backend
        event_data = {
            "name": event_name,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "frequency": frequency,
            "country": country_code,
            "extra_invalid_dates": extra_dates_list
        }

        # Llamada al backend
        response = requests.post(BACKEND_URL, json=event_data)

        if response.status_code == 200:
            st.success("Evento registrado con éxito!")

            ics_content = response.content
            st.download_button(
                label="Descargar archivo ICS",
                data=ics_content,
                file_name="eventos.ics",
                mime="text/calendar"
            )

        else:
            st.error("Error al registrar el evento")