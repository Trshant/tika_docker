from celery import Celery

app = Celery('tasks', broker='amqp://localhost')

if __name__ == '__main__':
    app.start()