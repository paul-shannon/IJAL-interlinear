import sys
import unittest
from Line import *
#----------------------------------------------------------------------------------------------------
def runTests():

   test_daylight_0()
   test_monkey_0()
   test_monkey_all()
   test_classifyTier()
   test_spokenTextToHtml()
   test_tokenizedPhonemesToHtml()
   test_freeTranslationToHtml()
   test_toHTML()

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
     lineText = line.getSpokenText()
     assert(len(lineText) >= 10)   # empirically derived.  lines have betwee 10 and 61 characters
     assert(len(lineText) < 100)   # empirically derived.  lines have betwee 10 and 61 characters
     if(verbose):
        print("%2d) %s" % (i, lineText))

#----------------------------------------------------------------------------------------------------
# ijal eaf lines have tiers of six types, of which all but the first seem to be optional
#   1) default-lt.  "default linguistic type" - this contains the spoken TEXT, and non-null start and stop times
#   2) phonenmic.  optional. the TEXT field is tab-delimited
#   3) translation/to.language.
#   4) translation: phonemic GL(oss)
def test_classifyTier():

   print("--- test_classifyTier")

     # test the usual case: 4 tiers, each with content
   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc = etree.parse(filename)
   line6 = Line(doc, 6)   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
   tierCount = line6.getTable().shape[0]
   assert(tierCount == 4)
   assert(line6.classifyTier(0) == "spokenText")
   assert(line6.classifyTier(1) == "tokenizedPhonemes")
   assert(line6.classifyTier(2) == "freeTranslation")
   assert(line6.classifyTier(3) == "tokenizedPhonemesTranslated")

       # now try a degenerate case, from one of the Spanish-only introductory lines
   line0 = Line(doc, 0)
   tierCount = line0.getTable().shape[0]
   assert(tierCount == 4)
   assert(line0.classifyTier(0) == "spokenText")
   assert(line0.classifyTier(1) == "unrecognized")
   assert(line0.classifyTier(2) == "freeTranslation")
   assert(line0.classifyTier(3) == "unrecognized")

#----------------------------------------------------------------------------------------------------
def test_spokenTextToHtml():

   print("--- test_spokenTextToHtml")

     # test the usual case: 4 tiers, each with content
   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc = etree.parse(filename)
   line6 = Line(doc, 6)   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
   tierCount = line6.getTable().shape[0]
   assert(tierCount == 4)
   assert(line6.classifyTier(0) == "spokenText")
   html = line6.spokenTextToHtml(0)
   assert(html.find("playAnnotation(28417, 35221)") > 300)
   assert(html.find("<i>Ke jejn makput. Makndüj mbeʹ ii maknhwej maj.</i>") > 440)
   assert(html[0:4] == '<tr ')
   assert(html[len(html)-5:len(html)] == '</tr>')

#----------------------------------------------------------------------------------------------------
def test_tokenizedPhonemesToHtml():

   print("--- test_tokenizedPhonemesToHtml")

     # test the usual case: 4 tiers, each with content
   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc = etree.parse(filename)
   line6 = Line(doc, 6)   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
   tierCount = line6.getTable().shape[0]
   assert(tierCount == 4)
   assert(line6.classifyTier(1) == "tokenizedPhonemes")
   html = line6.tokenizedPhonemesToHtml(1)
   assert(html[0:4] == '<tr ')
   assert(html[len(html)-5:len(html)] == '</tr>')
   assert(html.find("<tr class='CuPED–annotation–line CuPED–annotation–tier–2'>") == 0)
   assert(html.count("td>") == 16)   # 8 pairs of <td> ... </td>


#----------------------------------------------------------------------------------------------------
def test_tokenizedPhonemesTranslatedToHtml():

   print("--- test_tokenizedPhonemesTranslatedToHtml")

     # test the usual case: 4 tiers, each with content
   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc = etree.parse(filename)
   line6 = Line(doc, 6)   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
   tierCount = line6.getTable().shape[0]
   assert(tierCount == 4)
   assert(line6.classifyTier(3) == "tokenizedPhonemesTranslated")
   html = line6.tokenizedPhonemesTranslatedToHtml(3)
   assert(html[0:4] == '<tr ')
   assert(html[len(html)-5:len(html)] == '</tr>')
   assert(html.find("<tr class='CuPED–annotation–line CuPED–annotation–tier–3'>") == 0)
   assert(html.count("td>") == 16)   # 8 pairs of <td> ... </td>

#----------------------------------------------------------------------------------------------------
def test_freeTranslationToHtml():

   print("--- test_freeTranslationToHtml")

     # test the usual case: 4 tiers, each with content
   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc = etree.parse(filename)
   line6 = Line(doc, 6)   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
   tierCount = line6.getTable().shape[0]
   assert(tierCount == 4)
   assert(line6.classifyTier(2) == "freeTranslation")
   html = line6.freeTranslationToHtml(3)
   assert(html[0:4] == '<tr ')
   assert(html[len(html)-5:len(html)] == '</tr>')
   assert(html.find('<tr class="CuPED-annotation-line CuPED-annotation-tier-4">') == 0)
   assert(html.count("<td") == 1)
   assert(html.count("</td>") == 1)

#----------------------------------------------------------------------------------------------------
def test_toHTML():

   print("--- test_toHTML")

filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
doc = etree.parse(filename)
lineCount = len(doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
line = Line(doc, 6)
html = line.toHtml()

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
#line0 = Line(doc2, 0)   # in spanish, just two non-empty tiers
#line6 = Line(doc2, 6)   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
# line0 = Line(doc, 0)



