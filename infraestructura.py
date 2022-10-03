from io import BytesIO
import docker
import os


class imagen:
    def __init__(self):
        self.client = docker.from_env(version="auto")

    def _exists(self, tag):
        for c in self.client.images.list():
            if c.attrs['RepoTags']:
                if tag == c.attrs['RepoTags'][0]:
                    return c.attrs['RepoTags'][0]

    def _login(self, username, password):
        img = self.client.login(username=username, password=password)
        return img

    def _list_all(self):
        print
        ""
        print
        "{:15} {:30} {:20}".format('ID', 'TAG', 'SIZE MB')
        for c in self.client.images.list():
            if c.attrs['RepoTags']:
                print
                "{:15} {:30} {:20}".format( \
                    c.attrs['Id'].split(':')[1][:12], \
                    c.attrs['RepoTags'][0], \
                    str(c.attrs['Size'] / 1000000)[:20])

    def _create(self, dockerfile, tag):
        parent_dir = os.path.dirname(os.path.realpath(__file__))
        response = [line for line in \
                    self.client.images.build(path=parent_dir, \
                                             dockerfile=dockerfile, rm=True, tag=tag)]
        for r in response[1]:
            for key, value in r.iteritems():
                print
                str(value)

    def _pull(self, tag):
        img = self.client.images.pull(tag)
        return img


class red:
    def __init__(self, item):
        self.client = docker.from_env(version="auto")
        self.nombre = item['name']
        self.item = item
        if not self._exists():
            self.create()

    def _exists(self):
        c = self.client.networks.list()
        for n in c:
            if n.name == self.nombre:
                return n.name
        return None

    def create(self):
        if self.client:
            self.client.networks.create( \
                self.nombre, driver=self.item['driver'])

    def get_nombre(self):
        if self.client:
            return self.nombre

    def _list_all(self):
        c = self.client.networks.list()
        print
        ""
        print
        "{:30}".format("NOMBRE DE RED")
        for n in c:
            print(n.name)


class contenedor:
    def __init__(self, item):
        self.client = docker.from_env(version="auto")
        self.nombre = item['name']
        self.item = item

    def __exists(self):
        ret = None
        for c in self.client.containers.list(all=True):
            if self.nombre == c.attrs['Name'].split('/')[1]:
                ret = c
                break
        return ret

    def stop(self):
        self.c = self.__exists()
        if self.c:
            self.client.containers.model.stop(self.c)

    def start(self):
        self.c = self.__exists()
        if self.c:
            self.client.containers.model.start(self.c)

    def status(self):
        self.c = self.__exists()
        if self.c:
            return self.c.status.upper()
        else:
            return None

    def remove(self):
        self.c = self.__exists()
        if self.c:
            self.client.containers.model.remove(self.c)
            print
            ""
            print
            "Contenedor", \
            self.c.attrs['Name'].split('/')[1], "removido"
            print
            ""

    def info(self):
        self.c = self.__exists()
        if self.c:
            print
            " "
            print
            "{:15} {:20} {:15} {:30}".format( \
                'ID', 'NOMBRE', 'ESTADO', 'IMAGEN')
            print
            "{:15} {:20} {:15} {:30}".format( \
                str(self.c.attrs['Id'])[:12], \
                self.c.attrs['Name'].split('/')[1], \
                self.c.attrs['State']['Status'], \
                self.c.attrs['Config']['Image'])

    def create(self):
        self.c = self.__exists()
        if not self.c:
            self.client.containers.create( \
                image=self.item['image'], \
                name=self.item['name'], \
                ports=self.item['ports'], \
                links=self.item['links'], \
                environment=self.item['environment'], \
                volumes=self.item['volumes'], \
                entrypoint=self.item['entrypoint'], \
                cap_add=self.item['cap_add'], \
                mac_address=self.item['mac_address'], \
                network=self.item['network'], \
                detach=True, \
                tty=True, \
                init=True)

    def execute(self, command, pathdir):
        self.c = self.__exists()
        if self.c:
            if self.c.attrs['State']['Status'] == 'running':
                return self.client.containers.model. \
                    exec_run(self.c, cmd=command, tty=True, \
                             workdir=pathdir)
            else:
                return " El contenedor ", \
                       self.c.attrs['Name'].split('/')[1], \
                       " no esta en ejecucion. "

    def put_file(self, dir, datos):
        self.c = self.__exists()
        if self.c:
            if self.c.attrs['State']['Status'] == 'running':
                self.client.containers.model. \
                    put_archive(self.c, path=dir, data=datos)
            else:
                print
                ""
                print
                " El contenedor ", self.c.attrs['Name'].split('/')[1], \
                " no esta en ejecucion. "

    def logs(self):
        self.c = self.__exists()
        if self.c:
            if self.c.logs():
                for line in self.c.logs(stream=True):
                    print
                    line.strip()