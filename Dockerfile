FROM python:3-slim
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY main.py .
EXPOSE 8000
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000"]