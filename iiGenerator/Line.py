import pandas as pd
from xml.etree import ElementTree as etree
from pprint import pprint
from yattag import *
#------------------------------------------------------------------------------------------------------------------------
class Line:

   tierInfo = []
   rootElement = None
   tierElements = []
   doc = None
   lineNumber = None

   def __init__(self, doc, lineNumber):
     self.doc = doc
     self.lineNumber = lineNumber
     self.rootElement = doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
     self.allElements = findChildren(self.doc, self.rootElement)
       # need tier info to guide traverse
     self.tierInfo = [doc.attrib for doc in doc.findall("TIER")]
       # [{'LINGUISTIC_TYPE_REF': 'default-lt', 'TIER_ID': 'AYA'},
       #  {'LINGUISTIC_TYPE_REF': 'phonemic', 'PARENT_REF': 'AYA', 'TIER_ID': 'AYA2'},
       #  {'LINGUISTIC_TYPE_REF': 'translation', 'PARENT_REF': 'AYA', 'TIER_ID': 'ENG'},
       # {'LINGUISTIC_TYPE_REF': 'translation', 'PARENT_REF': 'AYA2', 'TIER_ID': 'GL'}]
     self.tbl = buildTable(doc, self.allElements)

   def getTierCount(self):
       return(len(self.tierElements))

   def getTable(self):
     return(self.tbl)

   def classifyTier(self, tierNumber):
     assert(tierNumber < self.getTable().shape[0])
     tierInfo = self.getTable().ix[tierNumber].to_dict()
     tierType = tierInfo['LINGUISTIC_TYPE_REF']
     hasTimes = tierInfo['START'] >= 0 and tierInfo['END'] >= 0
     hasText = tierInfo['TEXT'] != None
     hasTokenizedText = False
     if(hasText):
        hasTokenizedText = tierInfo['TEXT'].find("\t") > 0
     if((tierType == "default-lt") and (hasTimes)):
        return("spokenText")
     if(tierType == "phonemic" and hasTokenizedText):
        return("tokenizedWords")
     if(tierType == "translation" and hasTokenizedText):
        return("tokenizedGlosses")
     if(tierType == "translation" and hasText and not hasTokenizedText):
        return("freeTranslation")
     return ("unrecognized")


   #----------------------------------------------------------------------------------------------------
   def show(self):

      pprint(vars(self))

   #----------------------------------------------------------------------------------------------------
   def getSpokenText(self):
     return(self.tbl.ix[0, "TEXT"])

   #----------------------------------------------------------------------------------------------------
   def spokenTextToHtml(self, htmlDoc, tierNumber): # , lineNumber):

     tierObj = self.getTable().ix[tierNumber].to_dict()
     speechText = tierObj['TEXT']
     with htmlDoc.tag("div", klass="speech-tier"):
        htmlDoc.text(speechText)

   #----------------------------------------------------------------------------------------------------
   def tokenizedWordsToHtml(self, htmlDoc, tierNumber):

     tierObj = self.getTable().ix[tierNumber].to_dict()
     phonemes = tierObj['TEXT'].split("\t")
     styleString = "grid-template-columns: %s;" % ''.join(["%dch " % len(p) for p in phonemes])
     with htmlDoc.tag("div", klass="phoneme-tier", style=styleString):
        for phoneme in phonemes:
          with htmlDoc.tag("div", klass="phoneme-cell"):
             htmlDoc.text(phoneme)

   #----------------------------------------------------------------------------------------------------
   def tokenizedGlossesToHtml(self, htmlDoc, tierNumber):

     tierObj = self.getTable().ix[tierNumber].to_dict()
     phonemeGlosses = tierObj['TEXT'].split("\t")

     styleString = "grid-template-columns: %s;" % ''.join(["%dch " % len(p) for p in phonemeGlosses])
     with htmlDoc.tag("div", klass="phoneme-tier", style=styleString):
        for phonemeGloss in phonemeGlosses:
          with htmlDoc.tag("div", klass="phoneme-cell"):
             htmlDoc.text(phonemeGloss)

   #----------------------------------------------------------------------------------------------------
   def freeTranslationToHtml(self, htmlDoc, tierNumber):

     tierObj = self.getTable().ix[tierNumber].to_dict()
     speechText = tierObj['TEXT']
     with htmlDoc.tag("div", klass="freeTranslation-tier"):
        htmlDoc.text(speechText)

   #----------------------------------------------------------------------------------------------------
   def getHtmlHead(self):

      playerLibrary = open("player2.js").read();
      #s = "<head><script src='http://localhost:9999/player2.js'></script></head>"
      s = "<head></head>"
      return(s)

   #----------------------------------------------------------------------------------------------------
   def toHtml(self):
      tbl = self.getTable()
      tierCount = self.getTable().shape[0]
      html = "<html>"
      html += self.getHtmlHead();
      html += "<body><table border='1'>"
      translationHtml = ""
      storyLineNumber = 1
      for tierNumber in range(tierCount):
         tierType = self.classifyTier(tierNumber)
         print("tier number %d, type %s" % (tierNumber, tierType))
         if(tierType == "spokenText"):
            html += self.spokenTextToHtml(tierNumber, storyLineNumber)
         elif(tierType == "tokenizedWords"):
            html += self.tokenizedWordsToHtml(tierNumber)
         elif(tierType == "tokenizedGlosses"):
            html += self.tokenizedGlossesToHtml(tierNumber)
         elif(tierType == "freeTranslation"):
            translationHtml = self.freeTranslationToHtml(tierNumber)
      html += translationHtml
      html += "</table></body></html>"
      html = html.replace("\n", "")

      return(html)

   #----------------------------------------------------------------------------------------------------
   def tmp(self):
               # should be exactly one alignable tier, so it is safe to get the first one found
      alignableTierType_id = self.doc.find("LINGUISTIC_TYPE[@TIME_ALIGNABLE='true']").attrib["LINGUISTIC_TYPE_ID"]
      pattern = "TIER[@LINGUISTIC_TYPE_REF='%s']" % alignableTierType_id
      alignableTierId = self.doc.find(pattern).attrib["TIER_ID"]
         # we could use alignableTierId to select the tier, then the ALIGNABLE_ANNOTATION[lineNumber]
         # but the ALIGNABLE_ANNOTATION[lineNumber] tag accomplishes the same thing
      alignableElement = self.doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
      alignableElementId = alignableElement.attrib["ANNOTATION_ID"]
      timeSlot1 = alignableElement.attrib["TIME_SLOT_REF1"]
      timeSlot2 = alignableElement.attrib["TIME_SLOT_REF2"]

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
     #print("elementText: %s" % elementText)
     text.append(elementText)

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

   return(tbl)

#------------------------------------------------------------------------------------------------------------------------

#filename0 = "../testData/daylight77a.eaf"
#filename1 = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
#doc1 = etree.parse(filename0)
#doc2 = etree.parse(filename1)
#doc = doc2



