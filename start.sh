echo "Iniciando aplicação"

uvicorn main:app --host 0.0.0.0 --port $APP_PORT
