import sys, re
import unittest
from Line import *
#----------------------------------------------------------------------------------------------------
def runTests():

   test_daylight_0()
   test_daylight_1_4()
   test_monkey_0()
   test_monkey_all()
   test_classifyTier()
   test_spokenTextToHtml()
   test_tokenizedWordsToHtml()
   test_tokenizedGlossesToHtml()
   test_freeTranslationToHtml()
   #test_toHTML()

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
def test_daylight_1_4():

   print("--- test_daylight_1_4")
   filename = "../testData/daylight_1_4.eaf"
   doc = etree.parse(filename)
   line0 = Line(doc, 0)
   tbl = line0.getTable()
   tierTypes = list(tbl.ix[:, "LINGUISTIC_TYPE_REF"])
   assert(tierTypes== ['default-lt', 'phonemic', 'translation', 'translation'])
   assert(tbl.shape == (4, 10))
   #assert(list(tbl.ix[0, ["ANNOTATION_ID", "START", "END", "TEXT"]]) ==['a1', 0.0, 768.0, 'dil tu'])
   #assert(list(tbl.ix[1, ["ANNOTATION_ID", "TEXT"]]) == ['a332', 'focal'])
   #assert(tbl.ix[0, "ANNOTATION_ID"] == tbl.ix[1, "ANNOTATION_REF"])

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
def test_lokono_all(verbose=False):

   print("--- test_lokono_all")

filename = "../testData/LOKONO_IJAL_2.eaf"
doc = etree.parse(filename)
lineCount = len(doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
assert(lineCount == 344)
#for i in range(lineCount):
for i in range(0):
   line = Line(doc, i)
   tbl = line.getTable()
   tierTypes = list(tbl.ix[:, "LINGUISTIC_TYPE_REF"])
   print(tierTypes)
   #assert(tierTypes == ['default-lt', 'phonemic', 'translation', 'translation'])
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
   assert(line6.classifyTier(1) == "tokenizedWords")
   assert(line6.classifyTier(2) == "freeTranslation")
   assert(line6.classifyTier(3) == "tokenizedGlosses")

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
   htmlDoc = Doc()
   line6.spokenTextToHtml(htmlDoc, 0, 99)
   assert(htmlDoc.getvalue() == '<div class="speech-tier">Ke jejn makput. Makndüj mbeʹ ii maknhwej maj.</div>')

#----------------------------------------------------------------------------------------------------
def test_tokenizedWordsToHtml():

   print("--- test_tokenizedWordsToHtml")

     # test the usual case: 4 tiers, each with content
   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc = etree.parse(filename)
   line6 = Line(doc, 6)   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
   phonemes = line6.getTable().ix[1].to_dict()['TEXT'].split("\t")
   assert(phonemes == ['que', 'heM', 'mak=put', 'mak=nǝh', 'meʔ', 'ʔiː', 'mak=ŋ•weh', 'mas'])
   tierCount = line6.getTable().shape[0]
   assert(tierCount == 4)
   assert(line6.classifyTier(1) == "tokenizedWords")
   htmlDoc = Doc()
   line6.tokenizedWordsToHtml(htmlDoc, 1)
   htmlText = htmlDoc.getvalue()
   assert(len(re.findall('<div class="phoneme-tier" style="grid-template-columns: 3ch 3ch 7ch 7ch 3ch 3ch 9ch 3ch ;">', htmlText)) == 1)
   assert(len(re.findall('div class="phoneme-cell">', htmlText)) == 8)

#----------------------------------------------------------------------------------------------------
def test_tokenizedGlossesToHtml():

   print("--- test_tokenizedGlossesToHtml")

     # test the usual case: 4 tiers, each with content
   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc = etree.parse(filename)
   line6 = Line(doc, 6)   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
   phonemeGlosses = line6.getTable().ix[3].to_dict()['TEXT'].split("\t")
   assert(phonemeGlosses == ['that', 'there', 'CMP=exit', 'CMP=go', 'DIST', 'who', 'CMP=MOUTH•cry', 'more'])
   tierCount = line6.getTable().shape[0]
   assert(tierCount == 4)
   assert(line6.classifyTier(3) == "tokenizedGlosses")
   htmlDoc = Doc()
   line6.tokenizedGlossesToHtml(htmlDoc, 3)
   htmlText = htmlDoc.getvalue()
   assert(len(re.findall('<div class="phoneme-tier" style="grid-template-columns: 4ch 5ch 8ch 6ch 4ch 3ch 13ch 4ch ;">', htmlText)) == 1)
   assert(len(re.findall('div class="phoneme-cell">', htmlText)) == 8)

#----------------------------------------------------------------------------------------------------
def test_freeTranslationToHtml():

   print("--- test_freeTranslationToHtml")

     # test the usual case: 4 tiers, each with content
   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc = etree.parse(filename)
   line6 = Line(doc, 6)   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
   freeText = line6.getTable().ix[2].to_dict()['TEXT']
   assert(freeText == '‘He left. He went looking for someone who could shout louder.’')
   tierCount = line6.getTable().shape[0]
   assert(tierCount == 4)
   assert(line6.classifyTier(2) == "freeTranslation")
   htmlDoc = Doc()
   line6.freeTranslationToHtml(htmlDoc, 2)
   assert(htmlDoc.getvalue() == '<div class="speech-tier">‘He left. He went looking for someone who could shout louder.’</div>')

#----------------------------------------------------------------------------------------------------
def test_toHTML():

   print("--- test_toHTML")

   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc = etree.parse(filename)
   lineCount = len(doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
   line = Line(doc, 6)
   html = line.toHtml()

#----------------------------------------------------------------------------------------------------
def test_toHTML_daylight():

   print("--- test_toHTML_daylight")
   filename = "../testData/daylight_1_4.eaf"
   doc = etree.parse(filename)
   lineCount = len(doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))

   htmlDoc = Doc()

   htmlDoc.asis('<!DOCTYPE html>')
   with htmlDoc.tag('html', lang="en"):
      with htmlDoc.tag('head'):
         htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
      with htmlDoc.tag('body'):

        for lineNumber in range(lineCount):
           with htmlDoc.tag("div",  klass="line-wrapper"):
              with htmlDoc.tag("div", klass="line-sidebar"):
                 htmlDoc.text("%d)" % (lineNumber + 1))
              with htmlDoc.tag("div", klass="line-content"):
                 with htmlDoc.tag("div", klass="line"):
                    line = Line(doc, lineNumber)
                    tierCount = line.getTable().shape[0]
                    for t in range(tierCount):
                       tierType = line.classifyTier(t)
                       print("--- tier %d: %s" % (t, tierType))
                       if(tierType == "spokenText"):
                          line.spokenTextToHtml(htmlDoc, t)
                       if(tierType == "tokenizedWords"):
                          line.tokenizedWordsToHtml(htmlDoc, t)
                       if(tierType == "tokenizedGlosses"):
                          line.tokenizedGlossesToHtml(htmlDoc, t)
                       if(tierType == "freeTranslation"):
                          line.freeTranslationToHtml(htmlDoc, t)

   print(indent(htmlDoc.getvalue()))

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

#if __name__ == '__main__':
#   runTests()

#filename0 = "../testData/daylight77a.eaf"
#filename1 = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
#doc1 = etree.parse(filename0)
#doc2 = etree.parse(filename1)
#line0 = Line(doc2, 0)   # in spanish, just two non-empty tiers
#line6 = Line(doc2, 6)   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
# line0 = Line(doc, 0)



