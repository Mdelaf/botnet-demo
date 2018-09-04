from getpass import getuser
from platform import platform
import requests
import uuid
import hashlib

class Client:
  URL = 'http://localhost:8000'

  def __init__(self):
    self.os = platform()
    self.user = getuser()
    self._uuid = uuid.uuid4()
    self.task_id = -1

  def get_headers(self):
    return {
      'Authorization': 'Token {}'.format(self._uuid),
    }

  def brute_force_cracking(self, hash_to_crack, algorithm, char_set):
    if algorithm == 'md5':
      hash_algorithm = hashlib.md5
    else:
      hash_algorithm = hashlib.sha1
    hash_object = hash_algorithm(b'hola').hexdigest()
    if hash_object == hash_to_crack:
      print(True)
    print(False)

  def parse_command(self, command):
    command_list = command.split()
    if command_list[0] == 'bruteforce':
      hash_to_crack = command_list[command_list.index('-h') + 1]
      algorithm = command_list[command_list.index('-a') + 1]
      char_set = command_list[command_list.index('-s') + 1]
      return self.brute_force_cracking(hash_to_crack, algorithm, char_set)

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
      self.parse_command(response['command'])
    self.parse_command('bruteforce -h 925d7518fc597af0e43f5606f9a51512 -a sha1 -s ld -l 8 -p 3/5')

  def deliver_task(self, answer):
    url = '{}/delivery/'.format(Client.URL)
    requests.post(url, headers=self.get_headers(), data={
      'task_id': self.task_id,
      'answer': answer,
    })
    # check this request

  def __str__(self):
    return '{} {}'.format(self.os, self.user)

if __name__ == '__main__':
  client = Client()
  client.authenticate()
  client.get_task()
