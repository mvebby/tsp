FROM python

# рабочая директория внутри контейнейра, команды выполняются из этой директории (manage, runserver)
WORKDIR /tsp 

COPY requirements.txt ./
RUN pip install -r requirements.txt