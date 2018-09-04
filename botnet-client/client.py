from getpass import getuser
from platform import platform

import requests  # TODO: Ver si es mucho cacho usar urllib.request
import uuid
import hashlib

from word_generator import word_generator


class Client:
    URL = 'http://localhost:8000'

    def __init__(self):
        self.os = platform()
        self.user = getuser()
        self._uuid = uuid.uuid4()
        self.task_id = None

    def get_headers(self):
        return {
            'Authorization': 'Token {}'.format(self._uuid)
        }

    def authenticate(self):
        url = '{}/auth/'.format(Client.URL)
        requests.post(url, data={
          'user': self.user,
          'uid': self._uuid,
          'os': self.os,
        })

    def get_task(self):
        url = '{}/tasks/'.format(Client.URL)
        response = requests.get(url, headers=self.get_headers()).json()
        if 'task_id' in response and 'command' in response:
            self.task_id = response['task_id']
            # TODO: Eliminar esta linea después de las pruebas
            self.parse_command('bruteforce -h bf2d0283ea146823ac357b2bb08b8ee6 -a md5 -s ld -l 5 -p 1/3')
            # self.parse_command(response['command'])

    def deliver_task(self, answer):
        url = '{}/delivery/'.format(Client.URL)
        requests.post(url, headers=self.get_headers(), data={
          'task_id': self.task_id,
          'answer': answer,
        })

    def parse_command(self, command):
        command_list = command.split()
        kwargs = {command_list[i]: command_list[i+1] for i in range(len(command_list)) if command_list[i].startswith("-")}
        if command_list[0] == 'bruteforce':
            # TODO: Llamar al metodo en un thread aparte, así no se pierde la comunicacion con el servidor
            self.bruteforce(**kwargs)

    def bruteforce(self, **kwargs):
        # TODO: Eliminar -h e implementar -u (descargar archivo y guardar lista de hashes en variable)
        hash_to_crack = kwargs.get("-h")
        algorithm = kwargs.get("-a")
        char_set = kwargs.get("-s")
        length = int(kwargs.get("-l"))
        partition = kwargs.get("-p")

        if algorithm.lower() == 'md5':
            hash_algorithm = hashlib.md5
        else:
            hash_algorithm = hashlib.sha1

        for word in word_generator(char_set, length, partition):
            hash_object = hash_algorithm(bytes(word, 'utf-8')).hexdigest()
            # TODO: Comparar con todos los hashes de la lista
            if hash_object == hash_to_crack:
                # TODO: Si hay un match, llamar a deliver_task
                answer = "{}: {}".format(hash_to_crack, word)
                self.deliver_task(answer)


if __name__ == '__main__':
    client = Client()
    # TODO: Hacer un while True hasta que se autentique (por si el servidor esta off)
    client.authenticate()
    # TODO: Hacer un while True con sleep de 30 segs para pedir tasks de forma permanente
    client.get_task()
