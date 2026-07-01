from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Add to security.py
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

# Security Keys & Settings
SECRET_KEY = "SUPER_SECRET_COMPLEX_DEVELOPMENT_KEY_CHANGE_IN_PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Step 91: 30 minutes expiry

# Step 92: OAuth2 scheme that looks for a token at /api/v1/auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def create_access_token(data: dict) -> str:
    """Step 91: Encodes a JSON Web Token payload with a standard expiration window."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)