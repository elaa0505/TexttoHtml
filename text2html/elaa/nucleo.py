'''
@version : 0.1
@author  : elango
@mail    : elango111000@gmail.com

Text to html convertion tool. Easy to use no code required ot convert
'''

import sys
from pprint import pprint
from .io import ReaderArchive
from .tags import *

DOCUMENT_DOCTYPE = '<!DOCTYPE html>\n'

SYNTAX_TAG_ACTIVATE = '@'
SYNTAX_TAG_DELIMITER =  ';'
SYNTAX_TAG_NEWLINE = '\n'
SYNTAX_TAG_SPACE = ' '
SYNTAX_TAG_COMMENTARY = '#'
SYNTAX_TAG_ESCAPE = '!'

SYNTAX_TAG_NAME_SEPARATORS = (
	SYNTAX_TAG_ACTIVATE,
	SYNTAX_TAG_DELIMITER,
	SYNTAX_TAG_NEWLINE,
	SYNTAX_TAG_SPACE
)

SYNTAX_TAG_ARG_SEPARATORS = (
	SYNTAX_TAG_ACTIVATE,
	SYNTAX_TAG_DELIMITER
)

TAG_ACCEPT_NEWLINES = (
	Pre,
	Code
)

class ProcessorText:
	def __init__(self, entry, exit = None, show_doctype = True, print_debug = False):
		self.error = False

		try:
			self.reader = ReaderArchive(entry)
		except IOError:
			self.error = 'Unable to read informed file.'
		else:
			# Where will the exit be?
			if exit != None:
				try:
					self.exit = open(exit, 'w')
				except IOError:
					self.error = 'Could not write data to a file.'
			else:
				self.exit = sys.stdout

			self.show_doctype = show_doctype
			self.print_debug = print_debug

			self.html = Html()
			self.head = Head()
			self.body = Body()

			self.tags_lista = []

			self.html.add_contents((self.head, self.body))

			self.ignoring = False

	def comperror(self, msg, tag_NAME_done_sub = 0):
		self.error = True

		self.complog('\nOran a compilation error:\n\t'+ msg +' on the line ' + str(self.reader.num_line) + ', character ' + str(self.reader.num_char_line - tag_NAME_done_sub) + '.')
	
	# Print the Processing the tag
	def complog(self, msg):
		#sys.stdout.write(msg + '\n')
		elaa='0'
		

	def debuglog(self):
		if self.print_debug:
			self.complog('--Debug---------------------------------------------')
			self.complog('> ReaderArchive: line ' + str(self.reader.num_line) + ', character ' + str(self.reader.num_char_line) + '.')
			self.complog('> Structure of tag Html:')
			pprint(vars(self.html))
			self.complog('> Structure of tag Head:')
			pprint(vars(self.head))
			self.complog('> Structure of tag Body:')
			pprint(vars(self.body))
			self.complog('> Structure of fila de tags:')
			pprint(self.tags_lista)
			self.complog('--Debug---------------------------------------------')


	def write_exit(self):
		#self.complog('----------------------------------------------------')
		#self.complog('> Code Html generated:')
		#self.complog('----------------------------------------------------')
		
		#self.exit.write(DOCUMENT_DOCTYPE)
		
		if self.show_doctype:
			self.exit.write(DOCUMENT_DOCTYPE)
			
			#if self.exit != sys.stdout:
			#	sys.stdout.write(DOCUMENT_DOCTYPE)

		DOCUMENT = str(self.html)

		self.exit.write(DOCUMENT)
		
		# If input file exist
		#if self.exit != sys.stdout:
		#		sys.stdout.write(DOCUMENT)
				
	def create_tag_object(self, tag):
		if tag == 'title':
			return Title()
		elif tag == 'charset':
			return MetaCharset()
		elif tag == 'lang':
			return self.html
		elif tag == 'description':
			return MetaDescription()
		elif tag == 'keywords':
			return MetaKeywords()
		elif tag == 'author':
			return MetaAuthor()
		elif tag == 'h1':
			return Header()
		elif tag == 'h2':
			return Header2()
		elif tag == 'h3':
			return Header3()
		elif tag == 'h4':
			return Header4()
		elif tag == 'h5':
			return Header5()
		elif tag == 'h6':
			return Header6()
		elif tag == 'p':
			return Paragraph()
		elif tag == 'pre':
			return Pre()
		elif tag == 'code':
			return Code()
		elif tag == 'hr':
			return HorizontalRuler()
		elif tag == 'br':
			return BreakLine()
		elif tag == 'stylesheet':
			return Stylesheet()
		elif tag == 'span':
			return Span() 	
		elif tag == 'strong':
			return Strong()
		elif tag == 'em':
			return Emphasis()
		elif tag == 'img':
			return Image()
		elif tag == 'a':
			return Anchor()
		elif tag == 'youtube':
			return YoutubeVideo()
		else:
			return False

	def add_NAME_tag(self):
		NAME = ''

		while True:
			self.reader.move_point()

			char = self.reader.read_char()

			# Get tags without argument still in list

			char_pos = self.reader.read_char_pos()

			if not char:
				break

			if char not in SYNTAX_TAG_NAME_SEPARATORS:
				NAME += char

				if char_pos in SYNTAX_TAG_ARG_SEPARATORS or char_pos == SYNTAX_TAG_SPACE:
					break
			else:
				break

		return NAME

	def add_argument_tag(self, tag_object):
		arg = ''
		tag_inside = False

		while True:
			self.reader.move_point()

			char = self.reader.read_char()

			# Arrange recursion to read tags within other tags

			char_pos = self.reader.read_char_pos()

			if not char:
				break
			else:
				# If this tag doesn't accept a newline, just ignore this loop.
				# and skip a cycle
				if char == SYNTAX_TAG_NEWLINE and not isinstance(tag_object, TAG_ACCEPT_NEWLINES):
					continue;

			if char not in SYNTAX_TAG_ARG_SEPARATORS:
				if char == SYNTAX_TAG_SPACE:
					if len(arg) > 0:
						arg += char
				else:
					arg += char

				# If this tag argument is above another tag queue,
				# let's skip the next ';' because otherwise it will be terminated right there
				if char_pos in SYNTAX_TAG_ARG_SEPARATORS:
					if char_pos == SYNTAX_TAG_ACTIVATE:
						tag_inside = True
					
					break
			else:
				break

		return arg.lstrip(), tag_inside

	def add_COMMENTARY(self):
		while True:
			self.reader.move_point()

			char = self.reader.read_char()

			if not char or char == SYNTAX_TAG_NEWLINE:
				break

	def join_content_tag_dependent(self, char):
		if isinstance(self.tags_lista[-1], content):
			self.tags_lista[-1].concat(char)
		else:
			self.tags_lista[-1].receive_argument_tag(char)

	def join_content(self, char):
		# It's just content, concatenate this content in the last tag of our tag queue
		try:
			if char == SYNTAX_TAG_NEWLINE and not isinstance(self.tags_lista[-1], TAG_ACCEPT_NEWLINES):
				self.join_content_tag_dependent(char)
			else:
				self.join_content_tag_dependent(char)
				
		except IndexError:
			if char != SYNTAX_TAG_NEWLINE and char != SYNTAX_TAG_SPACE:
				new_content = content(char)

				self.tags_lista.append(new_content)
				self.body.add_contents(new_content)

	def rotate(self):
		if self.error:
			self.complog(self.error)
			return

		#try:
		while True:
			char = self.reader.read_char()

			if not char:
				break


			if char == SYNTAX_TAG_COMMENTARY:
				# If we are about to find a comment

				if not self.ignoring:
					self.add_COMMENTARY()
				else:
					self.join_content(char)
					self.ignoring = False

			elif char == SYNTAX_TAG_ESCAPE:
				prox_char = self.reader.read_char_pos()

				if prox_char == SYNTAX_TAG_COMMENTARY or prox_char == SYNTAX_TAG_ACTIVATE:
					self.ignoring = True
				else:
					self.join_content(char)

			elif char == SYNTAX_TAG_ACTIVATE:
				# Are we ignoring?
				if not self.ignoring:
					# Add this tag

					tag_NAME = self.add_NAME_tag()

					tag_object = self.create_tag_object(tag_NAME)

					if not tag_object:
						self.comperror('A tag "@' + tag_NAME + '" not set.', len(tag_NAME))
						break
					
					self.complog('Processing a tag @' + tag_NAME + '..')

					if tag_object.require_argument:
						tag_argument, tag_inside = self.add_argument_tag(tag_object)

						self.complog('\ttag_argument = "'+tag_argument+'"\n\ttag_inside = '+str(tag_inside))

						# Only return this error if the tag really can't be closed
						# (your modification is on attributes only)
						if not tag_argument and not tag_object.need_CLOSE:
							self.comperror('A tag "@' + tag_NAME + '" requires a parameter but was not informed.')
							break

						try:
							tag_object.receive_argument_tag(tag_argument)
						except Exception as e:
							self.comperror(str(e))
							break

					# self.create_tag_object () may return a reference to an existing object already in the skeleton
					# html, this is because we will just change something in it, not need to create another
					# so we need to avoid adding the same object again
					if not isinstance(tag_object, Html):
						# This logic allows recursion of one tag inside another
						# Also check if the tag we are trying to add content will not have the content discarded (not need_CLOSE)
						if len(self.tags_lista) > 0 and not isinstance(self.tags_lista[-1], content) and self.tags_lista[-1].need_CLOSE:
							self.tags_lista[-1].add_contents(tag_object)
						else:
							if tag_object.in_head:
								self.head.add_contents(tag_object)
							else:
								self.body.add_contents(tag_object)

						self.tags_lista.append(tag_object)
				else:
					self.join_content(char)
					self.ignoring = False

			elif char == SYNTAX_TAG_DELIMITER:
				if not self.ignoring:
					# Close tag being processed
					if len(self.tags_lista) > 0:
						self.tags_lista.pop()
				else:
					self.join_content(char)
					self.ignoring = False

			else:
				self.join_content(char)

			self.debuglog()

			self.reader.move_point()
		
		# Print the html tag from comment prompt
		if not self.error:
			self.write_exit()
			
			
			

		#except Exception as e:
		#	self.complog('Oran a problem rotating the compiler.\nException:\n\t' + str(e) + '\nDebug:\n\t' + 'line ' + str(self.reader.num_line) + '\n\tcharacter ' + str(self.reader.num_char_line))
