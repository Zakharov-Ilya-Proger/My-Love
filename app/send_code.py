import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings import settings

def send_email(to_email, subject, body):
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    email_address = settings.GMAIL_ADDRESS
    email_password = settings.GMAIL_PASSWORD

    msg = MIMEMultipart("alternative")
    msg['From'] = email_address
    msg['To'] = to_email
    msg['Subject'] = subject

    html_body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                padding: 20px 0;
                background-color: #007bff;
                color: #fff;
                border-radius: 5px 5px 0 0;
            }}
            .content {{
                padding: 20px;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                color: #fff;
                background-color: #007bff;
                text-align: center;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }}
            .button:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Password Reset</h1> <br>
                <p>{body}</p>
            </div>
            <div class="content">
                <a href="https://yourwebsite.com/password_reset_form" class="button">Go to Password Reset Form</a>
            </div>
        </div>
    </body>
    </html>
    """

    # Прикрепление HTML тела к письму
    msg.attach(MIMEText(html_body, 'html'))

    # Отправка письма
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(email_address, email_password)
        server.send_message(msg)
        print('Письмо отправлено успешно!')
