# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 16:38:42 2019

@author: sydne
"""
import pandas as pd
import numpy

leuk=pd.read_csv(r'C:\Users\sydne\Documents\Linear Algebra\leuk.csv')
print(leuk.loc[:,'V5001'])

import sklearn
from sklearn.preprocessing import StandardScaler

x=leuk.iloc[:,0:5000].values
y=leuk.loc[:,['V5001']].values
x_std = StandardScaler().fit_transform(x)


from sklearn.decomposition import PCA


pca=PCA(n_components=2)
principalComponents=pca.fit_transform(x)

principalDF = pd.DataFrame(data=principalComponents, columns = ['principal component1','principal component 2, principal component 3'])

finalDf=pd.concat([principalDF, leuk[['V5001']]], axis=1)
x=finalDf.iloc[:,0:2].values
print('Target classes:', finalDf.target_names)
y=finalDf.target

print(finalDf)

from collections import Counter

def misclassify( tg, pred ):
# Try to determine number of misclassified elements during clustering
#
# tg: Target class
# pred: Predicted cluster ID

	# Get number of classes, clusters, create a "misclassified
	tg_n = len( set( tg ) )
	pr_n = len( set( pred ) )
	miss = pr_n + 1

	# Initialize errors per class, set of cluster IDs seen
	err = [ 0 ] * tg_n
	clust_ID = []

	# For each target class, compute cluster ID errors
	for i in range( 0, tg_n ):
		# Grab subset of targets, predictions for current class
		beg = i * 50
		tg_sub = tg[ beg: beg + 50 ]
		pr_sub = pred[ beg: beg + 50 ]

		# "Mark as error" any cluster ID already assigned to a class
		for j,val in enumerate( pr_sub ):
			if val in clust_ID: pr_sub[ j ] = miss

		# Build match vector as target class ID minus cluster ID
		# Copy over errors from cluster ID vector
		match = tg_sub - pr_sub
		for j,val in enumerate( pr_sub ):
			match[ j ] = miss if val == miss else match[ j ]

		# Build dict of IDs, descending by frequency
		count = Counter( match )
		freq = count.most_common()

		# Find most frequent ID that is not "miss" error
		max_freq = miss
		for val in freq:
			if val[ 0 ] != miss:
				max_freq = val[ 0 ]
				err[ i ] = 50 - val[ 1 ]
				break

		# If all entries "miss" error, all entries are incorrect
		if max_freq == miss:
			err[ i ] = 50

			# Copy miss to entire subrange of original prediction list
			for j in range( 0, len( pr_sub ) ):
				pred[ j + beg ] = miss
			continue

		max_ID = miss
		for j,val in enumerate( match ):
			if val != max_freq: pred[ j + beg ] = miss
			if val == max_freq: max_ID = j

		# Add cluster ID to list of cluster IDs seen so far
		clust_ID = clust_ID + [ pr_sub[ max_ID ] ]

	# Return total errors, error per class
	return sum(err), err

from sklearn.cluster import KMeans

# Partition data into three clusters
km = KMeans( n_clusters = 3, random_state = 101 )
km.fit(x)
y_pred = km.predict(x)

n = len( y_pred )
err = misclassify( y, y_pred )

# Print accuracy results
print( 'k-Means Clustering:' )
print( 'Misassigned samples:', err[ 0 ] )
print( 'Accuracy: {:.2f} (out of 1)'.format( ( n - err[ 0 ] ) / n ) )


len(set(y))