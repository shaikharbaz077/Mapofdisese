heroku ps:scale web=1
web: gunicorn app:app
collectstatic --noinput
heroku config:set DEBUG_COLLECTSTATIC=1
