# celerybot
Example of telegram bot using celery

To run the webapp: python webapp.py

To run the worker: celery worker -A tasks --queues=bot_messages --loglevel=INFO

Have Fun!
