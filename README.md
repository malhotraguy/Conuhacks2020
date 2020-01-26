1. Clone the repository
2. Go to the _python_ subdirectory
3. Update main.py to include your secret key and key ID from your [Smooch](https://app.smooch.io) settings
4. Install dependencies (`pip install -r requirements.txt`)
5. Run the server (`FLASK_APP=main.py flask run`)
6. Use [ngrok](https://ngrok.com/) to create a secure tunnel to port 5000(`ngrok http 5000` after ngrok is installed on your PC)
7. Create a Facebook page and [connect it to Smooch](https://app.smooch.io/integrations/messenger)
8. Create a Webhook from your [dashboard](https://app.smooch.io/integrations/webhook) and point it at the full url for the /messages endpoint (e.g. https://MY-NGROK-DOMAIN.ngrok.io/messages )
9. Send messages to your Facebook page and watch the auto-replies roll in
