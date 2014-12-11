import string

class CleanUp:

	def remove_punctuations(self, word):
		# Strip any special characters out of word
		exclude = set(string.punctuation)
		word = ''.join(ch for ch in word if ch not in exclude)
		return word

	# Year

	def adjust_year(self, year):
		
		if len(str(year) == 1):
			return int(str(200) + str(year))
		
		if len(str(year) == 2):
			return int(str(19) + str(year))
		
		if len(str(year) == 4):
			return int(year)


