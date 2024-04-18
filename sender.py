import smtplib
import ssl 
from email.message import EmailMessage

subject = "Email from python"
body = "This is test"
sender_email = "youyou@gmail.com"
receiver_email = "youyou@gmail.com"
password = input("Enter a password: ")

message = EmailMessage()
message["from"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.set_content(body)

html = f"""
<html>
    <body>
        <h1>{subject}</h1>
        <p>{body}</p>
    </body>
</html>


"""


context = ssl.create_default_context()
print("sending Email")
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:

    server.login(sender_email,password)
    server.sendmail(sender_email,receiver_email,message.as_string)
print("sent!")

