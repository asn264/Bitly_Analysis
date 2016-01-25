'''

Author: Aditi Nair (asnair09@gmail.com)
Date: January 24th 2016

'''

from BitlyDataAnalyzer import *

def main():

	'''When generating plots I was concerned that a lot of my graphs looked similar. 
	It was unclear whether this was a property of the data or whether I had misunderstood some of the data fields.
	This function should either print Mismatched lengths or False to ensure that there is a difference in grouping by u, h or u and h.
	It should not print True.'''

	#Create instances of the Analyzer objects to help conduct analyses 
	general_analyzer = BitlyDataAnalyzer()
	ckw_analyzer = BitlyDataAnalyzer(only_ckw=True)

	print "Checking general dataset for variation in grouping by u and h: "
	general_analyzer.group_by_debugging()
	print "Checking ckw dataset for variation in grouping by u and h: "
	ckw_analyzer.group_by_debugging()

#Run the program 
if __name__ == '__main__':
	main()