from celery import Celery
from src.mail import create_message,mail
from asgiref.sync import async_to_sync

c_app = Celery()
c_app.config_from_object('src.config')


@c_app.task()
def send_email(receipients:list[str], subject:str, body:str):
    """
    Send email using Celery task.
    """
    
    message = create_message(recipients=receipients,subject=subject,body=body)
    
    async_to_sync(mail.send_message)(message)
    
    print("Email sent")
    
    
    