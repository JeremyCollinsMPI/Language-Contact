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
from Contact import *
from ContactLikelihood import * 


def contactStatesTreeTest():
	locationTree = assignCoordinatesByIso(tree, dataFrame, 'latitude', 'longitude')
	locationTree = reconstructLocationsForAllNodes(locationTree)
	for node in locationTree:
		print findNodeNameWithoutStructure(node)
		print locationTree[node]
	distanceThreshold = None
	limit = 10
	contactStatesTree = findContactStatesForAllNodes(tree, locationTree, dataFrame, featureName, distanceThreshold, limit)
	for node in contactStatesTree:
		print node
		print contactStatesTree[node]
	print contactStatesTree
	saveTreeToFile(contactStatesTree)


if __name__ == '__main__':
	trees = open('trees.txt').readlines()
	dataFrame = assignIsoValues('language.csv')
	featureName = '83A Order of Object and Verb'
	treeNumber = 66
	writeToFile = False
	if featureName == '89A Order of Numeral and Noun':
		dataFrame = filterDataFrame(dataFrame, featureName, ['2 Noun-Numeral', '1 Numeral-Noun'])
	if featureName == '82A Order of Subject and Verb':
		dataFrame = filterDataFrame(dataFrame, featureName, ['1 SV', '2 VS'])	
	if featureName == '83A Order of Object and Verb':
		dataFrame = filterDataFrame(dataFrame, featureName, ['1 OV', '2 VO'])
	states = findStates(dataFrame, featureName)
	matrix = [[0.999, 0.001], [0.001, 0.999]]
	tree = trees[treeNumber]
	tree = tree.strip('\n')
	tree = createTree(tree)
	tree = ensureAllTipsHaveIsoCodes(tree)
	tree = assignTipValuesByIso(tree, dataFrame, featureName)
	if writeToFile:
		contactStatesTreeTest()
	fileName = findNodeNameWithoutStructure(findRoot(tree)) + '.txt'
	contactStateTree = readTreeFromFile(fileName)
	outputTree = calculateLikelihoodForAllNodes(tree, states, matrix)
	results = []
	for borrowability in range(0, 20):
		borrowability = borrowability/100
		outputTree = calculateLikelihoodForAllNodesIncludingContact(tree, contactStateTree, states, matrix, borrowability)
		for node in outputTree:
			print findNodeNameWithoutStructure(node)
			print outputTree[node]['states']	
		results.append(findLikelihoodIncludingContact(tree, contactStateTree, states, matrix, borrowability))
	print results

