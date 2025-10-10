FROM spymovil/python38_imagen_base:20250930

# Evitar que Python haga buffering en stdout/stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /process
COPY . .
RUN ls -laR
RUN chmod 777 /process/*

# Comando de arranque (-u también fuerza no buffer)
#CMD ["python3", "-u", "/bdbackup/app.py"]
#CMD ["python3", "/apiredis/app.py"]

CMD ["python3", "/process/app.py"]
