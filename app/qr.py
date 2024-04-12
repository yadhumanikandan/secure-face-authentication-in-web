import qrcode  # type: ignore


def generate_qrcode_png(data, file_name):
    img = qrcode.make(data)

    path = f"app/static/qr/{file_name}.png"

    img.save(path)


generate_qrcode_png("https://google.com", "test")
