import warnings
import itertools
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import matplotlib
from pylab import rcParams
from tkinter import filedialog as fd

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')

matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

filename = "sample_dataset.csv" # change this line to use different dataset
df = pd.read_csv(filename)
df = df.groupby('elapsed_seconds_of_video')['balloon_angle'].sum().reset_index()
df = df.sort_values('elapsed_seconds_of_video')
df = df.set_index('elapsed_seconds_of_video')
print("How many nulls: ", df.isnull().sum())
df = df.groupby('elapsed_seconds_of_video')['balloon_angle'].sum().reset_index()
y = df['balloon_angle']
rcParams['figure.figsize'] = 18, 8
decomp = sm.tsa.seasonal_decompose(y, model='additive', period=50) # decomposition 

fig = decomp.plot()
plt.show()
