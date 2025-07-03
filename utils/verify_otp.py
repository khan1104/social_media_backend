from datetime import datetime
from fastapi import HTTPException, status

otp_storage = {}

def validate_otp(email: str, otp: str):
    data = otp_storage.get(email)

    if not data:
        print("❌ Email not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OTP not found for this email")

    # Check expiration
    if data["time"] < datetime.now():
        otp_storage.pop(email, None)
        print("❌ OTP expired")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired")

    # Check OTP match
    if str(data["otp"]) != str(otp):
        print("❌ Invalid OTP")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")

    # Success: optionally remove used OTP
    otp_storage.pop(email, None)
    print("✅ OTP verified successfully")
    return True
