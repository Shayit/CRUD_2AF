import pyotp
import qrcode

def generate_secret():
    return pyotp.random_base32()

def generate_otp_url(secret, username, issuer="MiApp"):
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=username, issuer_name=issuer)

def verify_otp(secret, otp_code):
    totp = pyotp.TOTP(secret)
    return totp.verify(otp_code)

def generate_qr(otp_auth_url):
    qr = qrcode.make(otp_auth_url)
    qr.show()