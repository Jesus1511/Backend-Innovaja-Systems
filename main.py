from fastapi import FastAPI, Depends # type: ignore
from fastapi.responses import JSONResponse # type: ignore
from Database.database import database, engine
from UserCrud.functions import singIn, logIn, deleteUser, get_current_user
from Database.models import UserIn, Base, LoginRequest, deleteRequest, getCurrentRequest, User

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

@app.post('/users/login')
async def login(request: LoginRequest):
    return await logIn(request.email, request.password)

@app.get('/users/current')
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.post('/users/singin')
async def singin_user(user: UserIn):  # Specify the UserIn model here
    return await singIn(user)

@app.post('/users/deleteUser')
async def delete(request: deleteRequest):
    id = request.id
    return await deleteUser(id)
    
