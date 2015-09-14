from astute_auth import settings
import mandrill


class ProspectEmail:
	def __init__(self):
		pass

	@staticmethod
	def send(email):
		mandrill_client = mandrill.Mandrill(settings.MANDRILL_APIKEY)
		message = {
			'from_email': settings.PROSPECT_EMAIL_FROM,
			'from_name': settings.PROSPECT_EMAIL_FROM_NAME,
			'html': settings.PROSPECT_EMAIL_BODY,
			'subject': settings.PROSPECT_EMAIL_SUBJECT,
			'to': [
				{
					'email': email,
					'type': 'to'
				}
			]
		}
		mandrill_client.messages.send(message=message)
