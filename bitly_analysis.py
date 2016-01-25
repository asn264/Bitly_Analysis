'''

Author: Aditi Nair (asnair09@gmail.com)
Date: January 24th 2016

'''

from BitlyDataAnalyzer import *

def main():

	#Create instances of the Analyzer objects to help conduct analyses and generate plots
	general_analyzer = BitlyDataAnalyzer()
	ckw_analyzer = BitlyDataAnalyzer(only_ckw=True)

	#Review basic information about both data-sets. 
	print 'I have created a general analyzer tool which looks at some selection of the provided data, as well as a \'ckw\' analyzer tool which only looks at some selection of the provided date where a \'ckw\' value is provided.'
	print 'Both datasets initially pulled 1000000 entries.'

	print 'The general dataset contains ' + str(len(general_analyzer.df)) + ' unique entries.'
	print 'The \'ckw\' dataset contains ' + str(len(ckw_analyzer.df)) + ' unique entries.'

	print 'Percent entries containing \'ckw\' fields in general dataset: ' + str(general_analyzer.compute_percent_ckw())
	print 'Percent entries containing \'ckw\' fields in \'ckw\' dataset: ' + str(ckw_analyzer.compute_percent_ckw())

	print 'Now we will generate the plots. This will take some time...'

	general_analyzer.generate_plots()
	ckw_analyzer.generate_plots()
	
	print 'All done! Please see Analysis.pdf for a nicely-formatted analysis of the plots and the data.'


#Run the program 
if __name__ == '__main__':
	main()