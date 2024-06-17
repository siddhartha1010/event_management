from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    # default="bcrypt",
    deprecated="auto"
)

class Hash():
    def bcrypt(self, password: str):
        return pwd_context.hash(password)#cryptcontext class contains hash method
    
    def verify(self, hashed_password,plain_password):
        return pwd_context.verify(plain_password,hashed_password)
 