from getpass import getuser
from platform import platform
import requests
import uuid

class Client:
  def __init__(self):
    self.os = platform()
    self.user = getuser()
    self.__uuid = uuid.uuid4()

  def authenticate(self):
    pass

  def get_task(self):
    pass

  def deliver_task(self):
    pass

  def __str__(self):
    return f'{self.os} {self.user}'

if __name__ == '__main__':
  client = Client()
