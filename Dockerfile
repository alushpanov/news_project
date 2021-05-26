FROM python:3
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /home/andrei/NEWS/news_project
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .