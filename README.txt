Author: Aditi Nair (asnair09@gmail.com)
Date Started: January 24th 2016


To start, download the file 'decodes01.gz' into this directory, run <gunzip decodes01.gz>. (The challenge website allowed only submissions of maximum size 10MB.)

Then run <python bitly_analysis.py> to get started. Finally see Analysis.pdf to see a nicely formatted explanation of the analysis I've done.

Plots are generated into the plots directory which also contains a previously_generated directory of plots that I generated using the program before submission.

Once I generated plots, I was concerned that some of my plots looked very similar. It was unclear whether this was a property of the data or whether I had misunderstood some of the data fields. Therefore, I created group_by_analysis.py to verify. You can run it with <python group_by_analysis.py>. 

Note: this code was written using Python 2.7.10 and pandas 0.16.2.