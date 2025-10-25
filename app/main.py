from fastapi import FastAPI
from app.routes import auth_routes, customer_routes

app = FastAPI(title="Bees & Bears Backend")

app.include_router(auth_routes.router)
app.include_router(customer_routes.router)