from fastapi import APIRouter, Depends, HTTPException, status # type: ignore
from UserCrud.functions import signIn, logIn, deleteUser, get_current_user, logOut, oauth2_scheme
from Database.models import UserIn, LoginRequest, DeleteRequest, User

user_router = APIRouter()

@user_router.post('/users/login')
async def login(request: LoginRequest):
    user = await logIn(request.email, request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

@user_router.get('/users/current')
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@user_router.post('/users/signin')
async def signin_user(user: UserIn):
    return await signIn(user)

@user_router.post('/users/deleteUser')
async def delete_user(request: DeleteRequest):
    return await deleteUser(request.id)

@user_router.post('/users/logout')
async def user_logout(token: str = Depends(oauth2_scheme)):
    return await logOut(token)

