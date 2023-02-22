from invoke import task

@task
def vicetools_container(c):
    c.run("docker image build -f docker/Dockerfile.vicetools -t realc64bot/vicetools .")

@task
def base_container(c):
    c.run("docker image build -f docker/Dockerfile.base -t realc64bot/base .")

@task
def app_container(c):
    c.run("docker image build -f docker/Dockerfile.app -t realc64bot/app .")

@task(vicetools_container, base_container, app_container)
def all_containers(c):
    return

@task(app_container)
def test(c):
    c.run("docker run -it --env PYTHONPATH=src realc64bot/app pytest")
