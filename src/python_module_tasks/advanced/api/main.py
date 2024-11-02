from fastapi import FastAPI

from python_module_tasks.advanced.api.routes import admin, customer

app = FastAPI()

app.include_router(customer.router, prefix="/customer")
app.include_router(admin.router, prefix="/admin")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Pizza Delivery Service!"}
