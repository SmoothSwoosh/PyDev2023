import sys
from collections import Counter
from random import choice
from urllib.request import urlopen
from os.path import isfile
from cowsay import cowsay, list_cows


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


def getRandomCow() -> str:
	return choice(list_cows())


def ask(prompt: str, valid: list[str] = None) -> str:
	message = cowsay(prompt, cowfile=cowfile) + '\n'
	guess = input(message)

	while valid and guess not in valid:
		message = cowsay(prompt, cowfile=cowfile) + '\n'
		guess = input(message)

	return guess if guess else input(message)


def inform(format_string: str, bulls: int, cows: int) -> None:
	message = cowsay(format_string.format(bulls, cows), cow=getRandomCow()) + '\n'
	print(message)


def getDict(dictionary: str, wordLength: int) -> list[str]:
	if isfile(dictionary):
		with open(dictionary, 'rb') as f:
			allWords = f.read().decode().split()
	else:
		with urlopen(dictionary) as f:
			allWords = f.read().decode().split()

	return [word for word in allWords if len(word) == wordLength]


COW_PATH = 'cow.file'
with open(COW_PATH, 'r') as f:
	cowfile = f.read()

match sys.argv:
	case [prog, dictionary, *wordLength]:
		wordLength = int(wordLength[0]) if wordLength else 5

		try:
			words = getDict(dictionary, wordLength)
		except:
			print('Invalid dictionary')
			exit()

		if not words:
			print('Dictionary doesn\'t contain words of such length')
			exit()

		numberOfAttempts = gameplay(ask, inform, words)
		print(numberOfAttempts)
		
	case _:
		print('Invalid command')