import smtplib
from email.mime.text import MIMEText


def send_mail(customer, assistant, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '0d1888e44112eb'
    password = '0675ef4a40929e'
    message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>assistant: {assistant}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'sender_email@example.com'
    receiver_email = 'receiver_email@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'succulents rating Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())