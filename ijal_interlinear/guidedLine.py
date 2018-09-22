import pandas as pd
from xml.etree import ElementTree as etree
from pprint import pprint
from yattag import *
import pdb
#------------------------------------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------------------------------
class GuidedLine:

   tierInfo = []
   spokenTextID = ""
   rootElement = None
   rootID = None
   tierElements = []
   doc = None
   lineNumber = None
   soundFile = None
   grammaticalTerms = None


   def __init__(self, doc, lineNumber, tierGuide, grammaticalTerms=[]):
     self.doc = doc
     self.lineNumber = lineNumber
     self.tierGuide = tierGuide
     self.grammaticalTerms = grammaticalTerms
     self.rootElement = self.doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
     self.allElements = findChildren(self.doc, self.rootElement)
     self.tblRaw = buildTable(doc, self.allElements)
     self.tbl = standardizeTable(self.tblRaw, tierGuide)
     self.morphemePacking = tierGuide["morphemePacking"]

     self.categories = categories = self.tbl["category"].tolist()
     self.speechRow = self.categories.index("speech")
     self.translationRow = self.categories.index("translation")
     tierCount = self.tbl.shape[0]
     self.morphemeRows = [i for i in range(tierCount) if self.categories[i] == "morpheme"]
     self.morphemeGlossRows = [i for i in range(tierCount) if self.categories[i] == "morphemeGloss"]


   def getTierCount(self):
       return(self.getTable().shape[0])

   def getTable(self):
     return(self.tbl)

   #----------------------------------------------------------------------------------------------------
   def show(self):

      pprint(vars(self))

   #----------------------------------------------------------------------------------------------------
   def getSpokenText(self):

    categories = self.tbl["category"].tolist()
    row = categories.index("speech")
    return(self.tbl.ix[0, "TEXT"])


   #----------------------------------------------------------------------------------------------------
   def htmlLeadIn(self, htmlDoc, audioDirectory):

      oneBasedLineNumber = self.lineNumber + 1
      text = "%d)" % oneBasedLineNumber
      htmlDoc.text(text)
      lineID = self.rootID
      audioTag = '<audio id="%s"><source src="%s/%s.wav"/></audio>' % (lineID, audioDirectory, lineID)
      htmlDoc.asis(audioTag)
      imageURL = "https://www.americanlinguistics.org/wp-content/uploads/speaker.png"
      buttonTag = '<button onclick="playSample(\'%s\')"><img src=\'%s\'/></button>' % (lineID, imageURL)
      htmlDoc.asis(buttonTag)


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
def standardizeTable(tbl, tierGuide):

   tierNames = tbl["TIER_ID"].tolist()
   permittedNames = [tierGuide[k] for k in tierGuide]
   shared = set(tierNames).intersection(permittedNames)

   tbl_trimmed = tbl.loc[tbl['TIER_ID'].isin(shared)]

   tierNames = tbl_trimmed["TIER_ID"].tolist()

      # reverse the guide so we can map from user-supplied and often idiosyncratic
      # TIER_ID values, to the IJAL standard types: speech, translation, morpheme, morphemeGloss

   revGuide = {v: k for k, v in tierGuide.items()}
   ids = tbl_trimmed["TIER_ID"]
   standardIDs = [revGuide[key] for key in ids]

      # add a new column to the table.  we will use this later to assemble the html
   tbl_final = tbl_trimmed.assign(category=standardIDs)

   return(tbl_final)

#------------------------------------------------------------------------------------------------------------------------


