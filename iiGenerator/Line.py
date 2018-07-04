import pandas as pd
from xml.etree import ElementTree as etree
from pprint import pprint
from yattag import *
import pdb
#------------------------------------------------------------------------------------------------------------------------
class Line:

   tierInfo = []
   spokenTextID = ""
   rootElement = None
   tierElements = []
   doc = None
   lineNumber = None
      # phoneme tokens and their gloss tokens are equal in number, often different in length,
      # and displayed in horizontal alignment, each vertical pair in a horizontal space
      # large enough to holder the longer of the two.  for instance, from Harry Moses
      # how daylight was stolen, line 3, fourth word, needs 18 character spaces
      #              gʷә-s-čal
      #              uncertain-means-get
      # this next member variable holds these values once calculated
   phonemeSpacing = []

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
       #  {'LINGUISTIC_TYPE_REF': 'translation', 'PARENT_REF': 'AYA2', 'TIER_ID': 'GL'}]
     self.tbl = buildTable(doc, self.allElements)
     self.rootSpokenTextID = self.deduceSpokenTextID()
     self.wordRepresentation = self.deduceWordRepresentation()

     #self.deduceStructure()
     #self.phonemeSpacing = [];
     #self.calculateSpacingOfPhonemeAndGlossTokens()


   def getImmediateChildrenOfRoot(self):
      rootID = self.deduceSpokenTextID()

   def getTierCount(self):
       return(len(self.tierElements))

   def getTable(self):
     return(self.tbl)

   def classifyTier(self, tierNumber):

     assert(tierNumber < self.getTable().shape[0])
     tierInfo = self.getTable().ix[tierNumber].to_dict()
     tierType = tierInfo['LINGUISTIC_TYPE_REF']
     hasTimes = tierInfo['START'] >= 0 and tierInfo['END'] >= 0
     hasText = tierInfo['TEXT'] != ""
     pdb.set_trace()
         # the root is the full spoken text, a single string, in practical orthography
         # is this tier a direct child of root?
         #   1) the full (untokenized) translation
         #   2) words, in one of (so far) two representations:
         #       a) phonetic transcription: tab-delimited text, with a child tier of glosses
         #       b) a set of direct children, each with 1 or 2 child elements of their own
     directRootChildElement = tierInfo["ANNOTATION_REF"] == self.rootSpokenTextID
     hasChildren = any((self.tbl["ANNOTATION_REF"] == tierInfo["ANNOTATION_ID"]).tolist())
     if(hasTimes):
        return("spokenText")
     if(not hasText):
        return("empty")
     if(directRootChildElement):
        if(hasChildren):
           return("nativeMorpheme")
        else:
           return("nativeGlossOrFreeTranslation")
     return("unrecognized")

#     hasTokenizedText = False
#     if(hasText):
#        hasTokenizedText = tierInfo['TEXT'].find("\t") > 0
#     if((hasTimes)):
#        return("spokenText")
#     if(tierType == "phonemic" and hasTokenizedText):
#        return("tokenizedWords")
#     if(tierType == "translation" and hasTokenizedText):
#        return("tokenizedGlosses")
#     if(tierType == "translation" and hasText and not hasTokenizedText):
#        return("freeTranslation")
#     return ("unrecognized")


   #----------------------------------------------------------------------------------------------------
   def deduceSpokenTextID(self):

      return(self.tbl.loc[pd.isnull(self.tbl['ANNOTATION_REF'])]["ANNOTATION_ID"][0])

   #----------------------------------------------------------------------------------------------------
   def deduceWordRepresentation(self):

      rootSpokenTextID = self.deduceSpokenTextID()
      numberOfDirectChildrenOfRoot = self.tbl.ix[self.tbl["ANNOTATION_REF"] == rootSpokenTextID].shape[0]
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
   def traverse(self):
      """
         assumes rootSpokenTextID and wordRepresentation have been figured out
      """
      rootID = self.rootSpokenTextID
      self.spokenTextRow = self.tbl.ix[self.tbl["ANNOTATION_ID"] == rootID].index[0]
      tbl = self.tbl  # allows more compact expressions

       # "noWords"   "tokenizedWords"  "wordsDistributedInElements"
      if(self.wordRepresentation == "noWords"):
         self.freeTranslationRow == self.tbl.ix[self.tbl["ANNOTATION_REF"] == rootID].index[0]
      elif(self.wordRepresentation == "tokenizedWords"):
         self.freeTranslationRow = tbl[(tbl.HAS_TABS == False) & (tbl.ANNOTATION_REF == self.rootSpokenTextID)].index.tolist()[0]
      elif(self.wordRepresentation == "wordsDistributedInElements"):
         self.freeTranslationRow = tbl[(tbl.HAS_SPACES == True) & (tbl.ANNOTATION_REF == self.rootSpokenTextID)].index.tolist()[0]

   #----------------------------------------------------------------------------------------------------
   def calculateSpacingOfPhonemeAndGlossTokens(self):

      #phonemesTier = line0.getTable().loc[tbl['LINGUISTIC_TYPE_REF'] == "phonemic"]['TEXT']
      #phonemeGlossesTier = line0.getTable().loc[tbl['LINGUISTIC_TYPE_REF'] == "translation"]['TEXT']
      import pdb; pdb.set_trace();
      phonemesTierText = self.getTable().ix[1]['TEXT']
      phonemeGlossesTierText = self.getTable().ix[3]['TEXT']
      phonemes = phonemesTierText.split("\t")
      phonemeGlosses = phonemeGlossesTierText.split("\t")
      print(phonemes)
      print(phonemeGlosses)
      assert(len(phonemes) == len(phonemeGlosses))
      for i in range(len(phonemes)):
         phonemeSize = len(phonemes[i])
         glossSize = len(phonemeGlosses[i])
         self.phonemeSpacing.append(max(phonemeSize, glossSize) + 1)

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
     #styleString = "grid-template-columns: %s;" % ''.join(["%dch " % len(p) for p in phonemes])
     styleString = "grid-template-columns: %s;" % ''.join(["%dch " % p for p in self.phonemeSpacing])
     with htmlDoc.tag("div", klass="phoneme-tier", style=styleString):
        for phoneme in phonemes:
          with htmlDoc.tag("div", klass="phoneme-cell"):
             htmlDoc.text(phoneme)

   #----------------------------------------------------------------------------------------------------
   def tokenizedGlossesToHtml(self, htmlDoc, tierNumber):

     tierObj = self.getTable().ix[tierNumber].to_dict()
     phonemeGlosses = tierObj['TEXT'].split("\t")

     #styleString = "grid-template-columns: %s;" % ''.join(["%dch " % len(p) for p in phonemeGlosses])
     styleString = "grid-template-columns: %s;" % ''.join(["%dch " % p for p in self.phonemeSpacing])
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

      print("toHtml, nothing here yet")

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
     if(elementText is None):
        elementText = ""
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
   textLengths = [len(t) for t in tbl["TEXT"].tolist()]
   tbl["TEXT_LENGTH"] = textLengths
   hasTabs = ["\t" in t for t in tbl["TEXT"].tolist()]
   tbl["HAS_TABS"] = hasTabs
   hasSpaces = [" " in t for t in tbl["TEXT"].tolist()]
   tbl["HAS_SPACES"] = hasSpaces

   return(tbl)

#------------------------------------------------------------------------------------------------------------------------

#filename0 = "../testData/daylight77a.eaf"
#filename1 = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
#doc1 = etree.parse(filename0)
#doc2 = etree.parse(filename1)
#doc = doc2



