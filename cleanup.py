import string

class CleanUp(object):

	def remove_punctuations(self, word):
		exclude = set(string.punctuation)
		word = ''.join(ch for ch in word if ch not in exclude)
		return word

	# Year