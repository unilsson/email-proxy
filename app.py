import os
import smtplib
from email.mime.text import MIMEText
from typing import List, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Standardmottagare från .env som backup
DEFAULT_RECIPIENTS = [email.strip() for email in os.getenv("EMAIL_TO", "").split(",") if email.strip()]

class EmailSchema(BaseModel):
    subject: str
    body: str
    # Tillåter en sträng (en adress) eller en lista av strängar (flera adresser)
    to: Union[EmailStr, List[EmailStr]] = None 

@app.post("/send")
def send_email(email: EmailSchema):
    # Logik: Använd 'to' från JSON om den finns, annars ta från .env
    recipients_input = email.to if email.to else DEFAULT_RECIPIENTS
    
    if not recipients_input:
        raise HTTPException(status_code=400, detail="Inga mottagare angivna.")

    # Se till att vi alltid jobbar med en lista
    recipients = [recipients_input] if isinstance(recipients_input, str) else recipients_input

    try:
        msg = MIMEText(email.body)
        msg["Subject"] = email.subject
        msg["From"] = os.getenv("EMAIL_USER")
        msg["To"] = ", ".join(recipients)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
            server.sendmail(msg["From"], recipients, msg.as_string())
        
        return {"status": "skickat", "to": recipients}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
