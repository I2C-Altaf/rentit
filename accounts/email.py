import random, math
import smtplib


def send_otp_email(user_email):
    digits="0123456789"
    OTP=""
    for i in range(4):
        OTP+=digits[math.floor(random.random()*10)]

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    admin_email = "al.idea2code@gmail.com"
    gsub = "OTP for Rent-It"
    msg = OTP + " is the OTP for Rent-It. Please Don't Share it with anyone."


    gmsg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nMessage: %s\r\n" % (admin_email, user_email, gsub, OTP)
    s.login(admin_email, "kaqauhpxpjbyvwrf")

    s.sendmail(admin_email,user_email,gmsg+msg)

    return OTP