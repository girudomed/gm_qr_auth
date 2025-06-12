import pyotp
import qrcode
from io import BytesIO
from . import config


otp = pyotp.TOTP(config.SECRET_KEY, interval=30)


def generate_code() -> str:
    code = otp.now()
    return f"{config.BRANCH_ID}:{code}"


def verify_code(payload: str) -> bool:
    try:
        branch, code = payload.split(":", 1)
    except ValueError:
        return False
    if branch != config.BRANCH_ID:
        return False
    return otp.verify(code)


def generate_qr() -> BytesIO:
    data = generate_code()
    img = qrcode.make(data)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf
