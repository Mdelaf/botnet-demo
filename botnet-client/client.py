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
import string


CHARSETS = {
    "l": string.ascii_lowercase,
    "L": string.ascii_uppercase,
    "d": string.digits,
    "s": string.punctuation
}


class WordGenerator:

    def __init__(self, charset, start_from=0):
        self.charset = charset
        self.cardinality = len(charset)
        self.cursor = [0]
        if start_from != 0:
            self.move_start(start_from)

    def move_start(self, position):
        current_position = 0
        current_length = 1
        while (self.cardinality ** current_length) + current_position <= position:
            current_position += self.cardinality ** current_length
            current_length += 1
        self.cursor = [0 for _ in range(current_length)]

        if position > current_position:
            difference = position - current_position

            for i in range(len(self.cursor)):
                if difference == 0:
                    break
                add = self.cursor[i] + difference
                difference = add // self.cardinality
                rest = add % self.cardinality
                self.cursor[i] = rest

    def iterations(self, number):
        k = 0

        while k < number:
            yield "".join(self.charset[index] for index in self.cursor[::-1])

            pointer = 0
            if self.cursor[pointer] < self.cardinality - 1:
                self.cursor[pointer] += 1

            else:
                increased_length = False  #
                while self.cursor[pointer] == self.cardinality - 1:
                    self.cursor[pointer] = 0
                    pointer += 1

                    if pointer == len(self.cursor):
                        self.cursor.append(0)  #
                        increased_length = True  #

                if not increased_length:  #
                    self.cursor[pointer] += 1

            k += 1


def word_generator(charset, max_length, partition):
    """
    :param charset: [str] only contains l, L, d or s
    :param max_length: [int] >= 1
    :param partition: [str] in format 'n/d' where 1 <= n <= d
    :return: [generator of str]
    """
    chars = ""
    for c in charset:
        chars += CHARSETS[c]

    chars_number = len(chars)
    total_strings = 0
    for i in range(1, max_length + 1):
        total_strings += chars_number ** i

    partition_number, total_partitions = partition.split("/")
    partition_number, total_partitions = int(partition_number), int(total_partitions)

    partition_size = total_strings // total_partitions
    start_iteration = partition_size * (partition_number - 1)

    if partition_number == total_partitions:
        partition_size = total_strings - start_iteration

    wg = WordGenerator(chars, start_iteration)
    return wg.iterations(partition_size)


class Client:
    URL = 'https://iic2523.pythonanywhere.com'

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
