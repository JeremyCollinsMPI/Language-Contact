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
from NewContact import *
import random

random.seed(10)

trees = open('trees.txt').readlines()

def addNodeToListTest():
	string = "(('Amux [amux1234]':1)'Southwestern Dargwa [sout3261]-l-':1)'South Dargwa [sout3260]':1"
	list = []
	list = addNodeToList(list, string, randomOrder = False)
	print list

def createNodeListTest():
	tree = trees[175].strip('\n')
	listA = createNodeList(tree, randomOrder = True)
	listB = createNodeList(tree, randomOrder = True)
	print listA
	if not listA == listB:
		print 'They are different'
	
def createTemporalOrderTest():
	temporalOrder = createTemporalOrder(trees, method = 'random')
	for member in temporalOrder:
		print member
	outputFile = open('temporalOrder.txt','w')
	outputFile.write('\n'.join(temporalOrder))

def findNodesToIncludeTest():
	temporalOrder = createTemporalOrder(trees, method = 'random')
	outputFile = open('temporalOrder.txt','w')
	outputFile.write('\n'.join(temporalOrder))
	node = ''
	toStopAt = "'Germanic [germ1287]'"
# 	toStopAt = "'Palaihnihan [pala1350]'"
	for member in temporalOrder:
		nodeName = findNodeNameWithoutStructure(member)
		if nodeName == toStopAt:
			node = member
	nodesToInclude = findNodesToInclude(node, temporalOrder)	
	print nodesToInclude
	return nodesToInclude
	
def checkNodeIsMostRecentTest():
	nodesToInclude = findNodesToIncludeTest()
	for i in xrange(len(nodesToInclude.keys())):
		node = nodesToInclude.keys()[i]
		print node
		print checkNodeIsMostRecent(node, nodesToInclude)

def newFindNodesWithinACertainDistanceTest():
	nodes = {}
	nodesFile = open('reconstructedLocations.txt','r').readlines()
	for line in nodesFile:
		line = line.split('\t')
		try:
			nodes[line[0]] = eval(line[1].strip('\n'))
		except:
			print 'Cannot add node location:'
			print line
	longitude = 0
	latitude = 52
	distanceThreshold = None
	limit = 20
# 	print nodes
# 	nodesToInclude = {"'Breton [bret1244][bre]-l-':1":''}
	useAllNodes = False
	print findNodesWithinACertainDistance(nodes, latitude, longitude, distanceThreshold, limit, nodesToInclude, useAllNodes)






def findNodesWithinACertainDistanceTest():
	nodes = {}
	nodesFile = open('reconstructedLocations.txt','r').readlines()
	for line in nodesFile:
		line = line.split('\t')
		try:
			nodes[line[0]] = eval(line[1].strip('\n'))
		except:
			print 'Cannot add node location:'
			print line
	longitude = 0
	latitude = 52
	distanceThreshold = None
	limit = 20
# 	print nodes
	nodesToInclude = "'Breton [bret1244][bre]-l-':1"
	useAllNodes = False
 	print findNodesWithinACertainDistance(nodes, latitude, longitude, distanceThreshold, limit, nodesToInclude, useAllNodes)

def findStatesFromNodesWithinACertainDistanceTest():
	nodes = {}
	reconstructedStates = {}
	nodesFile = open('reconstructedLocations.txt','r').readlines()
	reconstructedStatesFile = open('reconstruction.txt','r').readlines()	
	for line in nodesFile:
		line = line.split('\t')
		try:
			nodes[line[0]] = eval(line[1].strip('\n'))
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
	longitude = 0
	latitude = 52
	distanceThreshold = None
	limit = 20
	print nodes
	nodesToInclude = "'Breton [bret1244][bre]-l-':1"
	useAllNodes = True		
	print findStatesFromNodesWithinACertainDistance(reconstructedStates, nodes, latitude, longitude, distanceThreshold, limit, nodesToInclude, useAllNodes)

def newFindContactStatesForNodeTest():
	temporalOrderFile = open('temporalOrder.txt', 'r').readlines()
	temporalOrder = [x.strip('\n') for x in temporalOrderFile]
	distanceThreshold = None
	limit = 5
	nodesLocations = {}
	reconstructedStates = {}
	nodesFile = open('reconstructedLocations.txt','r').readlines()
	reconstructedStatesFile = open('reconstruction.txt','r').readlines()
	featureName = '83A Order of Object and Verb'
	dataFrame = assignIsoValues('language.csv')
	dataFrame = filterDataFrame(dataFrame, featureName, ['1 OV', '2 VO'])
	states = findStates(dataFrame, featureName)	
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
	treeString = trees[175]
	inputTree = createTree(treeString.strip('\n'))
	inputTree = ensureAllTipsHaveIsoCodes(inputTree)
	node = "'Breton [bret1244][bre]-l-':1"
	node = "(('Gothic [goth1244][got]-l-':1)'East Germanic [east2805]':1,(((('Dalecarlian [dale1238][qer]-l-':1,('Swedish [swed1254][swe]-l-':1)'East Swedic [east2781]':1)'East-Central Swedic [east2780]':1)'North Scandinavian [nort3266]':1,('Danish [dani1285][dan]-l-':1,'Jutish [juti1236][jut]-l-':1)'South Scandinavian [sout3248]':1,(('Faroese [faro1244][fao]-l-':1,'Icelandic [icel1247][isl]-l-':1)'Icelandic-Faroese [icel1246]':1,'Norwegian [norw1258][nor]-l-':1,'Old Norse [oldn1244][non]-l-':1)'West Scandinavian [west2805]':1)'North Germanic [nort3160]':1,((('German [stan1295][deu]-l-':1,('Luxembourgish [luxe1241][ltz]-l-':1,'Mainfr\xc3\x83\xc2\xa4nkisch [main1267][vmf]-l-':1,('K\xc3\x83\xc2\xb6lsch [kols1241][ksh]-l-':1,'Limburgan [limb1263][lim]-l-':1)'Ripuarian [ripu1236]':1)'Middle Franconian [midd1319]':1,'Old Frankish [fran1264][frk]-l-':1,('Hunsrik [riog1239][hrx]-l-':1,('Pennsylvania German [penn1240][pdc]-l-':1,'Pfaelzisch [pala1330][pfl]-l-':1)'Palatinate [pala1355]':1,'Upper Saxon [uppe1400][sxu]-l-':1)'Rhine Franconian [rhin1244]':1,('Lower Silesian [lowe1388][sli]-l-':1,'Wymysorys [wymy1235][wym]-l-':1)'Schlesisch-Wilmesau [schl1237]':1,'Unserdeutsch [unse1236][uln]-l-':1)'High Franconian [high1287]':1,(('Afrikaans [afri1274][afr]-l-':1,'Oorlams [oorl1238][oor]-l-':1)'Afrikaansic [afri1273]':1,(('Middle Dutch [midd1321][dum]-l-':1,('Dutch [dutc1256][nld]-l-':1,('Berbice Creole Dutch [berb1259][brc]-l-':1,'Negerhollands [nege1244][dcr]-l-':1,'Skepi Creole Dutch [skep1238][skw]-l-':1)'Dutch Caribbean Creole [dutc1257]':1,'Javindo [javi1237][jvd]-l-':1,'Petjo [petj1238][pey]-l-':1,'Vlaams [vlaa1240][vls]-l-':1,'Zeeuws [zeeu1238][zea]-l-':1)'Modern Dutch [mode1257]':1)'Middle-Modern Dutch [midd1347]':1,'Old Dutch [oldd1237][odt]-l-':1)'Macro-Dutch [macr1270]':1)'Low Franconian [wese1235]':1)'Franconian [fran1268]':1,(('Middle High German [midd1343][gmh]-l-':1,((('Colonia Tovar German [colo1254][gct]-l-':1,'Swabian [swab1242][swg]-l-':1,'Swiss German [swis1247][gsw]-l-':1,'Walser [wals1238][wae]-l-':1)'Alemannic [alem1243]':1,('Bavarian [bava1246][bar]-l-':1,'Cimbrian [cimb1238][cim]-l-':1,'Hutterite German [hutt1235][geh]-l-':1,'M\xc3\x83\xc2\xb3cheno [moch1255][mhn]-l-':1)'Bayerisch [baye1239]':1)'Alpine Germanic [uppe1397]':1,'Yiddish [yidd1255][yid]':1)'Modern High German [mode1258]':1)'Middle-Modern High German [midd1349]':1,'Old High German {ca. 750-1050} [oldh1241][goh]-l-':1)'High German [high1286]':1,(((('Achterhoeks [acht1238][act]-l-':1,'Drents [dren1238][drt]-l-':1,'Eastern Low German [nort2627][nds]-l-':1,('Eastern Frisian [east2288][frs]-l-':1,'Gronings [gron1242][gos]-l-':1)'Ostfriesisch-Groningisch [ostf1234]':1,'Plautdietsch [plau1238][pdt]-l-':1,'Sallands [sall1238][sdz]-l-':1,'Stellingwerfs [stel1238][stl]-l-':1,'Twents [twen1241][twd]-l-':1,'Veluws [velu1238][vel]-l-':1,'Westphalien [west2356][wep]-l-':1)'Low German [lowg1239]':1,'Middle Low German [midd1318][gml]-l-':1)'Middle-Modern Low German [midd1345]':1,'Old Saxon [olds1250][osx]-l-':1)'Alts\xc3\x83\xc2\xa4chsisch [alts1234]':1,(((('English [stan1293][eng]-l-':1,((((('Bajan [baja1265][bjs]-l-':1,'Guyanese Creole English [creo1235][gyn]-l-':1,'Trinidadian Creole English [trin1276][trf]-l-':1)'Barbados-Trinidad [barb1267]':1,'Virgin Islands Creole English [virg1240][vic]-l-':1)'Barbados-Eustatius [barb1266]':1,('Antigua and Barbuda Creole English [anti1245][aig]-l-':1,('Afro-Seminole Creole [afro1254][afs]-l-':1,('Bahamas Creole English [baha1260][bah]-l-':1,'Turks And Caicos Creole English [turk1310][tch]-l-':1)'Bahamian Gullah [baha1261]':1,'Sea Island Creole English [gull1241][gul]-l-':1)'Gullah [gull1243]':1)'Gullah-Nevis-Antigua [gull1242]':1,(('Grenadian Creole English [gren1247][gcl]-l-':1,'Tobagonian Creole English [toba1282][tgh]-l-':1)'Grenada-Tobago Creole [gren1248]':1,'Vincentian Creole English [vinc1243][svc]-l-':1)'Vincent-Grenadian Creole [vinc1244]':1)'Eastern Caribbean Creole [east2759]':1,(('Jamaican Creole English [jama1262][jam]-l-':1,'Limonese Creole [limo1249][qlm]-l-':1)'Jamaicanic [jama1264]':1,(('Belize Kriol English [beli1260][bzj]-l-':1,'Nicaragua Creole English [nica1252][bzk]-l-':1)'Belize-Miskito Creole English [beli1261]':1,'San Andres Creole English [sana1297][icr]-l-':1)'Miskitoic Creole English [misk1243]':1)'Western Caribbean Creole [west2854]':1)'Caribbean English Creole [cari1284]':1,((('Aukan [ndyu1242][djk]-l-':1,'Kwinti [kwin1243][kww]-l-':1)'Ndyuka [suri1272]':1,'Sranan Tongo [sran1240][srn]-l-':1)'Eastern Maroons [sran1241]':1,'Saramaccan [sara1340][srm]-l-':1)'Surinamese Creole English [suri1275]':1,('Ghanaian Pidgin English [ghan1244][gpe]-l-':1,'Krio [krio1253][kri]-l-':1,('Cameroon Pidgin [came1254][wes]-l-':1,'Nigerian Pidgin [nige1257][pcm]-l-':1)'Nigeria-Cameroon Creole English [nige1258]':1,'Pichi [fern1234][fpe]-l-':1)'West African Creole English [west2851]':1)'Guinea Coast Creole English [guin1259]':1,(('Bislama [bisl1239][bis]-l-':1,'Pijin [piji1239][pis]-l-':1,'Tok Pisin [tokp1240][tpi]-l-':1,'Torres Strait Creole [torr1261][tcs]-l-':1)'Early Melanesian Pidgin [earl1243]':1,'Hawai''i Creole English [hawa1247][hwc]-l-':1,'Kriol [krio1252][rop]-l-':1)'Pacific Creole English [paci1280]':1,'Pitcairn-Norfolk [pitc1234][pih]-l-':1)'Macro-English [macr1271]':1,'Middle English [midd1317][enm]-l-':1)'Mercian [merc1242]':1,'Old English {ca. 450-1100} [olde1238][ang]-l-':1,'Scots [scot1243][sco]-l-':1)'Anglian [angl1265]':1,('Northern Frisian [nort2626][frr]-l-':1,'Old Frisian [oldf1241][ofs]-l-':1,'Saterfriesisch [sate1242][stq]-l-':1,'Western Frisian [west2354][fry]-l-':1)'Frisian [fris1239]':1)'Anglo-Frisian [angl1264]':1)'North Sea Germanic [nort3175]':1)'West Germanic [west2793]':1)'Northwest Germanic [nort3152]':1)'Germanic [germ1287]':1"
	tree = newFindContactStatesForNode(inputTree, node, states, reconstructedStates, nodesLocations, temporalOrder, distanceThreshold, limit)
	print tree[node]

def newFindContactStatesForAllNodesTest():
	temporalOrderFile = open('temporalOrder.txt', 'r').readlines()
	temporalOrder = [x.strip('\n') for x in temporalOrderFile]
	distanceThreshold = None
	limit = 5
	nodesLocations = {}
	reconstructedStates = {}
	nodesFile = open('reconstructedLocations.txt','r').readlines()
	reconstructedStatesFile = open('reconstruction.txt','r').readlines()
	featureName = '83A Order of Object and Verb'
	dataFrame = assignIsoValues('language.csv')
	dataFrame = filterDataFrame(dataFrame, featureName, ['1 OV', '2 VO'])
	states = findStates(dataFrame, featureName)	
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
	treeString = trees[175]
	print 'processing'
	inputTree = createTree(treeString.strip('\n'))
	inputTree = ensureAllTipsHaveIsoCodes(inputTree)
	print 'beginning'
	tree = newFindContactStatesForAllNodes(inputTree, states, reconstructedStates, nodesLocations, temporalOrder, distanceThreshold, limit)
	print tree

def newFindStatesFromNodesWithinACertainDistanceTest():
	nodes = {}
	reconstructedStates = {}
	nodesFile = open('reconstructedLocations.txt','r').readlines()
	reconstructedStatesFile = open('reconstruction.txt','r').readlines()	
	for line in nodesFile:
		line = line.split('\t')
		try:
			nodes[line[0]] = eval(line[1].strip('\n'))
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
	longitude = 0
	latitude = 52
	distanceThreshold = None
	limit = 20
	print nodes
	nodesToInclude = {"'Breton [bret1244][bre]-l-':1"}
	useAllNodes = True		
	print newFindStatesFromNodesWithinACertainDistance(reconstructedStates, nodes, latitude, longitude, distanceThreshold, limit, nodesToInclude, useAllNodes)



# checkNodeIsMostRecentTest()
# findNodesToIncludeTest()
# checkNodeIsMostRecentTest()
# newFindNodesWithinACertainDistanceTest()
# newFindStatesFromNodesWithinACertainDistanceTest()
# newFindContactStatesForNodeTest()
newFindContactStatesForAllNodesTest()