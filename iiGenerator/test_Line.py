import sys
import unittest
from Line import *
#----------------------------------------------------------------------------------------------------
def runTests():

   test_daylight_0()
   test_monkey_0()
   test_monkey_all()
   #test_getHTML()

#----------------------------------------------------------------------------------------------------
def test_daylight_0():

   print("--- test_daylight_0")
   filename = "../testData/daylight77a.eaf"
   doc = etree.parse(filename)
   line0 = Line(doc, 0)
   tbl = line0.getTable()
   tierTypes = list(tbl.ix[:, "LINGUISTIC_TYPE_REF"])
   assert(tierTypes== ['default-lt', 'translation'])
   assert(tbl.shape == (2, 10))
   assert(list(tbl.ix[0, ["ANNOTATION_ID", "START", "END", "TEXT"]]) ==['a1', 0.0, 768.0, 'dil tu'])
   assert(list(tbl.ix[1, ["ANNOTATION_ID", "TEXT"]]) == ['a332', 'focal'])
   assert(tbl.ix[0, "ANNOTATION_ID"] == tbl.ix[1, "ANNOTATION_REF"])

#----------------------------------------------------------------------------------------------------
def test_monkey_0():

   print("--- test_monkey_0")
   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc = etree.parse(filename)

   line0 = Line(doc, 0)
   tbl = line0.getTable()
   assert(tbl.shape == (4, 10))
   #assert(tbl.ix[0, ["ANNOTATION_ID", "LINGUISTIC_TYPE_REF", "START", "END", "TEXT"]])
   row0_actual =  list(tbl.ix[0, ["ANNOTATION_ID", "LINGUISTIC_TYPE_REF", "START", "END", "TEXT"]])
   row0_expected = ['a1', 'default-lt', 388.0, 8895.0, 'Por ejemplo el, como se llama, el mono,']
   assert(row0_actual == row0_expected)
   assert(list(tbl.ix[:, "LINGUISTIC_TYPE_REF"]) == ["default-lt", "phonemic", "translation", "translation"])

#----------------------------------------------------------------------------------------------------
def test_monkey_all(verbose=False):

   print("--- test_monkey_all")

   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc = etree.parse(filename)
   lineCount = len(doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
   assert(lineCount == 41)
   for i in range(lineCount):
     line = Line(doc, i)
     tbl = line.getTable()
     tierTypes = list(tbl.ix[:, "LINGUISTIC_TYPE_REF"])
     assert(tierTypes == ['default-lt', 'phonemic', 'translation', 'translation'])
     lineText = line.getOriginalText()
     assert(len(lineText) >= 10)   # empirically derived.  lines have betwee 10 and 61 characters
     assert(len(lineText) < 100)   # empirically derived.  lines have betwee 10 and 61 characters
     if(verbose):
        print("%2d) %s" % (i, lineText))

#----------------------------------------------------------------------------------------------------
def test_getHTML():

   print("--- test_monkey_all")

   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc = etree.parse(filename)
   lineCount = len(doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
   line = Line(doc, 0)
   lineText = line.getOriginalText()
   print("%2d) %s" % (0, lineText))
   lineHtml = line.getHtml()
   print("%2d) %s" % (0, lineHtml))

#----------------------------------------------------------------------------------------------------
# david beck email (28 jan 2018)
#
#  create HTML for up to six lines (e.g., a line in a practical
#  orthography, a line in phonetic transcription, a parsing line, a
#  glossing line, a free translation in Language 1, and a free
#  transltion in Language 2). The parsing line and glossing line have
#  some other constraints on them (the annotations on these two lines
#  have to match perfectly and exhaustively).
#
#  suggesting these tier types:
#    1) text
#    2) phonemes
#    3) parsing
#    4) glossing
#    5) free translation language 1
#    6) free translation language 2
#
#  this functions's first job is to idenitfy the tier type, using iformal rules
def tierToHtml(tier):

  keys = list(tier.keys())
  assert(keys==['ANNOTATION_ID', 'LINGUISTIC_TYPE_REF', 'START', 'END', 'TEXT', 'ANNOTATION_REF',
                'TIME_SLOT_REF1', 'TIME_SLOT_REF2', 'PARENT_REF', 'TIER_ID'])

     # 4 types thus far: 0     default-lt, phonemic, translation, translation
     # are there any tiers with divided text, recognized by tabs and a parent/child
     # relationship, childTier.ANNOTATION_REF = parentTier.ANNOTATION_ID

  tierRefType = tier['LINGUISTIC_TYPE_REF']
  startTime = tier['START']
  rawText = tier['TEXT']
  hasSeparatedWords = rawText.find("\t") >= 0

  tierType = "unknown"
  if(tierRefType == "default-lt" and startTime >= 0):
     tierType = "text"
  #elseif(tierRefType == "phonemic" and hasSeparatedWords):
  #   tierType = "phonemes"
  #elseif(tierTypeRef == "

#----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 500)

if __name__ == '__main__':
   runTests()

#filename0 = "../testData/daylight77a.eaf"
#filename1 = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
#doc1 = etree.parse(filename0)
#doc2 = etree.parse(filename1)
#line0 = Line(doc2, 0)
# line0 = Line(doc, 0)



