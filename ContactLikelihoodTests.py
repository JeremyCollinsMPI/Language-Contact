from __future__ import division
import pandas
from TreeFunctions import *
from PrepareWalsData import *
import numpy as np
from scipy.linalg import fractional_matrix_power
from general import *
from LikelihoodFunction import * 
from ConvertToWalsTree import * 
from Contact import * 
from ContactLikelihood import * 

trees = open('trees.txt').readlines()


dataFrame = assignIsoValues('language.csv')


# prepare particular features

# numeral-noun
# featureName = '89A Order of Numeral and Noun'
# dataFrame = filterDataFrame(dataFrame, featureName, ['2 Noun-Numeral', '1 Numeral-Noun'])
# states = findStates(dataFrame, featureName)

# subject-verb
# featureName = '82A Order of Subject and Verb'
# dataFrame = filterDataFrame(dataFrame, featureName, ['1 SV', '2 VS'])
# states = findStates(dataFrame, featureName)
# print states


# object-verb
featureName = '83A Order of Object and Verb'
dataFrame = filterDataFrame(dataFrame, featureName, ['1 OV', '2 VO'])
states = findStates(dataFrame, featureName)
print states


# print states
matrix = [[0.999, 0.001], [0.001, 0.999]]
 
tree = trees[66]
tree = tree.strip('\n')


tree = createTree(tree)
tree = ensureAllTipsHaveIsoCodes(tree)


tree = assignTipValuesByIso(tree, dataFrame, featureName)
outputTree = calculateLikelihoodForAllNodes(tree, states, matrix)


contactStateTree = readTreeFromFile("'Austroasiatic [aust1305]'.txt")
print contactStateTree

def findLikelihoodIncludingContactTest():
	results = []
	for borrowability in range(1,2):
		borrowability = borrowability/10
		outputTree = calculateLikelihoodForAllNodesIncludingContact(tree, contactStateTree, states, matrix, borrowability)
		for node in outputTree:
			print findNodeNameWithoutStructure(node)
			print outputTree[node]['states']
	
		results.append(findLikelihoodIncludingContact(tree, contactStateTree, states, matrix, borrowability))
	print results

def findLikelihoodsIncludingContactWithoutRootProbabilitiesTest():
	results = []
	for borrowability in range(1,3):
		borrowability = borrowability/10
		outputTree = calculateLikelihoodForAllNodesIncludingContact(tree, contactStateTree, states, matrix, borrowability)
		for node in outputTree:
			print findNodeNameWithoutStructure(node)
			print outputTree[node]['states']	
		results.append(findLikelihoodsIncludingContactWithoutRootProbabilities(tree, contactStateTree, states, matrix, borrowability))
	print results
	return results

def findLikelihoodIncludingContactAndRootProbabilitiesTest():
	results = []
	for borrowability in range(1,3):
		borrowability = borrowability/10
		outputTree = calculateLikelihoodForAllNodesIncludingContact(tree, contactStateTree, states, matrix, borrowability)
		for node in outputTree:
			print findNodeNameWithoutStructure(node)
			print outputTree[node]['states']	
		results.append(findLikelihoodsIncludingContactWithoutRootProbabilities(tree, contactStateTree, states, matrix, borrowability))
	stateLikelihoods = results[0]
	rootProbabilities = {'1 OV':0, '2 VO':1}
	result = findLikelihoodIncludingContactAndRootProbabilities(states, stateLikelihoods, rootProbabilities)
	print result

def estimateRootProbabilitiesTest():
	results = []
	borrowability = 0.1
	result = estimateRootProbabilities(tree, contactStateTree, states, matrix, borrowability)
	print result

def findProbabilityOfDataIfThereIsContactAtTheRootTest():
	contactStateTree = eval(open("'Wakashan [waka1280]' 82A Order of Subject and Verb.txt", 'r').read())
	states = ['2 VS', '1 SV']
	stateLikelihoods = {'2 VS': 0.1, '1 SV': 0.9}
	print findProbabilityOfDataIfThereIsContactAtTheRoot(states, stateLikelihoods, contactStateTree)

def findLikelihoodIncludingContactAtTheRootTest():
	contactStateTree = eval(open("'Wakashan [waka1280]' 82A Order of Subject and Verb.txt", 'r').read())
	states = ['2 VS', '1 SV']
	stateLikelihoods = {'2 VS': 0.1, '1 SV': 0.9}
	rootBorrowability = 0.1
	rootProbabilities = {'2 VS': 0.1, '1 SV': 0.9}
	print findLikelihoodIncludingContactAtTheRoot(states, stateLikelihoods, rootProbabilities, contactStateTree, rootBorrowability)
findLikelihoodsIncludingContactWithoutRootProbabilitiesTest()	
