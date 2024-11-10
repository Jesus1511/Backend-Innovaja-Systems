from Database.database import database, session
from Database.models import User, UserIn, TokenData
from fastapi import HTTPException, status, Depends # type: ignore
from fastapi.responses import JSONResponse # type: ignore
from sqlalchemy import insert, select # type: ignore
from utils.hashing import hash_password, verify_password
from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from datetime import timedelta
from utils.jwt import create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # type: ignore
from jose import JWTError, jwt # type: ignore

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def singIn(user: UserIn):
    query = select(User).where((User.email == user.email) | (User.dni == user.dni))
    existing_user = await database.fetch_one(query)
    
    if existing_user:
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
        if existing_user.dni == user.dni:
            raise HTTPException(status_code=400, detail="DNI already registered")
    
    hashed_password = hash_password(user.password)

    # Preparar una consulta de inserción para el nuevo usuario
    query = insert(User).values(
        username=user.username,
        email=user.email,
        password=hashed_password,
        dni=user.dni
    )
    await database.execute(query)

    return JSONResponse(
        status_code=201,
        content={"message": "Usuario creado exitosamente", "user": user.dict()}
    )


async def logIn(email: str, password: str):
    usuario = session.query(User).filter(User.email == email).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="not registered Email")

    if verify_password(password, usuario.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    else:
        raise HTTPException(status_code=400, detail="incorrect email or password")


async def logOut(email: str):
    return


async def deleteUser(id:int):
    user_to_delete = session.query(User).filter_by(id=id).first()
 
    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
        return JSONResponse(
            status_code=201,
            content={"message": "Usuario eliminado correctamente"}
        )
    else:
      raise HTTPException(status_code=400, detail="User dosn't exist")


async def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = session.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

