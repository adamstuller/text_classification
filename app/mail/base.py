import os
from sendgrid import SendGridAPIClient
from app.config import config

sg = SendGridAPIClient(config['sendgrid']['api_key'])