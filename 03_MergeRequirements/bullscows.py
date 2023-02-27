import sys
from collections import Counter
from random import choice
from urllib.request import urlopen
from os.path import isfile


def bullscows(guess: str, secret: str) -> (int, int):
	bulls = sum(map(str.__eq__, guess, secret))
	cows = (Counter(guess) & Counter(secret)).total()

	return bulls, cows


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
	secret = choice(words)
	numberOfAttempts = 0

	guess = ''
	while guess != secret:
		numberOfAttempts += 1
		guess = ask('Введите слово: ', words)
		bulls, cows = bullscows(guess, secret)
		inform('Быки: {}, Коровы: {}', bulls, cows)

	return numberOfAttempts


def ask(prompt: str, valid: list[str] = None) -> str:
	guess = input(prompt)

	while valid and guess not in valid:
		guess = input(prompt)

	return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
	print(format_string.format(bulls, cows))


def getDict(dictionary: str, wordLength: int) -> list[str]:
	if isfile(dictionary):
		with open(dictionary, 'rb') as f:
			allWords = f.read().decode().split()
	else:
		with urlopen(dictionary) as f:
			allWords = f.read().decode().split()

	return [word for word in allWords if len(word) == wordLength]


match sys.argv:
	case [prog, dictionary, *wordLength]:
		wordLength = int(wordLength[0]) if wordLength else 5

		try:
			words = getDict(dictionary, wordLength)
		except:
			print('Invalid dictionary')
			exit()

		numberOfAttempts = gameplay(ask, inform, words)
		print(numberOfAttempts)
		
	case _:
		print('Invalid command')