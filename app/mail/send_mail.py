from sendgrid.helpers.mail import Mail
from app.config import config
from flask import current_app
import os
from .base import sg
from app.config import config


def send_mail_train_finished_notification(mailto, result):

    html_content = None

    if 'evaluation' in result:
        evaluation = result['evaluation']
        html_content = f"""
        <h2>You have successfully trained your pipeline!</h2>
<p style="font-size: 1.5em;">Name of your pipeline is  <strong >{result['name']}</strong> and you can access it on <strong>/api/v1/topics/{result['name']}/predict</strong> endpoint.</p>

<p style="font-size: 1.5em;">
  <strong>Pipeline description: </strong> {result['description']}
</p>

<p style="font-size: 1.5em;">
  Your pipeline's evaluation: 
 </p>
 <ul>
    <li>f1_macro: {evaluation['f1_macro']}</li>
    <li>f1_weighted: {evaluation['f1_weighted']}</li>
    <li>recall: {evaluation['recall']}</li>
    <li>precision: {evaluation['precision']}</li>
    <li>accuracy: {evaluation['accuracy']}</li>

</ul>


<p style="font-size: 1.5em;">Good luck using it!.</p>
        """
    else:
        html_content = """
        <h2>You have successfully trained your pipeline!</h2>
<p style="font-size: 1.5em;">Name of your pipeline is  <strong >{result['name']}</strong> and you can access it on <strong>/api/v1/topics/{result['name']}/predict</strong> endpoint.</p>

<p style="font-size: 1.5em;">
  <strong>Pipeline description: </strong> {result['description']}
</p>

<p style="font-size: 1.5em;">Good luck using it!.</p>
"""

    message = Mail(
        from_email=config['sendgrid']['mailfrom'],
        to_emails=mailto,
        subject='Pipeline trianing finished',
        html_content=html_content
    )

    return sg.send(message)
