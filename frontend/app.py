import streamlit as st
import requests
import ics
import os

from datetime import date
from streamlit_calendar import calendar as st_calendar


BACKEND_URL = "https://cycle-planner.onrender.com"
EVENTS_PATH = "/events/"
BASE_URL_DATE_NAGER  = "https://date.nager.at/"
AVAILABLE_COUNTRIES_PATH = "/api/v3/AvailableCountries"

st.set_page_config(page_title="Planificador de Eventos", page_icon="📅", layout="centered")
st.title("Planificador de Eventos")

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "static/styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("No se encontró 'styles.css'. Asegúrate de crearlo en el mismo directorio.")

# Cargar los estilos antes de la UI
load_css()

@st.cache_data
def get_countries():
    response = requests.get(BASE_URL_DATE_NAGER + AVAILABLE_COUNTRIES_PATH)
    if response.status_code == 200:
        countries = response.json()
        return {country["name"]: country["countryCode"] for country in countries}, next((i for i, c in enumerate(countries) if c["countryCode"] == "CO"), 0)
    return [], 0

country_dict, colombia_index = get_countries()

def parse_ics(ics_content):
    events = []
    calendar_data = ics.Calendar(ics_content)
    for event in calendar_data.events:
        events.append({
            "date": event.begin.date(),
            "summary": event.name
        })
    return events


def create_calendar(body):
    response = requests.post(BACKEND_URL + EVENTS_PATH, json=body)
    if response.status_code == 200:
        st.success("Evento registrado con éxito!")
        return response.content
    else:
        st.error("Error al registrar el evento")
        return None

def init_session_state():
    if "selected_year" not in st.session_state:
        st.session_state.selected_year = date.today().year
    if "events" not in st.session_state:
        st.session_state.events = []
    if "ics_content" not in st.session_state:
        st.session_state.ics_content = ""
    if "show_calendar" not in st.session_state:
        st.session_state.show_calendar = False

init_session_state()


def toggle_country():
    """Función para actualizar el estado de habilitación del país."""
    st.session_state.country_disabled = not st.session_state.exclude_holidays

with st.form("event_form"):
    event_name = st.text_input("Nombre del Evento", "Evento", max_chars=100)
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Fecha de inicio", min_value=date.today())
    with col2:
        end_date = st.date_input("Fecha final", value=date(date.today().year, 12, 31))

    col3, col4 = st.columns(2)
    with col3:
        frequency = st.number_input("Frecuencia (días)", min_value=1, value=6)
    with col4:
        country_name = st.selectbox("Seleccionar País", options=list(country_dict.keys()), index=colombia_index)
    exclude_weekends = st.checkbox("Excluir fines de semana", value=True)
    exclude_holidays = st.checkbox("Excluir festivos nacionales", value=True)

    country_code = country_dict[country_name]

    extra_invalid_dates = st.text_area("Otras fechas para excluir (YYYY-MM-DD, separadas por comas)",
                                       "2025-04-14,2025-04-15,2025-04-16")
    submit_button = st.form_submit_button("Generar Calendario")


if submit_button:
    if not event_name or not country_code:
        st.error("Por favor complete todos los campos obligatorios")
    else:
        extra_dates_list = [d.strip() for d in extra_invalid_dates.split(",") if d.strip()]

        event_data = {
            "name": event_name,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "frequency": frequency,
            "country": country_code,
            "exclude_weekends": exclude_weekends,
            "exclude_holidays": exclude_holidays,
            "extra_invalid_dates": extra_dates_list
        }
        calendar = create_calendar(event_data)
        if calendar:
            st.session_state.ics_content = calendar.decode("utf-8")
            st.session_state.show_calendar = True
            st.session_state.events = parse_ics(st.session_state.ics_content)

if st.session_state.show_calendar:
    with st.expander("Calendario de Eventos", expanded=True):

        event_list = [
            {
                "title": event["summary"],
                "start": event["date"].strftime("%Y-%m-%d"),
            }
            for event in st.session_state.events
        ]

        st_calendar(
            options={"editable": False, "selectable": False},
            events=event_list,
            key="calendar_view"
        )

        st.download_button("Descargar Calendario", data=st.session_state.ics_content,  file_name=f"{event_name}.ics",
                           mime="text/calendar")
