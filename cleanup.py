import string
import logging

__author__ = 'rohitsm'
__page__ = 'https://github.com/rohitsm/spsoldboys'

class CleanUp:

	def remove_punctuations(self, word):
		""" Strip any special characters out of word """
		exclude = set(string.punctuation)
		word = ''.join(ch for ch in word if ch not in exclude)
		return word

	# Year
	def adjust_year(self, year):
		"""Converts year into string of 4 digits"""
		
		if (len(str(year)) == 1):
			return str(str(200) + str(year))
		
		if (len(str(year)) == 2):
			# Will fail for entries after 2009
			return str(str(19) + str(year))
		
		if (len(str(year)) == 4):
			return str(year)

		if (len(str(year)) == 3):
			# Write to datastore
			logging.error("Incorrect year entered: ", year)
			return str(1904)



	def remove_quotes(self, entry_list):
		"""	Used for clearning stray quotes that otherwise
			mess up the datastore schema 
		"""
		clean_list = []
		for item in entry_list:
			clean_list.append(item.strip('"'))

		return clean_list

