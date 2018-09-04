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




"""
if __name__ == '__main__':
    partitions = 6
    for i in range(partitions):
        for x in word_generator("l", 4, "{}/{}".format(i+1, partitions)):
            print(x)
        print()
"""

