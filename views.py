# -*- coding: utf-8 -*-
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask


class Field:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.letter_dictionary = {'A': 1, 'B': 2, 'C': 3, 'D': 4, "E": 5, "F": 6, 'G': 7, 'H': 8}

    def check_is_correct(self) -> bool:
        if 0 <= self.x <= 8 and 0 <= self.y <= 8:
            return True
        else:
            return False

    def change_to_numbers(self, letter):
        return self.letter_dictionary[letter]



