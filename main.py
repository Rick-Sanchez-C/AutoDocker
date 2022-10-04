import time

import infraestructura
import os

image = 'httpd'
binding = {80: 8080}

print("Downloading Image...")
infraestructura.pullimage(image)
time.sleep(3)
print("Image downloaded")
print("Running container...")
infraestructura.runcontainerwithport(image, binding)
time.sleep(3)
print("Container running with the port binding " + str(binding))