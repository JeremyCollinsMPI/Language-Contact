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



def calculateLikelihoodForNodeIncludingContact(inputTree, contactStateTree, node, states, matrix, borrowability):
	tree = inputTree.copy()
	children = findChildren(node)
	for child in children:
		if tree[child] == 'Unassigned':
			tree[node] = 'Unassigned'
			return tree, False
	tree[node] = {}
	for child in children:
		branchLength = float(findBranchLength(child))
		tree[node][child] = {}
		for state1 in states:
			tree[node][child][state1]  = {}
			for state2 in states:
				likelihood = tree[child]['states'][state2]
				if likelihood == '?':
					tree[node][child][state1][state2] = '?'
				else:
					contactStateMatrix = []
					for state in states:
						toAppend = []
						for state in states:
							toAppend.append(contactStateTree[child][state])
						contactStateMatrix.append(toAppend)
					matrixIncludingContact = np.multiply(contactStateMatrix, borrowability) + np.multiply(matrix, (1-borrowability))
					tree[node][child][state1][state2] = likelihood * findTransitionProbability(state1, state2, states, matrixIncludingContact, branchLength)
	tree[node]['states'] = {}
	for state1 in states:
		total = 1
		sub_totals = []
		for child in children:				
			sub_total = 0
			for state2 in states:
				likelihood = tree[node][child][state1][state2]
				if likelihood == '?':
					sub_total = '?'
				else:
					sub_total = sub_total + likelihood
			sub_totals.append(sub_total)
		sub_totals = [x for x in sub_totals if not x == '?']
		if len(sub_totals) == 0:
			total = '?'
		else:
			total = np.prod(sub_totals)
		tree[node]['states'][state1] = total
	return tree, True

def calculateLikelihoodForAllNodesIncludingContact(inputTree, contactStateTree, states, matrix, borrowability):
	tree = inputTree.copy()
	done = False
	while done == False:			
		done = True
		for node in tree:
			if tree[node] == 'Unassigned':
				tree, nodeDone = calculateLikelihoodForNodeIncludingContact(tree, contactStateTree, node, states, matrix, borrowability)
				if not nodeDone:
					done = False
	return tree

def findLikelihoodIncludingContact(inputTree, contactStateTree, states, matrix, borrowability):
	tree = calculateLikelihoodForAllNodesIncludingContact(inputTree, contactStateTree, states, matrix, borrowability)
	root = findRoot(tree)
	total = 0
	for state in states:
		if tree[root]['states'][state] == '?':
			return 1
		else:
			total = total + tree[root]['states'][state]
	total = total/len(states)
	return total
	
def findLikelihoodsIncludingContactWithoutRootProbabilities(inputTree, contactStateTree, states, matrix, borrowability):
	tree = calculateLikelihoodForAllNodesIncludingContact(inputTree, contactStateTree, states, matrix, borrowability)
	root = findRoot(tree)
	results = {}
	for state in states:
		if tree[root]['states'][state] == '?':
			results[state] = 1
		else:
			results[state] = tree[root]['states'][state]
	return results

def findLikelihoodIncludingContactAndRootProbabilities(states, stateLikelihoods, rootProbabilities):
	total = 0
	for state in states:
		rootProbability = rootProbabilities[state]
		stateLikelihood = stateLikelihoods[state]
		total = total + (rootProbability * stateLikelihood)
	return total

def estimateRootProbabilities(inputTree, contactStateTree, states, matrix, borrowability):
	stateLikelihoods = findLikelihoodsIncludingContactWithoutRootProbabilities(inputTree, contactStateTree, states, matrix, borrowability)
	result = []
	for i in xrange(11):
		rootProbabilities = {}
		rootProbabilities[states[0]] = i/10
		rootProbabilities[states[1]] = 1 - rootProbabilities[states[0]]
		likelihood = findLikelihoodIncludingContactAndRootProbabilities(states, stateLikelihoods, rootProbabilities)
		result.append(likelihood)
	return result

def findProbabilityOfDataIfThereIsContactAtTheRoot(states, stateLikelihoods, contactStateTree):
	total = 0
	root = findRoot(contactStateTree)
	for state in states:
		total = total + (stateLikelihoods[state] * contactStateTree[root][state])
	return total

def findLikelihoodIncludingContactAtTheRoot(states, stateLikelihoods, rootProbabilities, contactStateTree, rootBorrowability):
	root = findRoot(contactStateTree)
	probabilityOfDataWithoutContact = findLikelihoodIncludingContactAndRootProbabilities(states, stateLikelihoods, rootProbabilities)
	probabilityOfDataWithContact = findProbabilityOfDataIfThereIsContactAtTheRoot(states, stateLikelihoods, contactStateTree)	
	total = ((1 - rootBorrowability) * probabilityOfDataWithoutContact) + (rootBorrowability * probabilityOfDataWithContact)
	return total
	
	