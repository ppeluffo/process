FROM spymovil/python38_imagen_base:20250930

# Evitar que Python haga buffering en stdout/stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /process
COPY . .
RUN ls -laR
RUN chmod 777 /process/*

CMD ["python3", "/process/app.py"]
