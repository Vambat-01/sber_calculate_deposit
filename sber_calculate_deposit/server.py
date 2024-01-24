import asyncio

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from uvicorn import Config, Server

from sber_calculate_deposit.models import RequestDeposit, ResponseDeposit

from sber_calculate_deposit.deposit import calculate_deposit


v1_router = APIRouter()


@v1_router.post("/deposit/calculate", response_model=ResponseDeposit)
def get_deposit(data: RequestDeposit):
    """Функция выводит полученные значения калькулятора и собирает данные в базу данных."""

    values = calculate_deposit(data=data)
    values_dict = {d.strftime("%d.%m.%Y"): amount for d, amount in values}
    return JSONResponse(content=values_dict)


app = FastAPI()
app.include_router(v1_router, prefix="/api/v1")


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Обработки ошибок при валидации данных."""

    if len(exc.errors()) > 1:
        err_massage = 'All fields are required'
    else:
        err_massage = (f"field {exc.errors()[0]['loc'][1]}: "
                       f"{exc.errors()[0]['msg']}")

    return JSONResponse(status_code=400, content={"error": err_massage})


async def main():
    config = Config(app=app, host="0.0.0.0", port=8000)
    server = Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
