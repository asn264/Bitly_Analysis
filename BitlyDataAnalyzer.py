'''

Author: Aditi Nair (asnair09@gmail.com)
Date: January 24th 2016

Submission for 24-hour Coding Challenge for Bitly Data Science internship. 

'''

import sys
import json
import pandas as pd
from matplotlib import pyplot as plt 


class BitlyDataAnalyzer(object):

	'''
	This class is an exploratory tool for understanding 'decodes01' as provided in the coding challenge.
	'''

	def __init__(self, only_ckw=False):

		#This is the data in 'decodes01' loaded into a pandas DataFrame
		self.df = self.load_and_format(only_ckw)
		self.ckw_suffix = '_ckw_only' if only_ckw else ''
		self.ckw_prefix = 'CKW ' if only_ckw else ''

	@staticmethod
	def load_and_format(only_ckw):

		'''decodes01 contains multiple json objects so you cannot directly use json.load to load the data into a dictionary. 
		Likewise, pd.read_json also fails. So we load each line in 'decodes01' as a dictionary and pass the list of dicts to pandas.'''
		
		max_df_size = 1000000
		raw_data = []

		try:

			with open('decodes01') as f:

				for line in f:

					t_dict = json.loads(line)

					if only_ckw:
						if 'ckw' in t_dict:
							raw_data.append(t_dict)
					else:
						raw_data.append(t_dict)
				
					if len(raw_data) == max_df_size:
						break

			#Load dictionaries into dataframe
			df = pd.DataFrame(raw_data)

			#Sometimes in production settings, transient issues with the database systems may result in duplicate entries in tables. 
			#We will discard these
			return df.drop_duplicates()

		except IOError:
			sys.exit("Please download the file 'decodes01.gz' into this directory, run <gunzip decodes01.gz>, and try again.")


	def count_duplicate_links(self):

		'''
		From using bitly I noticed that if you enter the same link twice, you get the same shortened-link. 
		I wanted to verify this using a larger set of data in case there was an underlying mechanism that biased my interpretation.
		(Ex: if you enter the same link twice from the same IP address, you get the same shortened-link, but not otherwise.)
		'''

		return True if self.df['g'].nunique() == self.df['u'].nunique() else False


	def compute_percent_ckw(self):

		if 'ckw' in self.df.columns:
			return len(self.df[self.df['ckw'].notnull()])/float(len(self.df)) * 100
		else:
			return 0


	def generate_plots(self):
		
		''' Short-hand function to generate all plots below. '''

		self.plot_clicks_per_link_distribution()
		print 'Completed clicks_per_link' + self.ckw_suffix + ' plot.'
		self.plot_clicks_per_link_by_user_distribution()
		print 'Completed clicks_per_link_by_user' + self.ckw_suffix + ' plot.'
		self.plot_num_clicks_by_user_distribution()
		print 'Completed num_clicks_by_user' + self.ckw_suffix + ' plot.'
		self.plot_unique_timezones_per_url_distribution()
		print 'Completed unique_timezones_per_url' + self.ckw_suffix + ' plot.'
		self.plot_unique_countries_per_url_distribution()
		print 'Completed unique_countries_per_url' + self.ckw_suffix + ' plot.'
		self.plot_clicks_per_timezone()
		print 'Completed plot_clicks_per_timezone' + self.ckw_suffix + ' plot.'
		self.plot_clicks_per_country()
		print 'Completed plots_clicks_per_country' + self.ckw_suffix + ' plot.'


	def group_by_debugging(self):

		'''This is to ensure that I haven't misunderstood the fields for u and h, since many of the relevant graphs look very similar.'''

		x = self.df.groupby(['u']).size()
		y = self.df.groupby(['u', 'h']).size()
		z = self.df.groupby('h').size()

		try:
			print x.eq(y).all()
		except ValueError:
			print 'Mismatched lengths'
		try:
			print x.eq(z).all()
		except ValueError:
			print 'Mismatched lengths'
		try:
			print y.eq(z).all()
		except ValueError:
			print 'Mismatched lengths'



	def plot_clicks_per_link_distribution(self):
		
		'''
		We want to see how much use people get out of a single link. In particular, how many clicks does a link get? 
		This function will create a bar plot showing the distribution. 

		From using bitly I noticed that if you enter the same link twice, you get the same shortened-link. 
		So each long URL can be associated with a unique shortened-link. 
		(This was also verified using the function count_duplicate_links.)
		'''

		#Take df and group by on long URL and then do count(*)
		temp = self.df.groupby(['u']).size()
		temp.plot(kind='hist', bins=100)
		plt.gcf().subplots_adjust(bottom=0.30)
		plt.suptitle(self.ckw_prefix + 'Distribution of Clicks per Link')
		plt.xlabel('Number of Clicks')
		plt.ylabel('Number of Links')
		plt.savefig('plots/clicks_per_link' + self.ckw_suffix + '.png')
		plt.clf()



	def plot_clicks_per_link_by_user_distribution(self):

		'''
		We want to see how much the average user gets out of a single link. 
		This will help us understand why different people use Bitly: 
		If the same person is clicking a link many times maybe they are using it for personal use.
		Otherwise, maybe they are using to share links with others so they tend not to click on it repeatedly.
		
		This function will create a histogram showing how many times a user clicks a single link. 
		'''

		#For each link, for each user, how many times has that user clicked that link
		temp = self.df.groupby(['u', 'h']).size()
		temp.plot(kind='hist', bins=100)
		plt.gcf().subplots_adjust(bottom=0.30)
		plt.suptitle(self.ckw_prefix + 'Distribution of Clicks per Link by User')
		plt.xlabel('Number of Clicks')
		plt.ylabel('Number of Links')
		plt.savefig('plots/clicks_per_link_by_user' + self.ckw_suffix + '.png')
		plt.clf()


	def plot_num_clicks_by_user_distribution(self):

		'''
		How much does the average user use Bitly? In short, how many clicks are they associated with?
		'''

		temp = self.df.groupby('h').size()
		temp.plot(kind='hist', bins=100)
		plt.gcf().subplots_adjust(bottom=0.30)
		plt.suptitle(self.ckw_prefix + 'Number of Clicks by Users')
		plt.xlabel('Number of Clicks')
		plt.ylabel('Number of Users')
		plt.savefig('plots/num_clicks_by_user' + self.ckw_suffix + '.png')
		plt.clf()


	def plot_unique_timezones_per_url_distribution(self):

		'''
		How many different time zones do links tend to be clicked in?
		'''

		timezones_per_url = self.df.groupby(['u'])['tz'].apply(lambda x: len(set(x.tolist())))

		timezones_per_url.plot(kind='hist', bins=100)
		plt.gcf().subplots_adjust(bottom=0.30)
		plt.suptitle(self.ckw_prefix + 'Distribution of Unique Time Zones per URL')
		plt.xlabel('Number of Unique Time Zones')
		plt.ylabel('Number of URLs')
		plt.savefig('plots/unique_timezones_per_url' + self.ckw_suffix + '.png')
		plt.clf()


	def plot_unique_countries_per_url_distribution(self):

		'''
		How many different countries do links tend to be clicked in?
		'''

		countries_per_url = self.df.groupby(['u'])['c'].apply(lambda x: len(set(x.tolist())))

		countries_per_url.plot(kind='hist', bins=100)
		plt.gcf().subplots_adjust(bottom=0.30)
		plt.suptitle(self.ckw_prefix + 'Distribution OF Unique Countries per URL')
		plt.xlabel('Number of Unique Countries')
		plt.ylabel('Number of URLs')
		plt.savefig('plots/unique_countries_per_url' + self.ckw_suffix + '.png')
		plt.clf()


	def plot_clicks_per_timezone(self):

		'''
		What is the relative popularity of different timezones?
		'''

		clicks_per_timezone = self.df.groupby(['tz']).size()
		clicks_per_timezone.sort()
		clicks_per_timezone.plot(kind='bar', figsize=(25,9))
		plt.gcf().subplots_adjust(bottom=0.50)
		plt.suptitle(self.ckw_prefix + 'Clicks per Time Zone')
		plt.xlabel('Time Zone')
		plt.ylabel('Clicks')
		plt.savefig('plots/clicks_per_timezone' + self.ckw_suffix + '.png')
		plt.clf()


	def plot_clicks_per_country(self):

		'''
		What is the relative popularity of different countries?
		'''

		clicks_per_country= self.df.groupby(['c']).size()
		clicks_per_country.sort()
		clicks_per_country.plot(kind='bar', figsize=(25,9))
		plt.gcf().subplots_adjust(bottom=0.30)
		plt.suptitle(self.ckw_prefix + 'Clicks per Country')
		plt.xlabel('Country')
		plt.ylabel('Clicks')
		plt.savefig('plots/clicks_per_country' + self.ckw_suffix + '.png')
		plt.clf()




