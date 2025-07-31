import os
from celery import Celery
import requests
import io
from xhtml2pdf import pisa
from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv
load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")
celery = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)


CHOC_EMAIL = os.getenv("CHOC_EMAIL")
CHOC_PASSWORD = os.getenv("CHOC_PASSWORD")
SECRET = os.getenv("SECRET")
SECRET_URL = os.getenv("SECRET_URL")

@celery.task(name='tasks.send_invoice_email_task')
def send_invoice_email(order_id, user_email):
    try:
        # Pull rendered invoice HTML from Flask app
        url = f"{SECRET_URL}/{order_id}/{SECRET}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch invoice HTML: {response.status_code}")
            return False

        invoice_html = response.text

        # Create PDF from HTML
        pdf_stream = io.BytesIO()
        pisa_status = pisa.CreatePDF(invoice_html, dest=pdf_stream)
        if pisa_status.err:
            print("PDF generation error")
            return False

        pdf = pdf_stream.getvalue()

        # Build email message
        msg = EmailMessage()
        msg['Subject'] = f"Your Invoice - {order_id}"
        msg['From'] = CHOC_EMAIL
        msg['To'] = user_email
        msg.set_content("Thanks for your order! Your invoice is attached.")
        msg.add_attachment(pdf, maintype='application', subtype='pdf', filename=f"Invoice_{order_id}.pdf")

        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user=CHOC_EMAIL, password=CHOC_PASSWORD)
            smtp.send_message(msg)

        pdf_stream.close()
        print("Invoice emailed successfully.")
        return True

    except Exception as e:
        print(f"[Invoice/Email Error]: {e}")
        return False



###celery -A tasks worker --loglevel=info --pool=solo
