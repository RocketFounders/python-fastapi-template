from core.registry import CELERY as app


@app.task
def task():
    with open("~/Desktop/hello.txt", "w") as f:
        f.write("hello world")
