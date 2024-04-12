import smtplib


def send_mail(to_address, otp):
    passwd = 'bsbcujgyqydcefac'

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login("securefaceauthentication@gmail.com", passwd)

    subject = "OTP FOR YOUR FACE RE-REGISTRATION."
    message = f"OTP for you face re-registration is {otp}"

    message = f"Subject: {subject}\n\n{message}"

    s.sendmail("yforyadhu2003@gmail.com", to_address, message)

    s.quit()


