'''
@version : 0.1
@author  : elango
@mail    : elango111000@gmail.com

Text to html convertion tool. Easy to use no code required ot convert
'''

class ReaderArchive:
	def __init__(self, file):
		self.data = ''
		self.data_size = 0
		self.pointer = 0

		self.num_line = 1
		self.num_char_line = 1

		with open(file, 'r') as f:
			self.data = f.read()
			f.close()

		self.data_size = len(self.data)

		if self.data_size <= 0:
			raise Exception('No data found when trying to read file "'+file+'".')

	def read_char(self, isdata = 0):
		try:
			return self.data[self.pointer + isdata]
		except IndexError:
			return False

	def read_char_ant(self):
		return self.read_char(-1)

	def read_char_pos(self):
		return self.read_char(1)

	def move_point(self, isdata = 1):
		# This function will now use a for loop so that it can always update self.num_line and self.num_char_line.
		for i in range(isdata):
			self.pointer += 1

			if self.read_char() == '\n':
				self.num_char_line = 1
				self.num_line += 1
			else:
				self.num_char_line += 1
