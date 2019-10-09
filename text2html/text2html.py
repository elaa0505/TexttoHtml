'''
@version : 0.1
@author  : elango
@mail    : elango111000@gmail.com

Text to html convertion tool. Easy to use no code required ot convert
'''

import sys
from elaa.nucleo import ProcessorText

PROGRAM_INS = """\
Usage: text2html.text2html FILE [-OPTIONS] [-OUT OUT]

    -o		On success, instead of writing to stdout, write to a file.
    -t		Adds the <! DOCTYPE html> header to the generated code.
    -d		[DEBUG] Each cycle the processor prints information about
		Html structure and file reader.

"""

PROGRAM_LIST_options = (
	{
		'option': '--help',
		'requires_parameter': False
	},
	{
		'option': '-o',
		'requires_parameter': True
	},
	{
		'option': '-t',
		'requires_parameter': False
	},
	{
		'option': '-d',
		'requires_parameter': False
	}
)

def print_userins():
	sys.stdout.write(PROGRAM_INS)
	
def process_arguments():
	arguments = []
	options = []

	# Getting file names and options through arguments
	for i in range(len(sys.argv)):
		if sys.argv[i].startswith('-'):
			found = False

			for opt in PROGRAM_LIST_options:
				if sys.argv[i] == opt['option']:
					found = True

					if opt['requires_parameter']:
						try:
							options.append(
								{
									opt['option']: sys.argv[i + 1]
								}
							)
						except IndexError:
							raise Exception('A option "' + opt['option'] + '" requires a parameter that was not entered.')
					else:
						options.append(
							{
								opt['option']: None
							}
						)

			if not found:
				raise Exception('A informed option "' + sys.argv[i] + '" does not exist.')
		else:
			# If not the first argument (this argument is the name of the file to be executed, in this case this script)
			# Let's see if this file is not the parameter of an already informed option
			if i != 0:
				you_can_add = True

				for op in options:
					for op_name in op:
						if sys.argv[i] == op[op_name]:
							you_can_add = False
							break

				if you_can_add:
					arguments.append(sys.argv[i])

	return arguments, options

def main():
	input_file = None
	output_file = None
	
	try:
		arguments, options = process_arguments()

		input_file = arguments[0]
	except IndexError:
		print_userins()
	except Exception as e:
		sys.stdout.write(str(e) + '\n')
	else:
		# Process options
		show_userinfo = False
		show_doctype = False
		print_debug = False

		for opt in options:
			for k in opt:
				if k == PROGRAM_LIST_options[0]['option']:
					show_userinfo = True
					break

				elif k == PROGRAM_LIST_options[1]['option']:
					output_file = opt[k]
					
				elif k == PROGRAM_LIST_options[2]['option']:
					show_doctype = True

				elif k == PROGRAM_LIST_options[3]['option']:
					print_debug = True

			if show_userinfo:
				break

		if not show_userinfo:
			p = ProcessorText(input_file, output_file, show_doctype, print_debug)
			p.rotate()
		else:
			print_userins()

if __name__ == '__main__':
	main()
	
