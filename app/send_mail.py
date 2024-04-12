import smtplib
from .CREDS import APP_PASSWORD, EMAIL


def send_mail(to_address, otp):
    passwd = APP_PASSWORD

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(EMAIL, passwd)

    subject = "OTP FOR YOUR FACE RE-REGISTRATION."
    message = f"OTP for you face re-registration is {otp}"

    message = f"Subject: {subject}\n\n{message}"

    s.sendmail(EMAIL, to_address, message)

    s.quit()


