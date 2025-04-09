
FROM python:3.10-slim

#to avoid python buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /accounts

#install MYSQL client dependencies

RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev\
    build-essential\
    && rm -rf /var/lib/apt/lists/*

#copy requirements file

COPY requirements.txt .


#Install Python dependencies

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


#copy projects file
COPY . .

EXPOSE 8000

#run the application

CMD ["gunicorn","accounts.wsgi:application","--bind","0.0.0:8000"]

