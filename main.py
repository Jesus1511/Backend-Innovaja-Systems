from fastapi import FastAPI, Depends # type: ignore
from Database.database import database, engine
from Database.models import Base

from routes.users_routes import user_router

#>
app = FastAPI()
# Crear tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    await database.connect()
    print("Conectado a la base de datos")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    print("Desconectado de la base de datos")

@app.get('/index')
def index():
    return("Servidor funcionando")

app.include_router(user_router)

    
