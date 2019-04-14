from __future__ import division
import pandas
from TreeFunctions import *
from PrepareWalsData import *
import numpy as np
from scipy.linalg import fractional_matrix_power
from general import *
from ConvertToWalsTree import * 
from math import sin, cos, asin, sqrt
from LikelihoodFunction import *
from Reconstruction import *


trees = open('trees.txt').readlines()
dataFrame = assignIsoValues('language.csv')
featureName = '83A Order of Object and Verb'
dataFrame = filterDataFrame(dataFrame, featureName, ['1 OV', '2 VO'])
states = findStates(dataFrame, featureName)
matrix = [[0.99, 0.01], [0.01, 0.99]]

def reconstructStatesForAllNodeTest():
	tree = trees[11]
	tree = tree.strip('\n')
	tree = createTree(tree)
	tree = ensureAllTipsHaveIsoCodes(tree)
	tree = assignTipValuesByIso(tree, dataFrame, featureName)
	outputTree = calculateLikelihoodForAllNodes(tree, states, matrix)
	for node in outputTree:
		print findNodeNameWithoutStructure(node)
		print outputTree[node]['states']
	print 'done'	
	outputTree = reconstructStatesForAllNodes(outputTree, states, matrix)
	for node in outputTree:
		print findNodeNameWithoutStructure(node)
		print outputTree[node]['reconstructedStates']
	print 'done'
	print outputTree

def reconstructStatesForAllTreesTest():
	result = reconstructStatesForAllTrees(trees, dataFrame, featureName, states, matrix, limitToIsos = True, numberUpTo = 'all')
	outputFile = open('reconstruction.txt','w')
	for member in result:
		outputFile.write(member + '\t' + str(result[member]) + '\n')
		print member + '\t' + str(result[member]) + '\n'
	print result

def produceListForNodeHeightsTest():
	treeList = []
	for m in range(11,13):
		tree = trees[m]
		tree = tree.strip('\n')
		tree = createTree(tree)
		tree = ensureAllTipsHaveIsoCodes(tree)
		treeList.append(tree)	
	nodeHeights = produceListForNodeHeights(treeList)
	print nodeHeights

def produceDictionaryForNodeHeightsTest():
	treeList = []
	for m in range(11,13):
		tree = trees[m]
		tree = tree.strip('\n')
		tree = createTree(tree)
		tree = ensureAllTipsHaveIsoCodes(tree)
		treeList.append(tree)	
	nodeHeights = produceListForNodeHeights(treeList)
	dictionary = produceDictionaryForNodeHeights(nodeHeights)
	print dictionary
	
def produceListAndDictionaryForNodeHeightsTest():
	treeList = []
	for m in range(11,13):
		tree = trees[m]
		tree = tree.strip('\n')
		tree = createTree(tree)
		tree = ensureAllTipsHaveIsoCodes(tree)
		treeList.append(tree)	
	nodeHeightsList, nodeHeightsDictionary = produceListAndDictionaryForNodeHeights(treeList)
	print nodeHeightsList
	print nodeHeightsDictionary

def prepareTreesTest():
	treeList = trees[0:10]
	print prepareTrees(treeList, numberUpTo = None)
	
def reconstructLocationsForAllTreesTest():
	trees = open('trees.txt').readlines()
	dataFrame = assignIsoValues('language.csv')
	result = reconstructLocationsForAllTrees(trees, dataFrame, numberUpTo = 'all', limitToIsos = True)
	outputFile = open('reconstructedLocations.txt','w')
	for member in result:
		outputFile.write(member + '\t' + str(result[member]) + '\n')
# reconstructLocationsForAllTreesTest()
# reconstructStatesForAllNodeTest()
# reconstructStatesForAllTreesTest()

produceListForNodeHeightsTest()
produceDictionaryForNodeHeightsTest()
# produceListAndDictionaryForNodeHeightsTest()
# prepareTreesTest()