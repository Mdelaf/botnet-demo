from getpass import getuser
from platform import platform
import requests
import uuid

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
      # do something
      pass

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
