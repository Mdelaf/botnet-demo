from getpass import getuser
from platform import platform
from threading import Thread

import urllib.request
import urllib.parse
import urllib.error
import json
import uuid
import hashlib
import time

from word_generator import word_generator


class Client:
    URL = 'http://localhost:8000'

    def __init__(self):
        self.os = platform()
        self.user = getuser()
        self._uuid = uuid.uuid4()
        self.task_id = None
        self.task_thread = None

    def get_headers(self):
        return {
            'Authorization': 'Token {}'.format(self._uuid)
        }

    def authenticate(self):
        url = '{}/auth/'.format(Client.URL)
        data = urllib.parse.urlencode({
            'user': self.user,
            'uid': self._uuid,
            'os': self.os,
        }).encode()
        try:
            req = urllib.request.Request(url, data=data, method='POST')
            response = urllib.request.urlopen(req)
        except urllib.error.URLError:
            return False

        if response.status == 204:
            return True
        return False

    def get_task(self):
        print('Talking to server..')
        url = '{}/tasks/'.format(Client.URL)
        req = urllib.request.Request(url, headers=self.get_headers(), method='GET')
        response = urllib.request.urlopen(req)
        response = json.loads(response.read().decode('utf-8'))
        if 'task_id' in response and 'command' in response:
            self.task_id = response['task_id']
            print('New task! -> ', response['command'])
            self.parse_command(response['command'])

    def deliver_task(self, answer):
        url = '{}/delivery/'.format(Client.URL)
        data = urllib.parse.urlencode({
            'task_id': self.task_id,
            'answer': answer,
        }).encode()
        req = urllib.request.Request(url, headers=self.get_headers(), data=data, method='POST')
        urllib.request.urlopen(req)

    def finished_task(self):
        url = '{}/finished/'.format(Client.URL)
        req = urllib.request.Request(url, headers=self.get_headers(), method='GET')
        urllib.request.urlopen(req)

    def parse_command(self, command):
        command_list = command.split()
        kwargs = {command_list[i]: command_list[i+1] for i in range(len(command_list)) if command_list[i].startswith("-")}
        if command_list[0] == 'bruteforce':
            print("Running task in a new thread")
            self.task_thread = Thread(target=self.bruteforce, kwargs=kwargs)
            self.task_thread.start()

    def bruteforce(self, **kwargs):
        hash_file_url = kwargs.get("-u")
        algorithm = kwargs.get("-a")
        char_set = kwargs.get("-s")
        length = int(kwargs.get("-l"))
        partition = kwargs.get("-p")

        response = urllib.request.urlopen(hash_file_url)
        hashes = [hash_.strip() for hash_ in response.read().decode('utf8').strip().split('\n')]

        if algorithm.lower() == 'md5':
            hash_algorithm = hashlib.md5
        else:
            hash_algorithm = hashlib.sha1

        for word in word_generator(char_set, length, partition):
            hash_object = hash_algorithm(bytes(word, 'utf-8')).hexdigest()
            try:
                pos = hashes.index(hash_object)
            except ValueError:
                continue
            else:
                answer = "{}: {}".format(hashes[pos], word)
                self.deliver_task(answer)
                print("Match found: " + answer)

        print("Finished task")
        self.finished_task()


if __name__ == '__main__':
    client = Client()

    while not client.authenticate():
        time.sleep(30)

    while True:
        client.get_task()
        time.sleep(30)
