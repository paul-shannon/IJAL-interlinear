from Line import *
from xml.etree import ElementTree as etree

class Text:

   tiers = []
   lines = []

   def __init__(self, filename):
     self.filename = filename
     self.doc = etree.parse(filename)
     self.linguisticTierTypes = self.doc.findall("LINGUISTIC_TYPE")
     self.tiers = self.doc.findall("TIER")
     self.lineCount = len(self.doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
     for i in range(self.lineCount):
        self.lines.append(Line(self.doc, i))
     #timeAlignable = [e.attrib['TIME_ALIGNABLE'] for e in self.linguisticTierTypes]
     #ids = [e.attrib['LINGUISTIC_TYPE_ID'] for e in self.linguisticTierTypes]
     # self.timeAlignedElment = self.doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[self.lineNumber]
     # timeAlignedElementIndices = [i for i in range(len(timeAlignable)) if timeAlignable[i] == 'true']
       # should be just one element that is time aligned
     # assert(len(timeAlignedElementIndices) == 1)
     #timeAlignedID = ids[timeAlignedElementIndices[0]]
        # the aligned element is the nth

   def show(self):
      print("--- %s" % self.filename)
      print("--- %d linguisticTierTypes" % len(self.linguisticTierTypes))
      sink = [print(e.attrib) for e in self.linguisticTierTypes]
      print("--- %d tiers" % len(self.tiers))
      sink = [print(e.attrib) for e in self.tiers]

   def getLine(self, lineNumber):
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

