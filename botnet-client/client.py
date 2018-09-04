from getpass import getuser
from platform import platform
import requests
import uuid
from cracker import Cracker
import time

class Client:
  URL = 'http://localhost:8000'

  def __init__(self):
    self.os = platform()
    self.user = getuser()
    self._uuid = uuid.uuid4()
    self.cracker = Cracker()
    self.task_id = -1

  def __str__(self):
    return '{} {}'.format(self.os, self.user)

  def get_headers(self):
    return {
      'Authorization': 'Token {}'.format(self._uuid),
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
      self.parse_command(response['command'])
    # No recibe la tarea, asique aca hay que poner el comando. Por ahora es un solo hash
    self.parse_command('bruteforce -h 5f249886559f87d1cf8ccaadedd6e11f76c53629 -a sha1 -s lllldd -l 5 -p 1/10')

  def deliver_task(self, answer):
    url = '{}/delivery/'.format(Client.URL)
    requests.post(url, headers=self.get_headers(), data={
      'task_id': self.task_id,
      'answer': answer,
    })

  def parse_command(self, command):
    command_list = command.split()
    if command_list[0] == 'bruteforce':
      hash_to_crack = command_list[command_list.index('-h') + 1]
      algorithm = command_list[command_list.index('-a') + 1]
      char_set = command_list[command_list.index('-s') + 1]
      t = time.time()
      self.cracker.brute_force_cracking([hash_to_crack], algorithm, char_set)
      print('TOTAL TIME', time.time() - t)

if __name__ == '__main__':
  client = Client()
  client.authenticate()
  client.get_task()
