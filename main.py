from infraestructura import contenedor, red, imagen
import os


parent_dir = os.path.dirname(os.path.realpath(__file__))
html_dir = '{}/html'.format(parent_dir)

img = imagen()

print("Descargando imagen, espere unos minutos....")
img_APP = img._pull('php:7.2-apache')
print(img_APP)

INFRAESTRUCTURA = \
    {'image': 'php:7.2-apache',
     'name': 'contenedor_php',
     'ports': {'80/tcp': 80},
     'links': {},
     'entrypoint': '',
     'environment': [],
     'cap_add': [],
     'network': '',
     'mac_address': '00:00:00:00:00:03',
     'volumes': {html_dir: \
                     {'bind': '/var/www/html', 'mode': 'rw'}}
     }

print("Para y remueve contenedor ...")
ctr = contenedor(INFRAESTRUCTURA)
ctr.stop()
ctr.remove()

print("Reinicia contenedor, espere unos minutos...")
ctr = contenedor(INFRAESTRUCTURA)
ctr.create()
while True:
    edo = ctr.status()
    if edo == 'CREATED':
        ctr.start()
    elif edo == 'RUNNING':
        break

print("Directorio de trabajo")
if ctr.status() == 'RUNNING':
    r = ctr.execute('ls', '/var/www/html')
    print(r)
