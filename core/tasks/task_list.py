from tasks.celery_app import CELERY


@CELERY.task
def task():
    with open("~/Desktop/hello.txt", "w") as f:
        f.write("hello world")
