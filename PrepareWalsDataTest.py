from PrepareWalsData import *
from general import * 
import random

def lookUpValueForIsoTest():
	dataFrame = assignIsoValues('language.csv')
	value = lookUpValueForIso('zoc', dataFrame, '2A Vowel Quality Inventories')
	value = lookUpValueForIso('ood', dataFrame, '89A Order of Numeral and Noun')
	print value
def findStatesTest():
	dataframe = assignIsoValues('language.csv')
	print findStates(dataframe, '2A Vowel Quality Inventories')



lookUpValueForIsoTest()



# dataFrame = assignIsoValues('language.csv')
# # print dataFrame['89A Order of Numeral and Noun']
# dataFrame = dataFrame['89A Order of Numeral and Noun'].dropna()
# print dataFrame.loc['fra']

