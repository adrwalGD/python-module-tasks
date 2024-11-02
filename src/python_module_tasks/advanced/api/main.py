from fastapi import FastAPI
import uvicorn

from python_module_tasks.advanced.api.routes import admin, customer

app = FastAPI()

app.include_router(customer.router, prefix="/customer")
app.include_router(admin.router, prefix="/admin")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Pizza Delivery Service!"}


def main():
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    main()
