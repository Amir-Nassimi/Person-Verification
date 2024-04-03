FROM python:3.11.0
LABEL authors="hesamdavarpanah"

RUN apt -y update
RUN apt -y upgrade
RUN apt-get clean
RUN apt-get install -y netcat-traditional
RUN apt-get install -y net-tools
RUN apt-get install -y iputils-ping
RUN apt-get install -y zsh
RUN apt-get install -y libgl1
RUN apt-get install -y supervisor

RUN python -m pip install --upgrade pip

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade -r /code/requirements.txt

COPY . /code

RUN chmod +x ./run.sh
RUN chmod +x ./docker-entrypoint.sh
RUN chmod -R 777 ./

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["supervisord"]