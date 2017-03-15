from celery import Celery, Task
import telepot
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from celery.signals import worker_init
import time

LOCAL_BROKER = 'amqp://guest:guest@localhost/celerybot'

celery_app = Celery('tasks', broker=LOCAL_BROKER)
celery_app.conf.CELERY_ROUTES = {
        'reply_message': {
            'queue': 'bot_messages',
        }
}
logger = get_task_logger(__name__)


@worker_init.connect
def worker_start(sender, **kwargs):
    print('worker started')
    logger.error('Starting worker!')


class MyTask(Task):
    """An abstract Celery Task to perform any action on task completion"""
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        # to something
        logger.info('task completed!')
        pass


@celery_app.task(name="reply_message", bind=True, default_retry_delay=0.1, base=MyTask)
def reply_message(self, token, chat_id, message):
    bot = telepot.Bot(token)
    try:
        bot.sendChatAction(chat_id, "typing")
        time.sleep(0.5)
        bot.sendMessage(chat_id, u"That was she said:" + message)
    except Exception as err:
        self.retry(exc=err, max_retries=3, eta=datetime.now()+timedelta(minutes=1))
    logger.info("replied to {chat_id}".format(chat_id=chat_id))
    return 'OK'
