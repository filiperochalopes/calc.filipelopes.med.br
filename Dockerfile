# syntax=docker/dockerfile:1

FROM python:3.12-alpine
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --user -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--reload" ]