import cmd
import threading
import time
import readline
import socket
import shlex


SOCKET_SIZE = 1024
HOST = 'localhost'
PORT = 1337


class Client(cmd.Cmd):

	intro = '<<<Welcome to CowChat!>>>'
	prompt = '(CowChat) '

	_service_buffer = ''


	def __init__(self, *args, **params):
		super().__init__(*args, **params)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((HOST, PORT))

	def do_cows(self, args):
		if args:
			print('Wrong arguments')
		else:
			self.socket.send('cows\n'.encode())

	def do_login(self, args):
		match shlex.split(args):
			case [name]:
				self.socket.send(f'login {name}\n'.encode())
			case _:
				print('Wrong arguments')

	def do_say(self, args):
		match shlex.split(args):
			case [name, text]:
				self.socket.send(f'say {name} "{text}"\n'.encode())
			case _:
				print('Wrong arguments')

	def do_who(self, args):
		if args:
			print('Wrong arguments')
		else:
			self.socket.send('who\n'.encode())

	def do_yield(self, args):
		match shlex.split(args):
			case [text]:
				self.socket.send(f'yield "{text}"\n'.encode())
			case _:
				print('Wrong arguments')

	def do_quit(self, args):
		if args:
			print('Wrong arguments')
		else:
			self.socket.send('quit\n'.encode())
			return True

	def complete_login(self, text, line, begidx, endidx):
		self.socket.send('service_cows\n'.encode())

		while not (available_cows := self._service_buffer):
			continue

		self._service_buffer = ''

		return [cow for cow in available_cows.split() if cow.startswith(text)]

	def complete_say(self, text, line, begidx, endidx):
		self.socket.send('service_who\n'.encode())

		while not (registered_cows := self._service_buffer):
			continue

		self._service_buffer = ''

		if registered_cows == 'No registered clients':
			return []

		return [cow for cow in registered_cows.split() if cow.startswith(text)]

	def receive(self):
		while True:
			response = self.socket.recv(SOCKET_SIZE).decode().strip()

			if not response:
				break

			if response.startswith('?'):
				self._service_buffer = response.lstrip('? ')
			else:
				print(f"\n{response}\n{readline.get_line_buffer()}", end="", flush=True)


if __name__ == '__main__':
	client = Client()
	receiver = threading.Thread(target=client.receive, args=())
	receiver.start()
	client.cmdloop()