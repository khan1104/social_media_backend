
from config.redis import redis_client
from fastapi import HTTPException,status

def validate_otp(email: str, otp: str):
    data = redis_client.get(f"otp:{email}")

    if data is None:
        raise HTTPException(detail="Otp has been expire",status_code=status.HTTP_404_NOT_FOUND)
    
    if str(data) != str(otp):
        raise HTTPException(detail="inavlid otp",status_code=status.HTTP_400_BAD_REQUEST)
    
    return True
