from . import qr

if __name__ == "__main__":
    img_bytes = qr.generate_qr()
    with open("qr.png", "wb") as f:
        f.write(img_bytes.getvalue())
    print("QR code saved to qr.png")
