# Email Proxy Service

En lättviktig mikrotjänst för att skicka e-post via ett lokalt API. Perfekt för notifieringar från Home Assistant eller andra skript i ditt hem.

## API-anrop

Tjänsten tar emot POST-anrop på /send med en JSON-body.

### Parametrar

* subject (sträng): Rubriken på mejlet.
* body (sträng): Meddelandet i mejlet.
* to (valfritt, sträng eller lista av strängar): Mottagare. Om du utelämnar denna används standardmottagarna från inställningarna (.env).

### Exempel

Skicka till en specifik person:
POST http://127.0.0.1:21964/send
Body: { "subject": "Larm", "body": "Diskutrymme lågt", "to": "admin@example.com" }

Skicka till flera personer:
POST http://127.0.0.1:21964/send
Body: { "subject": "Rapport", "body": "Backup klar", "to": ["mottagare1@example.com", "mottagare2@example.com"] }

Skicka till standardmottagare:
POST http://127.0.0.1:21964/send
Body: { "subject": "Status", "body": "Systemet körs" }

## Installation

1. Skapa en .env fil med dina uppgifter:
   EMAIL_USER=din-adress@gmail.com
   EMAIL_PASSWORD=ditt-app-lösenord
   EMAIL_TO=standard1@example.com,standard2@example.com

2. Installera nödvändiga paket:
   pip install fastapi uvicorn pydantic[email] python-dotenv

3. Starta tjänsten och anropa den via curl eller valfritt HTTP-verktyg.