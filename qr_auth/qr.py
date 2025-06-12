import base64
import pyotp
import qrcode
from io import BytesIO
from . import config


def _ensure_base32(secret: str) -> str:
    """Return a base32-encoded secret for TOTP.

    If the provided secret is already valid base32, it is returned as-is.
    Otherwise the raw string is encoded to base32.
    """
    try:
        base64.b32decode(secret, casefold=True)
        return secret
    except Exception:
        return base64.b32encode(secret.encode()).decode()


otp = pyotp.TOTP(_ensure_base32(config.SECRET_KEY), interval=30)


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
