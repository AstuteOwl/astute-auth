from astute_auth import settings
import mandrill


class VerificationEmail:
	def __init__(self):
		pass

	@staticmethod
	def send(email, validation_key):
		mandrill_client = mandrill.Mandrill(settings.MANDRILL_APIKEY)
		message = {
			'from_email': settings.VALIDATION_EMAIL_FROM,
			'from_name': settings.VALIDATION_EMAIL_FROM_NAME,
			'html': settings.VALIDATION_EMAIL_BODY.format(email=email, validation_key=validation_key),
			'subject': settings.VALIDATION_EMAIL_SUBJECT,
			'to': [
				{
					'email': email,
					'type': 'to'
				}
			]
		}
		mandrill_client.messages.send(message=message)
