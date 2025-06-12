import pyotp
from importlib import reload
from qr_auth import qr, config


def test_generate_and_verify(monkeypatch):
    secret = pyotp.random_base32()
    monkeypatch.setenv('SECRET_KEY', secret)
    monkeypatch.setenv('BRANCH_ID', '1')
    reload(config)
    reload(qr)

    code = qr.generate_code()
    assert qr.verify_code(code)

    wrong = code[:-1] + ('0' if code[-1] != '0' else '1')
    assert not qr.verify_code(wrong)
