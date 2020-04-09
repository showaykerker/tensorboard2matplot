from collections import OrderedDict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
pandas 

          wall_time       relative  performance/successRate  loss/actorLoss  loss/criticLoss
5000   1.586019e+09   15402.346391                    0.016        0.443302         0.005209
10000  1.586035e+09   31535.651242                    0.018        0.659367         0.010056
15000  1.586050e+09   46102.767550                    0.132        0.800042         0.016228
20000  1.586063e+09   58943.215238                    0.206        0.845896         0.043629
25000  1.586075e+09   71191.548972                    0.299        0.838121         0.049333
30000  1.586086e+09   82806.918912                    0.340        0.738454         0.077819
35000  1.586098e+09   93941.598907                    0.380        0.618673         0.119397
40000  1.586109e+09  105024.457817                    0.430        0.458337         0.128933
45000  1.586120e+09  116024.366345                    0.370        0.290222         0.170296
50000  1.586131e+09  126932.034167                    0.377        0.246781         0.194892
55000  1.586142e+09  138096.532138                    0.388        0.181751         0.222578
60000  1.586153e+09  149282.179844                    0.405        0.250683         0.207150
"""

tableau20 = np.array([(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)] ) / 255.

class plotter():
	def __init__(self, use_relative_time=False, use_min_max=False):
		self.use_relative_time = use_relative_time
		self.use_min_max = use_min_max

	def plot(self, odict, groups, suptitle="", moving_avg=0.):
		self.odict = odict
		self.groups = groups
		self.seperated = OrderedDict({})

		n_idx = None
		
		for tn in groups:
			self.seperated[tn] = []

		for n, v in odict.items():
			df = v['data']
			if n_idx is None: 
				n_idx = len(df)
				idx_names = df.index if not self.use_relative_time else df['relative'].to_numpy()/3600
			elif n_idx > len(df): 
				n_idx = len(df)
				idx_names = df.index if not self.use_relative_time else df['relative'].to_numpy()/3600
			self.seperated[v["groups"]].append(df)
			

		label_names = list(df.columns)
		try:
			label_names.remove('relative')
			label_names.remove('wall_time')
		except: pass

		print('Plotting Labels:', label_names)

		self._plot(n_idx, idx_names, label_names, suptitle, moving_avg)
			

	def _plot(self, n_idx, idx_names, label_names, suptitle, moving_avg):
		groups = self.seperated.keys()
		if self.use_min_max:
			values = np.zeros((len(self.seperated.keys()), len(label_names), 3, n_idx))  # n_groups, lbl, mean and min and max, n_idx
		else:
			values = np.zeros((len(self.seperated.keys()), len(label_names), 2, n_idx))  # n_groups, lbl, mean and var, n_idx
		for i_group, (k, dfs) in enumerate(self.seperated.items()):
			# key: group_name
			# value: list of df of given group_name
			values_tmp = np.zeros((len(label_names), len(dfs), n_idx))
			try:
				for i_lbl, lbl in enumerate(label_names):
						
					for i_df, df in enumerate(dfs):
						values_tmp[i_lbl, i_df] = df[lbl].to_numpy()[:n_idx]

				values[i_group, :, 0] = values_tmp.mean(axis=1)

				for i in range(values.shape[-1]-1):
					values[i_group, :, 0, i+1] = values[i_group, :, 0, i+1] * (1-moving_avg) + values[i_group, :, 0, i] * moving_avg
					

				if self.use_min_max:
					values[i_group, :, 1] = values_tmp.min(axis=1)
					values[i_group, :, 2] = values_tmp.max(axis=1)
				else:
					values[i_group, :, 1] = values_tmp.var(axis=1)

			except KeyError:
				print('Errors Occurr. Give up plotting label %s from group %s' % (lbl, k) )
			

		fig, ax = plt.subplots(len(label_names), 1, sharex=True)
		fig.suptitle(suptitle)
		for i_lbl, lbl in enumerate(label_names):			
			ax[i_lbl].grid()
			ax[i_lbl].set_ylabel(lbl)
			if i_lbl == len(list(label_names)) - 1: 
				ax[i_lbl].set_xlabel('iterations' if not self.use_relative_time else 'relative time (hours)')
			for i_group, group_name in enumerate(self.seperated.keys()):
				ax[i_lbl].plot(idx_names, values[i_group, i_lbl, 0], label=group_name, color=tableau20[(i_group*3)%20], alpha=0.8)
				if self.use_min_max:
					ax[i_lbl].fill_between(idx_names, values[i_group, i_lbl, 1], values[i_group, i_lbl, 2], color=np.clip(tableau20[(i_group*3)%20]*1.4, 0, 1), alpha=0.2)
				else:
					ax[i_lbl].fill_between(idx_names, values[i_group, i_lbl, 0]-values[i_group, i_lbl, 1], values[i_group, i_lbl, 0]+values[i_group, i_lbl, 1], color=np.clip(tableau20[(i_group*3)%20]*1.4, 0, 1), alpha=0.2)
			leg = ax[i_lbl].legend(loc='upper left', shadow=True)

		plt.show()

		

					

			


			
			

