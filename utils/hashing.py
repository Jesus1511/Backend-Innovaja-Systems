from passlib.context import CryptContext # type: ignore

# Configura el contexto de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Genera un hash de la contraseña proporcionada."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con el hash."""
    return pwd_context.verify(plain_password, hashed_password)