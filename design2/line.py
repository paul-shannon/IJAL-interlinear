import pandas as pd
from xml.etree import ElementTree as etree
from pprint import pprint
from yattag import *
import pdb
#------------------------------------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------------------------------
class Line:

   tierInfo = []
   spokenTextID = ""
   rootElement = None
   rootID = None
   tierElements = []
   doc = None
   lineNumber = None
   soundFile = None

   def __init__(self, doc, lineNumber):
     self.doc = doc
     self.lineNumber = lineNumber
     self.rootElement = self.doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
     self.allElements = findChildren(self.doc, self.rootElement)
       # need tier info to guide traverse
     self.tierInfo = [doc.attrib for doc in doc.findall("TIER")]
       # [{'LINGUISTIC_TYPE_REF': 'default-lt', 'TIER_ID': 'AYA'},
       #  {'LINGUISTIC_TYPE_REF': 'phonemic', 'PARENT_REF': 'AYA', 'TIER_ID': 'AYA2'},
       #  {'LINGUISTIC_TYPE_REF': 'translation', 'PARENT_REF': 'AYA', 'TIER_ID': 'ENG'},
       #  {'LINGUISTIC_TYPE_REF': 'translation', 'PARENT_REF': 'AYA2', 'TIER_ID': 'GL'}]
     self.tbl = buildTable(doc, self.allElements)
     self.rootID = self.deduceSpokenTextID()


   def getImmediateChildrenOfRoot(self):
      rootID = self.deduceSpokenTextID()

   def getTierCount(self):
       return(self.getTable().shape[0])

   def getTable(self):
     return(self.tbl)


   #----------------------------------------------------------------------------------------------------
   def deduceSpokenTextID(self):

      return(self.tbl.loc[pd.isnull(self.tbl['ANNOTATION_REF'])]["ANNOTATION_ID"][0])

   #----------------------------------------------------------------------------------------------------
   def deduceWordRepresentation(self):

      rootSpokenTextID = self.deduceSpokenTextID()
      tbl_emptyLinesRemoved = self.tbl.query("TEXT != ''")
         # do not wish to count children with empty text fields
      numberOfDirectChildrenOfRoot = tbl_emptyLinesRemoved.ix[self.tbl["ANNOTATION_REF"] == rootSpokenTextID].shape[0]
         # add test for present but empty word tier, as in monkey line 1
      if(numberOfDirectChildrenOfRoot == 1):
         return("noWords")
      elif(numberOfDirectChildrenOfRoot == 2):
         return("tokenizedWords")
      elif(numberOfDirectChildrenOfRoot > 2):
         return("wordsDistributedInElements")
      else:
         print("unrecognized word representation")

   #----------------------------------------------------------------------------------------------------
   def getWordRepresentation(self):
      return(self.wordRepresentation)

   #----------------------------------------------------------------------------------------------------
   def show(self):

      pprint(vars(self))

   #----------------------------------------------------------------------------------------------------
   def getSpokenText(self):
     return(self.tbl.ix[0, "TEXT"])


#------------------------------------------------------------------------------------------------------------------------
def findChildren(doc, rootElement):

   elementsToDo = [rootElement]
   elementsCompleted = []

   while(len(elementsToDo) > 0):
      currentElement = elementsToDo[0]
      parentRef = currentElement.attrib["ANNOTATION_ID"]
      pattern = "TIER/ANNOTATION/REF_ANNOTATION[@ANNOTATION_REF='%s']" % parentRef
      childElements = doc.findall(pattern)
      elementsToDo.remove(currentElement)
      elementsCompleted.append(currentElement)
      if(len(childElements) > 0):
         elementsToDo.extend(childElements)

   return(elementsCompleted)

def extractAudio(doc, rootElement, masterAudioFile):

#------------------------------------------------------------------------------------------------------------------------
def buildTable(doc, lineElements):

   tbl_elements = pd.DataFrame(e.attrib for e in lineElements)
   #print(tbl_elements)

   #pdb.set_trace()
   startTimeSlotID = tbl_elements.ix[0, 'TIME_SLOT_REF1']
   pattern = "TIME_ORDER/TIME_SLOT[@TIME_SLOT_ID='%s']" % startTimeSlotID
   startTime = int(doc.find(pattern).attrib["TIME_VALUE"])
   startTimes = [startTime]
   rowCount = tbl_elements.shape[0]
   for i in range(1, rowCount):
     startTimes.append(float('NaN'))

   endTimeSlotID   = tbl_elements.ix[0, 'TIME_SLOT_REF2']
   pattern = "TIME_ORDER/TIME_SLOT[@TIME_SLOT_ID='%s']" % endTimeSlotID
   endTime = int(doc.find(pattern).attrib["TIME_VALUE"])
   endTimes = [endTime]
   for i in range(1, rowCount):
     endTimes.append(float('NaN'))
   tbl_times = pd.DataFrame({"START": startTimes, "END": endTimes})
   #print(tbl_times)


   ids = [e.attrib["ANNOTATION_ID"] for e in lineElements]
   tierInfo = []
   text = []

   for id in ids:
     parentPattern = "*/*/*/[@ANNOTATION_ID='%s']/../.." % id
     tierAttributes = doc.find(parentPattern).attrib
     tierInfo.append(tierAttributes)
     childPattern = "*/*/*/[@ANNOTATION_ID='%s']/ANNOTATION_VALUE" % id
     elementText = doc.find(childPattern).text
     if(elementText is None):
        elementText = ""
     #print("elementText: %s" % elementText)
     text.append(elementText.strip())

   tbl_tierInfo = pd.DataFrame(tierInfo)

   tbl_text = pd.DataFrame({"TEXT": text})

   # print("---- tbl_elements")
   # print(tbl_elements)
   #
   # print("---- tbl_tierInfo")
   # print(tbl_tierInfo)
   #
   # print("---- tbl_times")
   # print(tbl_times)
   #
   # print("---- tbl_text")
   # print(tbl_text)

   tbl = pd.concat([tbl_elements, tbl_tierInfo, tbl_times, tbl_text], axis=1)
   preferredColumnOrder = ["ANNOTATION_ID", "LINGUISTIC_TYPE_REF", "START", "END", "TEXT", "ANNOTATION_REF", "TIME_SLOT_REF1", "TIME_SLOT_REF2",
                           "PARENT_REF", "TIER_ID"]
   tbl = tbl[preferredColumnOrder]
   textLengths = [len(t) for t in tbl["TEXT"].tolist()]
   tbl["TEXT_LENGTH"] = textLengths
   hasTabs = ["\t" in t for t in tbl["TEXT"].tolist()]
   tbl["HAS_TABS"] = hasTabs
   hasSpaces = [" " in t for t in tbl["TEXT"].tolist()]
   tbl["HAS_SPACES"] = hasSpaces
      # eliminate rows with no text
      # leave it in for now, take the tiers at face value, handle empty lines in toHTML
   tbl = tbl.query("TEXT != ''").reset_index(drop=True)
   return(tbl)

#------------------------------------------------------------------------------------------------------------------------


