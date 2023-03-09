import cowsay
import cmd
import readline
import shlex


class CowShell(cmd.Cmd):
	intro = 'Welcome to the cow shell!'
	prompt = '(cow) '


	def do_make_bubble(self, args):
		"""
		Wraps text if -t (wrap_text) is true, then pads text and sets inside a bubble.
    	This is the text that appears above the cows

    	param: message - message to be displayed in bubble
    	param: -b - cowsay or cowthink
    	param: -w - width of bubble
    	param: -t - wrap text or not
		"""
		text, *optional_params = shlex.split(args, comments=True)

		FLAGS = {'-b': 'brackets', '-w': 'width', '-t': 'wrap_text'}
		params = {'brackets': cowsay.THOUGHT_OPTIONS['cowsay'], 'width': 40, 'wrap_text': True}
		while optional_params:
			flag, value, *optional_params = optional_params
			match flag:
				case '-w':
					params[FLAGS[flag]] = int(value)
				case '-b':
					params[FLAGS[flag]] = cowsay.THOUGHT_OPTIONS[value]
				case '-t':
					params[FLAGS[flag]] = value
				case _:
					raise Exception('Wrong arguments')

		try:
			print(cowsay.make_bubble(text, **params))
		except:
			raise Exception('Wrong arguments')


	def complete_make_bubble(self, text, line, begidx, endidx):
		COMPLETIONS = {'-b', '-w', '-t'}
		parsed = shlex.split(line)

		if len(parsed) < 2 or text in COMPLETIONS:
			#Line without parameter 'message'
			#or text is from completions
			return []

		if len(parsed) == 2:
			return list(COMPLETIONS) if not text else []

		if parsed[-1] in COMPLETIONS and parsed.count(parsed[-1]) > 1:
			#Multiple occurences of the same flag
			return []

		match parsed[-1]:
			case '-b':
				return ['cowsay', 'cowthink']
			case '-w':
				return ['40']
			case '-t':
				return ['True']
			case _:
				if parsed[-2] == '-b' and text:
					return [br for br in ['cowsay', 'cowthink'] if br.startswith(parsed[-1])]

				return list(COMPLETIONS - set(parsed))


	def do_list_cows(self, args):
		"""Lists all cow file names in the given directory"""
		try:
			if args:
				print(cowsay.list_cows(args))
			else:
				print(cowsay.list_cows())
		except:
			raise Exception('Wrong arguments')


	def do_cowsay(self, args):
		"""
		Similar to the Linux cowsay command of cowsay. Returns the resulting cowsay string

	    :param message: The message to be displayed
	    :param cow: -f - the available cows
	    :param eyes: -e - the eyes of cow
	    :param tongue: -t - the tongue of cow
		"""
		message, *optional_params = shlex.split(args, comments=True)

		FLAGS = {'-f': 'cow', '-e': 'eyes', '-t': 'tongue'}
		params = {'cow': 'default', 'eyes': cowsay.Option.eyes, 'tongue': cowsay.Option.tongue}
		while optional_params:
			try:
				flag, value, *optional_params = optional_params
				params[FLAGS[flag]] = value
			except:
				raise Exception('Wrong arguments')

		try:
			print(cowsay.cowsay(message, **params))
		except:
			raise Exception('Wrong arguments')


	def complete_cowsay(self, text, line, begidx, endidx):
		COMPLETIONS = {'-f', '-e', '-t'}
		parsed = shlex.split(line)

		if len(parsed) < 2 or text in COMPLETIONS:
			#Line without parameter 'message'
			#or text is from completions
			return []

		if len(parsed) == 2:
			return list(COMPLETIONS) if not text else []

		if parsed[-1] in COMPLETIONS and parsed.count(parsed[-1]) > 1:
			#Multiple occurences of the same flag
			return []

		matching = parsed[-1] if parsed[-1] in COMPLETIONS or not text else parsed[-2]

		match matching:
			case '-f':
				COWS = cowsay.list_cows()
				return [cow for cow in COWS if cow.startswith(text)]
			case '-e':
				EYES = ['oo', '00', 'XX', '**', '--', '..']
				return [eye for eye in EYES if eye.startswith(text)]
			case '-t':
				TONGUES = ['U ', '  ', 'ww ', 'S ']
				return [tongue for tongue in TONGUES if tongue.startswith(text)]
			case _:
				return list(COMPLETIONS - set(parsed))


	def do_cowthink(self, args):		
		"""
		Similar to the Linux cowthink command of cowsay. Returns the resulting cowthink string

	    :param message: The message to be displayed
	    :param cow: -f – the available cows
	    :param eyes: -e
	    :param tongue: -t
		"""
		message, *optional_params = shlex.split(args, comments=True)

		FLAGS = {'-f': 'cow', '-e': 'eyes', '-t': 'tongue'}
		params = {'cow': 'default', 'eyes': cowsay.Option.eyes, 'tongue': cowsay.Option.tongue}
		while optional_params:
			try:
				flag, value, *optional_params = optional_params
				params[FLAGS[flag]] = value
			except:
				raise Exception('Wrong arguments')

		try:
			print(cowsay.cowthink(message, **params))
		except:
			raise Exception('Wrong arguments')


	def complete_cowthink(self, text, line, begidx, endidx):
		return self.complete_cowsay(text, line, begidx, endidx)


if __name__ == '__main__':
	CowShell().cmdloop()