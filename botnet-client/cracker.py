import hashlib
import string
import time

class Cracker:
  def brute_force_cracking(self, hashes, algorithm, char_set):
    t = 0
    if algorithm == 'md5':
      hash_algorithm = hashlib.md5
    else:
      hash_algorithm = hashlib.sha1
    char_pool = Cracker.get_char_pool(char_set)
    Cracker.get_next_word(char_pool)
    for word in Cracker.get_next_word(char_pool):
      t1 = time.time()
      hash_object = hash_algorithm(bytes(word, 'utf-8')).hexdigest()
      t += time.time() - t1
      if hash_object == hashes[0]:
        print(word)
        print('HASHING TIME: ', t)
        break

  @staticmethod
  def get_positions(max_positions):
    positions = [0 for i in max_positions]
    yield positions
    while positions != max_positions:
      for n, position in enumerate(positions[::-1]):
        index = len(max_positions) - n - 1
        max_position = max_positions[index]
        if position == max_position:
          positions[index] = 0
          continue
        if position <= max_position:
          positions[index] += 1
          break
      yield positions

  @staticmethod
  def get_next_word(char_pool):
    max_positions = []
    for char_options in char_pool:
      max_positions.append(len(char_options) - 1)
    for position in Cracker.get_positions(max_positions):
      word = ''
      for n, char_options in enumerate(char_pool):
        word += str(char_options[position[n]])
      yield word

  @staticmethod
  def get_char_pool(char_set):
    letters = list(string.ascii_lowercase)
    upper_case_letters = list(string.ascii_uppercase)
    numbers = [n for n in range(10)]
    symbols = list(string.punctuation)
    char_pool = []
    for i in char_set:
      if i == 'l':
        char_pool.append(letters)
      elif i == 'L':
        char_pool.append(upper_case_letters)
      elif i == 'd':
        char_pool.append(numbers)
      elif i == 's':
        char_pool.append(symbols)
    return char_pool