import docker

client = docker.from_env()


def runcontainer(image):
    container = client.containers.run(image, detach=True)
    print("Container started with ID: {}".format(container.id))


def runcontainerwithport(image, binding):
    container = client.containers.run(image, detach=True, ports=binding)
    print("Container started with ID: {}".format(container.id))


def listcontainers():
    for container in client.containers.list():
        print(container.id)


def stopall():
    for container in client.containers.list():
        container.stop()


def printlogs(container_id):
    container = client.containers.get(container_id)
    print(container.logs())


def listimages():
    for image in client.images.list():
        print(image.id)


def pullimage(imagename):
    image = client.images.pull(imagename)
    print(image.id)


def commitcontainer(container_id, commitname):
    container = client.containers.get(container_id)
    image = container.commit(commitname)
    print(image.id)
