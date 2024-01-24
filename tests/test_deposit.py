from fastapi.testclient import TestClient
from sber_deposit.server import app
from unittest import TestCase

client = TestClient(app)


class DepositTestCorrect(TestCase):
    def test_correct_deposit(self):
        request_data = {
            "date": "31.01.2021", "periods": 3, "amount": 10000, "rate": 6
        }
        expected_response = {
            "31.01.2021": 10050, "28.02.2021": 10100.25, "31.03.2021": 10150.75
        }
        response = client.post("/api/v1/deposit/calculate", json=request_data)
        assert response.status_code == 200
        assert response.json() == expected_response


class DepositTestError(TestCase):
    def test_incorrect_date_format(self):
        request_data = {
            "date": "31-01-2021", "periods": 3, "amount": 10000, "rate": 6
        }
        response = client.post("/api/v1/deposit/calculate", json=request_data)
        assert response.status_code == 400
        assert response.json()["error"] == "field date: Value error, Date must be in DD.MM.YYYY format"

    def test_incorrect_period_format_more(self):
        request_data = {
            "date": "31.01.2021", "periods": 100, "amount": 10000, "rate": 6
        }
        response = client.post("/api/v1/deposit/calculate", json=request_data)
        assert response.status_code == 400
        assert response.json()["error"] == "field periods: Input should be less than or equal to 60"

    def test_incorrect_period_format_less(self):
        request_data = {
            "date": "31.01.2021", "periods": -1, "amount": 10000, "rate": 6
        }
        response = client.post("/api/v1/deposit/calculate", json=request_data)
        assert response.status_code == 400
        assert response.json()["error"] == "field periods: Input should be greater than or equal to 1"

    def test_incorrect_amount_format_more(self):
        request_data = {
            "date": "31.01.2021", "periods": 3, "amount": 3000100, "rate": 6
        }
        response = client.post("/api/v1/deposit/calculate", json=request_data)
        assert response.status_code == 400
        assert response.json()["error"] == "field amount: Input should be less than or equal to 3000000"

    def test_incorrect_amount_format_less(self):
        request_data = {
            "date": "31.01.2021", "periods": 3, "amount": 5000, "rate": 6
        }
        response = client.post("/api/v1/deposit/calculate", json=request_data)
        assert response.status_code == 400
        assert response.json()[
                   "error"] == "field amount: Input should be greater than or equal to 10000"

    def test_incorrect_rate_format_more(self):
        request_data = {
            "date": "31.01.2021", "periods": 3, "amount": 100000, "rate": 0
        }
        response = client.post("/api/v1/deposit/calculate", json=request_data)
        assert response.status_code == 400
        assert response.json()["error"] == "field rate: Input should be greater than or equal to 1"

    def test_incorrect_rate_format_less(self):
        request_data = {
            "date": "31.01.2021", "periods": 3, "amount": 100000, "rate": 9
        }
        response = client.post("/api/v1/deposit/calculate", json=request_data)
        assert response.status_code == 400
        assert response.json()["error"] == "field rate: Input should be less than or equal to 8"

    def test_incorrect_empty_data(self):
        response = client.post("/api/v1/deposit/calculate", json={})
        assert response.status_code == 400
        assert response.json()["error"] == "All fields are required"
