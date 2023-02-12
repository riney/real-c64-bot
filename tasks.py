from invoke import task

@task
def containers(c):
    c.run("scripts/build_containers.sh")

@task
def test(c):
    c.run("docker run realc64bot/test -it pytest")
