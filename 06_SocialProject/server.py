import asyncio
import shlex
import cowsay


HOST = '0.0.0.0'
PORT = 1337


class Server:

	_clients = {}
	_available_cows = set(cowsay.list_cows())


	def __init__(self, host=HOST, port=PORT):
		self.host = host
		self.port = port

	async def chat(self, reader, writer):
		ID = '{}:{}'.format(*writer.get_extra_info('peername'))
		personal_queue = asyncio.Queue()
		send = asyncio.create_task(reader.readline())
		receive = asyncio.create_task(personal_queue.get())
		connected = True

		while connected and not reader.at_eof():
			done, pending = await asyncio.wait([send, receive], 
				return_when=asyncio.FIRST_COMPLETED)
			for task in done:
				if task is send:
					send = asyncio.create_task(reader.readline())
					message = task.result().decode().strip()
					match shlex.split(message):
						case ['who']:
							response = ' '.join(self._clients.keys()) \
								if self._clients else 'No registered clients'
							await personal_queue.put(response)
						case ['service_who']:
							response = ' '.join(self._clients.keys()) \
								if self._clients else 'No registered clients'
							await personal_queue.put('?' + response)
						case ['cows']:
							await personal_queue.put(
								' '.join(self._available_cows))
						case ['service_cows']:
							await personal_queue.put(
								'?' + ' '.join(self._available_cows))
						case ['login', name] if ID not in self._clients.keys():
							if name in self._available_cows:
								ID = name
								self._clients[ID] = personal_queue
								self._available_cows.remove(ID)
								await personal_queue.put(
									f'You are successfully registered as {ID}')
						case ['say', name, text] if ID in self._clients.keys():
							if name in self._clients.keys():
								await self._clients[name].put(
									cowsay.cowsay(text, cow=ID))
						case ['yield', text] if ID in self._clients.keys():
							for q in self._clients.values():
								if q is not personal_queue:
									await q.put(cowsay.cowsay(text, cow=ID))
						case ['quit']:
							connected = False
							self._available_cows.add(ID)
							await personal_queue.put('You successfully exited')
						case _:
							await personal_queue.put('Wrong command')
				elif task is receive:
					receive = asyncio.create_task(personal_queue.get())
					writer.write(f'{task.result()}\n'.encode())
					await writer.drain()

		send.cancel()
		receive.cancel()
		if ID in self._clients.keys():
			del self._clients[ID]
		writer.close()
		await writer.wait_closed()

	def start(self):
		async def routine():
			server = await asyncio.start_server(
				self.chat, self.host, self.port)
			async with server:
				await server.serve_forever()

		asyncio.run(routine())


if __name__ == '__main__':
	server = Server()
	server.start()