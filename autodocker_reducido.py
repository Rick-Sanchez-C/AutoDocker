#!/usr/bin/env python3
import time
import docker
import os
client = docker.from_env()
def pullimage(imagename):
    image = client.images.pull(imagename)
    print(image.id)

def runcontainerwithport(image, binding):
    container = client.containers.run(image, detach=True, ports=binding)
    print("Container started with ID: {}".format(container.id))

image = 'httpd'
binding = {80: 8080}

print("Downloading Image...")
pullimage(image)
time.sleep(3)
print("Image downloaded")
print("Running container..")
runcontainerwithport(image, binding)
time.sleep(3)
print("Container running with the port binding " + str(binding))