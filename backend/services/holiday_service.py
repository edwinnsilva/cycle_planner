from datetime import date
from typing import List
import requests
import logging


BASE_URL_DATE_NAGER  = "https://date.nager.at/"
PUBLIC_HOLIDAYS_PATH  = "api/v3/PublicHolidays/{Year}/{CountryCode}"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)



def get_holidays(year: int, country_code: str) -> List[date]:
    """
    Consulta los festivos nacionales de un país para un año determinado.

    :param year: Año para el cual se consultan los festivos.
    :param country_code: Código del país (ejemplo: "CO" para Colombia).
    :return: Lista de fechas de festivos en formato "YYYY-MM-DD".
    """
    url = BASE_URL_DATE_NAGER + PUBLIC_HOLIDAYS_PATH.format(Year=year, CountryCode=country_code)

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        logger.info(f"successful call to date.nager")
        holidays = [date.fromisoformat(holiday["date"]) for holiday in response.json()]
        return holidays
    except requests.RequestException as e:
        logger.error(f"Fallo en la solicitud de festivos: {e}")
        return []
