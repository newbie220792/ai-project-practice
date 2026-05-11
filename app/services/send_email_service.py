import smtplib

def send_email(subject, body, to):
    # Implement your email sending logic here using smtplib or any email service provider API
    # Example using smtplib:
    sender_email = "example@gmail.com"
    sender_password = "password"    
    message = f"Subject: {subject}\n\n{body}"
    try:
        with smtplib.SMTP("google.smtp.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to, message)
    except Exception as e:
        print(f"Failed to send email: {e}") 
    
    