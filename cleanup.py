import string

__author__ = 'rohitsm'
__page__ = 'https://github.com/rohitsm/spsoldboys'

class CleanUp:

	def remove_punctuations(self, word):
		# Strip any special characters out of word
		exclude = set(string.punctuation)
		word = ''.join(ch for ch in word if ch not in exclude)
		return word

	# Year
	def adjust_year(self, year):
		
		if (len(str(year)) == 1):
			return str(str(200) + str(year))
		
		if (len(str(year)) == 2):
			return str(str(19) + str(year))
		
		if (len(str(year)) == 4):
			return str(year)

	def remove_quotes(self, entry_list):
		clean_list = []
		for item in entry_list:
			clean_list.append(item.strip('"'))

		return clean_list

