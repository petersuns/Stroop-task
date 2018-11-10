"""
#perform basic data analysis on the data colleted

@author: Shuo and Chiara
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import glob

# housekeeping issue: set the current working directory
# Please change this to your path
os.chdir('/Users/shuosun/Documents/KU Leuven/Stroop task/output') 
dirname = os.getcwd()

# open all the output .csv files and read them in one dataframe
Outputpathlist = glob.glob(dirname+"/*.csv")
len(Outputpathlist)
print(Outputpathlist)
df_from_each_file = (pd.read_csv(f) for f in Outputpathlist)
data   = pd.concat(df_from_each_file, ignore_index=True)

# sepreate phase 1 and phase 2 for data analysis
time_1 =data[data.Phase==1].Time
time_2 =data[data.Phase==2].Time
time_both = [time_1,time_2]

# Histogram of phase 1
title = 'Histogram of the Congruent Condition'
kind = 'hist'
plot = time_1.plot(title=title, kind=kind, bins=7)
xLabel = plt.xlabel('Time (seconds)')

# Histogram of phase 2
title = 'Histogram of the Congruent Condition'
kind = 'hist'
plot = time_2.plot(title=title, kind=kind, bins=7)
xLabel = plt.xlabel('Time (seconds)')

# Bar Diagramm of reaction time in phase 1 and phase 2
df = pd.DataFrame({'Phase 1': time_1, 'Phase 2': time_2},
                   columns=['Phase 1', 'Phase 2'])
plt.figure();
df.plot.hist(title="Stroop Data", stacked="false", bins = 25);
plt.ylabel('Count')
plt.xlabel('Time in Seconds')
plt.title('Bar Diagram')

#boxplot of reaction time in phase 1 and phase 2
color = dict(boxes='grey', whiskers='blue', medians="DarkBlue", caps="green" )
df.plot.box(color=color, sym="r+");
plt.ylabel('Time in Seconds')
plt.title('Boxplots for Stroop Data')

# key statistics of all data 
print "Key statistics of all data"
print data.describe()

# key statistics of reaction time in phase 1 and phase 2
print "Key statistics of reation time in phase 1"
print time_1.describe()
print "Key statistics of reation time in phase 2"
print time_2.describe()
print "Phase 1 time, median:",time_1.median()
print "Phase 1 time, standard deviation:",time_1.std()
print "Phase 2 time, median:",time_2.median()
print "Phase 2 time, standard deviation:",time_2.std()

# calculate outlieres
newdata = data.copy()
newdata['TimeDeviationFromMean'] = abs(newdata['Time'] - newdata['Time'].mean())
newdata['IsTimeOutlier'] = abs(newdata['Time'] - newdata['Time'].mean()) > 1.96*newdata['Time'].std()
newdata['TimeSquareDevation'] = abs(newdata['Time'] - newdata['Time'].mean())**2
print "Table of Outliers"
print newdata

# calculate variance of reaction time 
TimeVariance = ((newdata.TimeSquareDevation).sum())/(newdata['Time'].count()-1)
print "Variance of reaction time:",TimeVariance

#calc IQR for reaction time
dfc = pd.DataFrame({'Time': data['Time']})
dfc.sort_values('Time', inplace=True)
Q1 = dfc['Time'].quantile(0.25)
Q3 = dfc['Time'].quantile(0.75)
IQR_time = Q3 - Q1
print "Reaction Time  Interquartile Range (IQR)"
print "Q1:", Q1
print "Q3:", Q3
print "IQR:", IQR_time
Outlier = Q1-(1.5*IQR_time)
print Outlier
Outlierabove = Q3 + (1.5*IQR_time)
print Outlierabove





