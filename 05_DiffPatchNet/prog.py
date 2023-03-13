import asyncio
import cowsay
import shlex


BUFFER_SIZE = 1000


clients = {}
pending_clients = {}


async def write_message(writer, message):
	message += '\n'
	writer.write(message.encode())
	await writer.drain()


async def client(reader, writer):
	ID = '{}:{}'.format(*writer.get_extra_info('peername'))
	pending_clients[ID] = asyncio.Queue()
	connected = True

	send = asyncio.create_task(reader.read(BUFFER_SIZE))
	receive = asyncio.create_task(pending_clients[ID].get())
	while connected and not reader.at_eof():
		done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)

		for task in done:
			message = task.result().decode().strip()

			if task is send:
				send = asyncio.create_task(reader.read(BUFFER_SIZE))
				if ID in pending_clients.keys():
					#client's registering
					match shlex.split(message):
						case ['who']:
							if clients:
								await write_message(writer, 'Registered clients: ' + 
									', '.join(clients.keys()))
							else:
								await write_message(writer, 'No registered clients')
						case ['cows']:
							available_cows = set(cowsay.list_cows()) - clients.keys()
							await write_message(writer, 'Available cow names: ' +
									', '.join(available_cows))
						case ['login', name]:
							available_cows = set(cowsay.list_cows()) - clients.keys()
							if name in available_cows:
								del pending_clients[ID]
								receive.cancel()
								ID = name
								clients[ID] = asyncio.Queue()
								receive = asyncio.create_task(clients[ID].get())
								await write_message(writer, f'You are successfully registered as {ID}')
							else:
								await write_message(writer, 'This name is not available')
						case ['quit']:
							connected = False
							await write_message(writer, 'You successfully exited')
						case _:
							await write_message(writer, 'Wrong command')

				else:
					#client is registered
					match shlex.split(message):
						case ['who']:
							if clients:
								await write_message(writer, 'Registered clients: ' + 
									', '.join(clients.keys()))
							else:
								await write_message(writer, 'No registered clients')
						case ['cows']:
							available_cows = set(cowsay.list_cows()) - clients.keys()
							await write_message(writer, 'Available cow names: ' +
									', '.join(available_cows))
						case ['say', name, text]:
							if name not in clients.keys():
								await write_message(writer, f'No registered client with name {name}')
							else:
								await clients[name].put(text.encode())
						case ['yield', text]:
							for out in clients.values():
								if out is not clients[ID]:
									await out.put(text.encode())
						case ['quit']:
							connected = False
							await write_message(writer, 'You successfully exited')
						case _:
							await write_message(writer, 'Wrong command')

			elif task is receive:
				receive = asyncio.create_task(clients[ID].get())
				await write_message(writer, message)

	send.cancel()
	receive.cancel()
	
	if ID in pending_clients.keys():
		del pending_clients[ID]
	else:
		del clients[ID]
	
	writer.close()
	await writer.wait_closed()


async def main():
	server = await asyncio.start_server(client, '0.0.0.0', 1337)
	async with server:
		await server.serve_forever()


asyncio.run(main())