'''
@version : 0.1
@author  : elango
@mail    : elango111000@gmail.com

Text to html convertion tool. Easy to use no code required ot convert
'''

TAG_CHAR_OPEN = '<'
TAG_CHAR_CLOSE = '>'
TAG_CHAR_CLOSE_SIGNATURE = '/'

YOUTUBE_URL = 'https://www.youtube.com/embed/'

def filter_quotes_double(cnt):
	cnt = str(cnt)
	return cnt.replace('"', '&quot;')

def filter_entities_html(cnt):
	new_str = ''

	for c in cnt:
		if c == TAG_CHAR_OPEN:
			new_str += '&lt;'
		elif c == TAG_CHAR_CLOSE:
			new_str += '&gt;'
		else:
			new_str += c

	return new_str

class Tag:
	def __init__(self, tag, need_CLOSE = True, in_head = False, require_argument = True, content = [], arguments = {}):
		self.tag = tag
		self.need_CLOSE = need_CLOSE
		self.in_head = in_head
		self.require_argument = require_argument
		self.content = []
		self.arguments = {}

		if need_CLOSE:
			self.add_contents(content)
			
		self.add_arguments(arguments)

	def __str__(self):
		ret = TAG_CHAR_OPEN + self.tag

		if len(self.arguments) > 0:
			for k in self.arguments:
				ret += ' ' + k + '="' + filter_entities_html(filter_quotes_double(self.arguments[k])) + '"'

		if not self.need_CLOSE:
			ret += TAG_CHAR_CLOSE_SIGNATURE + TAG_CHAR_CLOSE
			return ret
		else:
			ret += TAG_CHAR_CLOSE
			for item in self.content:
				ret += str(item)
			ret += TAG_CHAR_OPEN + TAG_CHAR_CLOSE_SIGNATURE + self.tag + TAG_CHAR_CLOSE

			return ret

	def add_contents(self, x):
		if isinstance(x, (list, tuple)):
			self.content.extend(x)
		elif isinstance(x, (Tag, content)):
			self.content.append(x)
		else:
			raise TypeError('Unable to add an object of type "' + str(type(x)) + '" content list.')

	def add_arguments(self, x):
		if isinstance(x, dict):
			self.arguments.update(x)
		else:
			raise TypeError('Unable to add an object of type "' + str(type(x)) + '" to the dictionary of arguments.')

	def receive_argument_tag(self, arg):
		if len(self.content) > 0:
			for i in range(len(self.content)):
				i += 1

				if isinstance(self.content[-i], content):
					if i <= 1:
						self.content[-i].concat(arg)
					else:
						self.add_contents(content(arg))
					break
		else:
			self.add_contents(content(arg))

class content:
	def __init__(self, content = ''):
		if isinstance(content, str):
			self.content = content
		else:
			raise TypeError('Content must be of type string.')

	def __str__(self):
		return filter_entities_html(self.content)

	def concat(self, obj):
		if isinstance(obj, str):
			self.content += obj
		else:
			raise TypeError('Unable to concatenate an object of type "' + str(type(obj)) + '" a string of content.')

class Html(Tag):
	def __init__(self, content = [], arguments = {'lang': ''}):
		Tag.__init__(self, 'html', True, None, True, content, arguments)

	def receive_argument_tag(self, arg):
		self.arguments['lang'] += arg

class Head(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'head', True, None, None, content)

class Title(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'title', True, True, True, content)

class MetaCharset(Tag):
	def __init__(self, arguments = {'charset': ''}):
		Tag.__init__(self, 'meta', False, True, True, None, arguments)

	def receive_argument_tag(self, arg):
		self.arguments['charset'] += arg

class MetaDescription(Tag):
	def __init__(self, arguments = {'name': 'description', 'content': ''}):
		Tag.__init__(self, 'meta', False, True, True, None, arguments)

	def receive_argument_tag(self, arg):
		self.arguments['content'] += arg

class MetaKeywords(Tag):
	def __init__(self, arguments = {'name': 'keywords', 'content': ''}):
		Tag.__init__(self, 'meta', False, True, True, None, arguments)

	def receive_argument_tag(self, arg):
		self.arguments['content'] += arg

class MetaAuthor(Tag):
	def __init__(self, arguments = {'name': 'author', 'content': ''}):
		Tag.__init__(self, 'meta', False, True, True, None, arguments)

	def receive_argument_tag(self, arg):
		self.arguments['content'] += arg

class Header(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'h1', True, False, True, content)

class Header2(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'h2', True, False, True, content)

class Header3(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'h3', True, False, True, content)

class Header4(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'h4', True, False, True, content)

class Header5(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'h5', True, False, True, content)

class Header6(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'h6', True, False, True, content)

class Paragraph(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'p', True, False, True, content)

class Pre(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'pre', True, False, True, content)

class Code(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'code', True, False, True, content)

class HorizontalRuler(Tag):
	def __init__(self):
		Tag.__init__(self, 'hr', False, False, False)

class BreakLine(Tag):
	def __init__(self):
		Tag.__init__(self, 'br', False, False, False)

class Stylesheet(Tag):
	def __init__(self):
		Tag.__init__(self, 'link', False, True, True, None, {'rel': 'stylesheet', 'href': ''})

	def receive_argument_tag(self, arg):
		self.arguments['href'] += arg

class Span(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'span', True, False, True, content)

class Strong(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'strong', True, False, True, content)

class Emphasis(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'em', True, False, True, content)

class Image(Tag):
	def __init__(self):
		Tag.__init__(self, 'img', False, False, True, None, {'src': '', 'alt': ''})

	def receive_argument_tag(self, arg):
		self.arguments['src'] += arg
		self.arguments['alt'] += arg

class Anchor(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'a', True, False, True, content, {'href': ''})

	def receive_argument_tag(self, arg):
		args = arg.strip().split(' ')

		if len(args) < 2:
			if self.arguments['href'] != '':
				self.add_contents(content(args[0]))
			else:
				self.arguments['href'] = args[0]
		else:
			self.arguments['href'] += args[0]
			self.add_contents(content(args[1]))

class YoutubeVideo(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'iframe', True, False, True, content, {'class': 'youtube-frame', 'width': 854, 'height': 480, 'src': '', 'frameborder': 0, 'allowfullscreen': 1})

	def receive_argument_tag(self, arg):
		if self.arguments['src'] == '':
			if arg.startswith('http://') or arg.startswith('https://') or arg.startswith('www.'):
				self.arguments['src'] += arg
			else:
				self.arguments['src'] += YOUTUBE_URL + arg
		else:
			self.arguments['src'] += arg

class Body(Tag):
	def __init__(self, content = []):
		Tag.__init__(self, 'body', True, False, None, content)
