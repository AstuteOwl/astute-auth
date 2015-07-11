astute-auth
===========
Simple authentication using JWT intended to be deployed to Heroku.

Bootstrap
=========
If using Heroku you'll need to configure a few secrets and addons. This will also configure your .env file for local development.

	ASTUTE_AUTH_SECRET_KEY=somereallylongsecretkeythatisnotwhatyouseehere
	HMAC_SECRET_KEY=anotherlongkeytobeusedingeneratingthehmac
	DATABASE_URL=postgress://username:password@localhost/somedb
	VALIDATION_EMAIL_FROM=noreply@yourdomain.com
	VALIDATION_EMAIL_FROM_NAME=My App
	VALIDATION_EMAIL_SUBJECT=My email subject
	VALIDATION_EMAIL_BODY=My email body
	
	heroku addons:create mandrill:starter
	heroku config:set ASTUTE_AUTH_SECRET_KEY=$ASTUTE_AUTH_SECRET_KEY
	heroku config:set HMAC_SECRET_KEY=$HMAC_SECRET_KEY
	heroku config:set VALIDATION_EMAIL_FROM=$VALIDATION_EMAIL_FROM
	heroku config:set VALIDATION_EMAIL_FROM_NAME=$VALIDATION_EMAIL_FROM_NAME
	heroku config:set VALIDATION_EMAIL_SUBJECT=$VALIDATION_EMAIL_SUBJECT
	heroku config:set VALIDATION_EMAIL_BODY=$VALIDATION_EMAIL_BODY
	# Don't set DATABASE_URL on Heroku, that is only for local development

	echo DATABASE_URL='$DATABASE_URL' >> .env
	echo ASTUTE_AUTH_SECRET_KEY='$ASTUTE_AUTH_SECRET_KEY' >> .env
	echo HMAC_SECRET_KEY='$HMAC_SECRET_KEY' >> .env
	echo MANDRILL_APIKEY=`heroku config:get MANDRILL_APIKEY` >> .env
	echo VALIDATION_EMAIL_FROM='$VALIDATION_EMAIL_FROM' >> .env
	echo VALIDATION_EMAIL_FROM_NAME='$VALIDATION_EMAIL_FROM_NAME' >> .env
	echo VALIDATION_EMAIL_SUBJECT='$VALIDATION_EMAIL_SUBJECT' >> .env
	echo VALIDATION_EMAIL_BODY='$VALIDATION_EMAIL_BODY' >> .env
