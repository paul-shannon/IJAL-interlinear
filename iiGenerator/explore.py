from xml.etree import ElementTree as etree

tierInfo = []
tierElements = []
lineNumber = None
filename0 = "../testData/daylight77a.eaf"
filename1 = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
doc1 = etree.parse(filename0)
doc2 = etree.parse(filename1)
doc = doc2
lineNumber = 0
tierInfo = [doc.attrib for doc in doc.findall("TIER")]
    # [{'LINGUISTIC_TYPE_REF': 'default-lt', 'TIER_ID': 'AYA'},
    #  {'LINGUISTIC_TYPE_REF': 'phonemic', 'PARENT_REF': 'AYA', 'TIER_ID': 'AYA2'},
    #  {'LINGUISTIC_TYPE_REF': 'translation', 'PARENT_REF': 'AYA', 'TIER_ID': 'ENG'},
    #  {'LINGUISTIC_TYPE_REF': 'translation', 'PARENT_REF': 'AYA2', 'TIER_ID': 'GL'}]
rootElement = doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
parentRef = rootElement.attrib["ANNOTATION_ID"]
nextTierIndex = 1
done = False
while !done:

nextTierType = tierInfo[nextTierIndex]["LINGUISTIC_TYPE_REF"]
patternValues = (nextTierType, parentRef)
pattern = "TIER[@LINGUISTIC_TYPE_REF='%s']/ANNOTATION/REF_ANNOTATION[@ANNOTATION_REF='%s']" % patternValues
childElement = doc.find(pattern)
if(childElement == None):
   done = True
else:
   tierElements.append(childElement)
   nextTierIndex += 1
   parentRef = childElement.attrib["ANNOTATION_ID"]


