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
from Reconstruction import *

if __name__ == '__main__':
	finalResults = []
	trees = open('trees.txt').readlines()
	trees = prepareTrees(trees)
	dataFrame = assignIsoValues('language.csv')
	featureName = '89A Order of Numeral and Noun'
	reconstructStates = False
	reconstructLocations = False
	if featureName == '89A Order of Numeral and Noun':
		dataFrame = filterDataFrame(dataFrame, featureName, ['2 Noun-Numeral', '1 Numeral-Noun'])
	if featureName == '82A Order of Subject and Verb':
		dataFrame = filterDataFrame(dataFrame, featureName, ['1 SV', '2 VS'])	
	if featureName == '83A Order of Object and Verb':
		dataFrame = filterDataFrame(dataFrame, featureName, ['1 OV', '2 VO'])
	if featureName == '85A Order of Adposition and Noun Phrase':
		dataFrame = filterDataFrame(dataFrame, featureName, ['1 Postpositions', '2 Prepositions'])
	if featureName == '86A Order of Genitive and Noun':
		dataFrame = filterDataFrame(dataFrame, featureName, ['1 Genitive-Noun', '2 Noun-Genitive'])
	if featureName == '87A Order of Adjective and Noun':
		dataFrame = filterDataFrame(dataFrame, featureName, ['1 Adjective-Noun', '2 Noun-Adjective'])
	if featureName == '88A Order of Demonstrative and Noun':
		dataFrame = filterDataFrame(dataFrame, featureName, ['1 Demonstrative-Noun', '2 Noun-Demonstrative'])
	if featureName == '90A Order of Relative Clause and Noun':
		dataFrame = filterDataFrame(dataFrame, featureName, ['1 Noun-Relative clause', '2 Relative clause-Noun'])
	states = findStates(dataFrame, featureName)
	matrix = [[0.999, 0.001], [0.001, 0.999]]
	if reconstructStates:
		result = reconstructStatesForAllTrees(trees, dataFrame, featureName, states, matrix, limitToIsos = True, numberUpTo = 'all')
		outputFile = open(featureName + ' Reconstruction.txt','w')
		for member in result:
			outputFile.write(member + '\t' + str(result[member]) + '\n')
	if reconstructLocations:
		trees = open('trees.txt').readlines()
		dataFrame = assignIsoValues('language.csv')
		result = reconstructLocationsForAllTrees(trees, dataFrame, numberUpTo = 'all', limitToIsos = True)
		outputFile = open('reconstructedLocations.txt','w')
		for member in result:
			outputFile.write(member + '\t' + str(result[member]) + '\n')
	if writeToFile:
		nodesLocations = {}
		reconstructedStates = {}
		nodesFile = open('reconstructedLocations.txt','r').readlines()
		reconstructedStatesFile = open(featureName + ' Reconstruction.txt','r').readlines()
		for line in nodesFile:
			line = line.split('\t')
			try:
				nodesLocations[line[0]] = eval(line[1].strip('\n'))
			except:
				print 'Cannot add node location:'
				print line
		for line in reconstructedStatesFile:
			line = line.split('\t')
			try:
				reconstructedStates[line[0]] = eval(line[1].strip('\n'))
			except:
				print 'Cannot add node states:'
				print line
		nodeHeightsList, nodeHeightsDictionary = produceListAndDictionaryForNodeHeights(trees)
	for treeNumber in range(0,420):
		print treeNumber	
		tree = assignTipValuesByIso(tree, dataFrame, featureName)
		if tree == {}:
			continue
		writeToFile = True
		treeToWrite = tree.copy()
		if writeToFile:
			tree = ultraNewFindContactStatesForAllNodes(treeToWrite, states, reconstructedStates, nodesLocations, nodeHeightsList, nodeHeightsDictionary, distanceThreshold, limit)
			treeFileName = findNodeNameWithoutStructure(findRoot(tree)) + ' ' + featureName + '.txt'
			saveTreeToFile(tree, treeFileName)
		fileName = findNodeNameWithoutStructure(findRoot(tree)) + ' ' + featureName + '.txt'
		contactStateTree = readTreeFromFile(fileName)
		outputTree = calculateLikelihoodForAllNodes(tree, states, matrix)
		results = []
		for borrowability in range(0, 10):
			borrowability = borrowability/10
			outputTree = calculateLikelihoodForAllNodesIncludingContact(tree, contactStateTree, states, matrix, borrowability)
			for node in outputTree:
				print findNodeNameWithoutStructure(node)
				print outputTree[node]['states']	
			results.append(findLikelihoodIncludingContact(tree, contactStateTree, states, matrix, borrowability))
		finalResults.append(results)
		print results
	print finalResults
	for m in xrange(10):
		print m
		print np.sum(np.log([x[m] for x in finalResults]))
	print states

