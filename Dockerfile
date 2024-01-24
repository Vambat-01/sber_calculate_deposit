FROM python:3.9

WORKDIR /app

COPY sber_calculate_deposit sber_calculate_deposit
COPY requirements.txt requirements.txt
COPY main.py main.py

RUN pip install -r requirements.txt

CMD ["python", "main.py"]