# FastAPI Backend

Este es un backend construido con FastAPI. Proporciona endpoints para la gestión de eventos.

## Requisitos

- Python 3.9
- FastAPI
- Uvicorn

## Instalación y ejecución local

1. Clona el repositorio:
2. Crea un entorno virtual (opcional pero recomendado):

   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```sh
   pip install -r requirements.txt
   ```

4. Ejecuta el servidor:

   ```sh
    uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
   ```

5. Prueba el endpoint localmente con `curl`:

   ```sh
   curl --location 'http://0.0.0.0:8000/events' \
   --header 'Content-Type: application/json' \
   --data '{
       "name": "Event",
       "start_date": "2025-02-01",
       "end_date" : "2025-02-28",
       "frequency": 3,
       "country": "CO",
       "exclude_weekends": true,
       "exclude_holidays": true,
       "extra_invalid_dates" : ["2025-02-16","2025-02-17","2025-02-18","2025-02-19","2025-02-20"]
   }'
   ```


## Documentación Interactiva

FastAPI genera documentación automática en:
- **Swagger UI**: [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) (local)
- **Redoc**: [http://0.0.0.0:8000/redoc](http://0.0.0.0:8000/redoc) (local)

Cuando se despliega en Render, sustituye `http://0.0.0.0:8000` con la URL pública del servicio.

