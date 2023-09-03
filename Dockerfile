FROM library/python:3.11

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

ENTRYPOINT ["uvicorn", "main:app"]
CMD ["--host", "0.0.0.0", "--port", "80"]