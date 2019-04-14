from __future__ import division
import pandas
from TreeFunctions import *
from PrepareWalsData import *
import numpy as np
from scipy.linalg import fractional_matrix_power
from general import *
from LikelihoodFunction import * 
from ConvertToWalsTree import * 

trees = open('trees.txt').readlines()


dataFrame = assignIsoValues('language.csv')
featureName = '83A Order of Object and Verb'
dataFrame = filterDataFrame(dataFrame, featureName, ['1 OV', '2 VO'])
states = findStates(dataFrame, featureName)
# print states
matrix = [[0.99, 0.01], [0.01, 0.99]]
 
tree = trees[175]
tree = tree.strip('\n')


tree = createTree(tree)
tree = ensureAllTipsHaveIsoCodes(tree)


tree = assignTipValuesByIso(tree, dataFrame, featureName)

outputTree = calculateLikelihoodForAllNodes(tree, states, matrix)
for node in outputTree:
	print findNodeNameWithoutStructure(node)
	print outputTree[node]['states']
print 'done'
