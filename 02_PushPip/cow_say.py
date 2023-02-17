from cowsay import cowsay, list_cows
import argparse
import os


#These are several provided modes which change the appearance of the cow 
#depending on its particular emotional/physical state
MODES = "bdgpstwy"


#Create arguments' parser
parser = argparse.ArgumentParser(prog='Cowsay Baby!', description='My gosh. It can MOO!', epilog='The end')
parser.add_argument('-b', '--borg', dest='b', action='store_true', help='Initiates Borg mode')
parser.add_argument('-d', '--dead', dest='d', action='store_true', help='Causes the cow to appear dead')
parser.add_argument('-g', '--greedy', dest='g', action='store_true', help='Invokes greedy mode')
parser.add_argument('-p', '--paranoia', dest='p', action='store_true', help='Causes a state of paranoia to come over the cow')
parser.add_argument('-s', '--stoned', dest='s', action='store_true', help='Makes the cow appear thoroughly stoned')
parser.add_argument('-t', '--tired', dest='t', action='store_true', help='Yields a tired cow')
parser.add_argument('-w', '--wired', dest='w', action='store_true', help='Initiates wired mode')
parser.add_argument('-y', '--youth', dest='y', action='store_true', help='Brings on the cow\'s youthful apperance')
parser.add_argument('-e', '--eyes', default='OO', type=str, help='A custom eye string')
parser.add_argument('-f', '--cowfile', default='default', help='A custom string representing a cow', type=str)
parser.add_argument('-l', '--cowlist', dest='l', action='store_true', help='List all cowfiles on the current COWPATH')
parser.add_argument('-n', '--wrap', action='store_true', help='Whether text should be wrapped in the bubble')
parser.add_argument('-T', '--tongue', default="  ", help='A custom tongue string. It must be 2 characters long')
parser.add_argument('-W', '--width', default=40, type=int, help='The width of the text bubble')
parser.add_argument('message', nargs='?', default='Are you Bully Maguire? Gimme a message', help='A string to wrap in the text bubble')


#Parse input arguments
args = parser.parse_args()
args.eyes = args.eyes[:2] #takes only first 2 characters of Eyes string

if len(args.tongue) != 2:
	raise('Tongue string must be two characters!')

preset = ''.join([mode for mode in MODES if args.__dict__[mode]])


if args.__dict__['l']:
	#Print list of available "cows"
	print(f'Cow files in {os.path.dirname(os.path.abspath(__file__))}:\n', *list_cows())
else:
	#Make it COW!
	cow, cowfile = 'default', args.cowfile
	if '/' not in cowfile:
		cow, cowfile = cowfile, None

	say = cowsay(message=args.message, eyes=args.eyes, tongue=args.tongue, \
			width=args.width, wrap_text=args.wrap, cow=cow, cowfile=cowfile, preset=preset)
	print(say)