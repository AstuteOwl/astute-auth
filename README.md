astute-auth
===========
Simple authentication using JWT intended to be deployed to Heroku.

Bootstrap
=========
If using Heroku you'll need to configure a few secrets and addons. This will also configure your .env file for local development.

	ASTUTE_AUTH_SECRET_KEY=somereallylongsecretkeythatisnotwhatyouseehere
	HMAC_SECRET_KEY=anotherlongkeytobeusedingeneratingthehmac
	DATABASE_URL=postgress://username:password@localhost/somedb

	heroku addons:create mandrill:starter
	heroku config:set ASTUTE_AUTH_SECRET_KEY=$ASTUTE_AUTH_SECRET_KEY
	heroku config:set HMAC_SECRET_KEY=$HMAC_SECRET_KEY
	# Don't set DATABASE_URL on Heroku, that is only for local development

	echo DATABASE_URL='$DATABASE_URL' >> .env
	echo ASTUTE_AUTH_SECRET_KEY='$ASTUTE_AUTH_SECRET_KEY' >> .env
	echo HMAC_SECRET_KEY='$HMAC_SECRET_KEY' >> .env

