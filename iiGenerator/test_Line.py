import re
import sys
import unittest
from Line import *
import importlib
pd.set_option('display.width', 1000)


def runTests():

    test_spokenTextID()
    test_deduceWordRepresentation()
    test_traverse()
    #test_daylight_0()
    #test_daylight_1_4()
    #test_monkey_0()
    #test_monkey_all()
    #test_classifyTier()
    #test_spokenTextToHtml()
    #test_tokenizedWordsToHtml()
    #test_tokenizedGlossesToHtml()
    #test_freeTranslationToHtml()
    # test_toHTML()

def showVariedTables():

    pd.set_option('display.width', 1000)

    filename = "../testData/LOKONO_IJAL_2.eaf"
    doc = etree.parse(filename)
    x3 = Line(doc, 3)
    print(x3.getTable())

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    doc = etree.parse(filename)
    x6 = Line(doc, 6)
    print(x6.getTable())

    filename = "../testData/daylight_1_4.eaf"
    doc = etree.parse(filename)
    x1 = Line(doc, 1)
    print(x1.getTable())


def test_getTable_from_LOKONO():

    print("--- test_getTable_from_LOKONO")
    pd.set_option('display.width', 1000)
    filename = "../testData/LOKONO_IJAL_2.eaf"
    doc = etree.parse(filename)
    x2 = Line(doc, 3)
    tbl2 = x2.getTable()
    assert(x2.classifyTier(0) == "spokenText")
    assert(x2.classifyTier(1) == "nativeGlossOrFreeTranslation")
    assert(x2.classifyTier(2) == "nativeMorpheme")

def test_getTable_from_MonkeyAndThunder_line_0_spokenText_colonialLanguage():

    print("--- test_getTable_from_MonkeyAndThunder_line_0_spokenText_colonialLanguage")
    pd.set_option('display.width', 1000)
    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    doc = etree.parse(filename)
    lineNumber = 0
    x = Line(doc, lineNumber)
    tbl = x.getTable()
    assert(tbl.shape[0] == 4)
    assert(tbl['TEXT_LENGTH'].tolist() == [39, 0, 50, 0])
    assert(tbl['HAS_TABS'].tolist() == [False, False, False, False])
        # skip the 0th, the root row, which therefore has no backpointer
        # make sure that all the child tiers point back to an reference id
    refIDs = tbl["ANNOTATION_ID"].tolist()
    backPointers = tbl["ANNOTATION_REF"].tolist()[1:4]
    assert([bp in refIDs for bp in backPointers] == [True, True, True])
    assert(x.classifyTier(0) == "spokenText")
    assert(x.classifyTier(1) == "empty")
    assert(x.classifyTier(2) == "freeTranslation")


def test_spokenTextID():

    """ the spokenTextID is the root identifier of each line,
        providing the basis for linking all of the tiers in that line's elements
    """
    print("--- test_deduceSpokenTextID")

    filename = "../testData/LOKONO_IJAL_2.eaf"
    doc = etree.parse(filename)
    lineCount = len(doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
    maxLinesToTest = 10
    if(lineCount < maxLinesToTest):
        max = lineCount
    uniqueIDs = []
    # print("testing %d/%d lines from %s" % (maxLinesToTest, lineCount,filename))
    for lineNumber in range(maxLinesToTest):
        x = Line(doc, lineNumber)
        rootID = x.deduceSpokenTextID()
        uniqueIDs.append(rootID)
    assert(len(uniqueIDs) == maxLinesToTest)

    filename = "../testData/daylight_1_4.eaf"
    doc = etree.parse(filename)
    lineCount = len(doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
    maxLinesToTest = 10
    if(lineCount < maxLinesToTest):
        maxLinesToTest = lineCount
    uniqueIDs = []
    #print("testing %d/%d lines from %s" % (maxLinesToTest, lineCount,filename))

    if(lineCount < maxLinesToTest):
        maxLinesToTest = lineCount
    for lineNumber in range(maxLinesToTest):
        x = Line(doc, lineNumber)
        rootID = x.deduceSpokenTextID()
        assert(rootID not in uniqueIDs)
        uniqueIDs.append(rootID)
        #print("%d: %s" % (lineNumber, rootID))
    assert(len(uniqueIDs) == maxLinesToTest)
    line0 = Line(doc, 0)
    assert(line0.deduceSpokenTextID() == "a1")

    filename = "../testData/daylight77a.eaf"
    doc = etree.parse(filename)
    lineCount = len(doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
    maxLinesToTest = 10
    if(lineCount < maxLinesToTest):
        maxLinesToTest = lineCount
    uniqueIDs = []
    #print("testing %d/%d lines from %s" % (maxLinesToTest, lineCount,filename))
    for lineNumber in range(lineCount):
        x = Line(doc, lineNumber)
        rootID = x.deduceSpokenTextID()
        assert(rootID not in uniqueIDs)
        uniqueIDs.append(rootID)
        #print("%d: %s" % (lineNumber, rootID))
    assert(len(uniqueIDs) == maxLinesToTest)
    line0 = Line(doc, 0)
    assert(line0.deduceSpokenTextID() == "a1")

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    doc = etree.parse(filename)
    lineCount = len(doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
    uniqueIDs = []
    maxLinesToTest = 10
    if(lineCount < maxLinesToTest):
        maxLinesToTest = lineCount
    #print("testing %d/%d lines from %s" % (maxLinesToTest, lineCount,filename))

    for lineNumber in range(maxLinesToTest):
        x = Line(doc, lineNumber)
        rootID = x.deduceSpokenTextID()
        assert(rootID not in uniqueIDs)
        uniqueIDs.append(rootID)
        #print("%d: %s" % (lineNumber, rootID))
    assert(len(uniqueIDs) == maxLinesToTest)
    line0 = Line(doc, 0)
    assert(line0.deduceSpokenTextID() == "a1")

def test_deduceWordRepresentation():

    print("--- test_deduceWordRepresentation")

    filename = "../testData/LOKONO_IJAL_2.eaf"
    doc = etree.parse(filename)
    x3 = Line(doc, 3)
    assert(x3.getWordRepresentation() == "wordsDistributedInElements")

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    doc = etree.parse(filename)
    x6 = Line(doc, 6)
    assert(x6.getWordRepresentation() == "tokenizedWords")

    filename = "../testData/daylight_1_4.eaf"
    doc = etree.parse(filename)
    x1 = Line(doc, 1)
    assert(x1.getWordRepresentation() == "tokenizedWords")

def test_traverse():
    filename = "../testData/LOKONO_IJAL_2.eaf"
    doc = etree.parse(filename)
    x3 = Line(doc, 3)
    print(x3.getTable())
    x3.wordRepresentation
    x3.traverse()
    assert(x3.spokenTextRow == 0)
    assert(x3.freeTranslationRow == 1)

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    doc = etree.parse(filename)
    x1 = Line(doc, 1)
    print(x1.getTable())
    x1.wordRepresentation
    x1.traverse()
    # not working yet.  must accomodate word line which though present is emtpy, 0 characters
    #assert(x1.spokenTextRow == 0)
    #assert(x1.freeTranslationRow == 2)

    x6 = Line(doc, 6)
    print(x6.getTable())
    assert(x6.wordRepresentation == "tokenizedWords")
    x6.traverse()
    assert(x6.spokenTextRow == 0)
    assert(x6.freeTranslationRow == 2)


    filename = "../testData/daylight_1_4.eaf"
    doc = etree.parse(filename)
    x1 = Line(doc, 1)
    print(x1.getTable())
    x1.wordRepresentation
    x1.traverse()
    assert(x1.spokenTextRow == 0)
    assert(x1.freeTranslationRow == 2)


def dev():
    filename = "../testData/LOKONO_IJAL_2.eaf"
    doc = etree.parse(filename)
    line0 = Line(doc, 0)
    tbl = line0.getTable()

    childIDs = tbl.loc[tbl["ANNOTATION_REF"]== "a23", "ANNOTATION_ID"].tolist()
    childText = tbl.loc[tbl["ANNOTATION_REF"]== "a23", "TEXT"].tolist()
    textLength = [len(t) for t in tbl["TEXT"].tolist()]


def test_daylight_0():

    print("--- test_daylight_0")
    filename = "../testData/daylight77a.eaf"
    #filename = "../testData/daylight_1_4.eaf"
    doc = etree.parse(filename)
    line0 = Line(doc, 0)
    tbl = line0.getTable()
    tierTypes = list(tbl.ix[:, "LINGUISTIC_TYPE_REF"])
    assert(tierTypes == ['default-lt', 'phonemic', 'translation', 'translation'])
    assert(tbl.shape == (4, 10))
    assert(list(tbl.ix[0, ["ANNOTATION_ID", "START", "END", "TEXT"]]) == [
           'a1', 0.0, 768.0, 'dil tu'])
    assert(list(tbl.ix[1, ["ANNOTATION_ID", "TEXT"]]) == ['a332', 'focal'])
    assert(tbl.ix[0, "ANNOTATION_ID"] == tbl.ix[1, "ANNOTATION_REF"])

# ----------------------------------------------------------------------------------------------------
def test_daylight_1_4():

   print("--- test_daylight_1_4")
   tbl=line0.getTable()
   tierTypes=list(tbl.ix[:, "LINGUISTIC_TYPE_REF"])
   assert(tierTypes == ['default-lt', 'phonemic',
          'translation', 'translation'])
   assert(tbl.shape == (4, 10))
   # assert(list(tbl.ix[0, ["ANNOTATION_ID", "START", "END", "TEXT"]]) ==['a1', 0.0, 768.0, 'dil tu'])
   # assert(list(tbl.ix[1, ["ANNOTATION_ID", "TEXT"]]) == ['a332', 'focal'])
   # assert(tbl.ix[0, "ANNOTATION_ID"] == tbl.ix[1, "ANNOTATION_REF"])

# ----------------------------------------------------------------------------------------------------
def test_monkey_0():

   print("--- test_monkey_0")
   filename="../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc=etree.parse(filename)

   line0=Line(doc, 0)
   tbl=line0.getTable()
   assert(tbl.shape == (4, 10))
   # assert(tbl.ix[0, ["ANNOTATION_ID", "LINGUISTIC_TYPE_REF", "START", "END", "TEXT"]])
   row0_actual=list(
       tbl.ix[0, ["ANNOTATION_ID", "LINGUISTIC_TYPE_REF", "START", "END", "TEXT"]])
   row0_expected=['a1', 'default-lt', 388.0, 8895.0,
       'Por ejemplo el, como se llama, el mono,']
   assert(row0_actual == row0_expected)
   assert(list(tbl.ix[:, "LINGUISTIC_TYPE_REF"]) == [
          "default-lt", "phonemic", "translation", "translation"])

# ----------------------------------------------------------------------------------------------------
def test_monkey_all(verbose=False):

   print("--- test_monkey_all")

   filename="../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc=etree.parse(filename)
   lineCount=len(doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
   assert(lineCount == 41)
   for i in range(lineCount):
     line=Line(doc, i)
     tbl=line.getTable()
     tierTypes=list(tbl.ix[:, "LINGUISTIC_TYPE_REF"])
     assert(tierTypes == ['default-lt', 'phonemic',
            'translation', 'translation'])
     lineText=line.getSpokenText()
     # empirically derived.  lines have betwee 10 and 61 characters
     assert(len(lineText) >= 10)
     # empirically derived.  lines have betwee 10 and 61 characters
     assert(len(lineText) < 100)
     if(verbose):
        print("%2d) %s" % (i, lineText))

# ----------------------------------------------------------------------------------------------------
def test_lokono_all(verbose=False):

    print("--- test_lokono_all")

    filename="../testData/LOKONO_IJAL_2.eaf"
    doc=etree.parse(filename)
    lineCount=len(doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
    assert(lineCount == 344)
    for i in range(3):
        line=Line(doc, i)
        tbl=line.getTable()
        tierTypes=list(tbl.ix[:, "LINGUISTIC_TYPE_REF"])
        print(tierTypes)
        # assert(tierTypes == ['default-lt', 'phonemic', 'translation', 'translation'])
        lineText=line.getSpokenText()
        # empirically derived.  lines have betwee 10 and 61 characters
        assert(len(lineText) >= 10)
        # empirically derived.  lines have betwee 10 and 61 characters
        assert(len(lineText) < 100)
    if(verbose):
        print("%2d) %s" % (i, lineText))

# ----------------------------------------------------------------------------------------------------
# ijal eaf lines have tiers of six types, of which all but the first seem to be optional
#   1) default-lt.  "default linguistic type" - this contains the spoken TEXT, and non-null start and stop times
#   2) phonenmic.  optional. the TEXT field is tab-delimited
#   3) translation/to.language.
#   4) translation: phonemic GL(oss)
def test_classifyTier():

   print("--- test_classifyTier")

     # test the usual case: 4 tiers, each with content
   filename="../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc=etree.parse(filename)
   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
   line6=Line(doc, 6)
   tierCount=line6.getTable().shape[0]
   assert(tierCount == 4)
   assert(line6.classifyTier(0) == "spokenText")
   assert(line6.classifyTier(1) == "tokenizedWords")
   assert(line6.classifyTier(2) == "freeTranslation")
   assert(line6.classifyTier(3) == "tokenizedGlosses")

       # now try a degenerate case, from one of the Spanish-only introductory lines
   line0=Line(doc, 0)
   tierCount=line0.getTable().shape[0]
   assert(tierCount == 4)
   assert(line0.classifyTier(0) == "spokenText")
   assert(line0.classifyTier(1) == "unrecognized")
   assert(line0.classifyTier(2) == "freeTranslation")
   assert(line0.classifyTier(3) == "unrecognized")

# ----------------------------------------------------------------------------------------------------
def test_spokenTextToHtml():

   print("--- test_spokenTextToHtml")

     # test the usual case: 4 tiers, each with content
   filename="../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc=etree.parse(filename)
   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
   line6=Line(doc, 6)
   tierCount=line6.getTable().shape[0]
   assert(tierCount == 4)
   assert(line6.classifyTier(0) == "spokenText")
   htmlDoc=Doc()
   line6.spokenTextToHtml(htmlDoc, 0, 99)
   assert(htmlDoc.getvalue() ==
          '<div class="speech-tier">Ke jejn makput. Makndüj mbeʹ ii maknhwej maj.</div>')

# ----------------------------------------------------------------------------------------------------
def test_tokenizedWordsToHtml():

   print("--- test_tokenizedWordsToHtml")

     # test the usual case: 4 tiers, each with content
   filename="../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc=etree.parse(filename)
   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
   line6=Line(doc, 6)
   phonemes=line6.getTable().ix[1].to_dict()['TEXT'].split("\t")
   assert(phonemes == ['que', 'heM', 'mak=put',
          'mak=nǝh', 'meʔ', 'ʔiː', 'mak=ŋ•weh', 'mas'])
   tierCount=line6.getTable().shape[0]
   assert(tierCount == 4)
   assert(line6.classifyTier(1) == "tokenizedWords")
   htmlDoc=Doc()
   line6.tokenizedWordsToHtml(htmlDoc, 1)
   htmlText=htmlDoc.getvalue()
   assert(len(re.findall('<div class="phoneme-tier" style="grid-template-columns: 3ch 3ch 7ch 7ch 3ch 3ch 9ch 3ch ;">', htmlText)) == 1)
   assert(len(re.findall('div class="phoneme-cell">', htmlText)) == 8)

# ----------------------------------------------------------------------------------------------------
def test_tokenizedGlossesToHtml():

   print("--- test_tokenizedGlossesToHtml")

     # test the usual case: 4 tiers, each with content
   filename="../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc=etree.parse(filename)
   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
   line6=Line(doc, 6)
   phonemeGlosses=line6.getTable().ix[3].to_dict()['TEXT'].split("\t")
   assert(phonemeGlosses == ['that', 'there', 'CMP=exit',
          'CMP=go', 'DIST', 'who', 'CMP=MOUTH•cry', 'more'])
   tierCount=line6.getTable().shape[0]
   assert(tierCount == 4)
   assert(line6.classifyTier(3) == "tokenizedGlosses")
   htmlDoc=Doc()
   line6.tokenizedGlossesToHtml(htmlDoc, 3)
   htmlText=htmlDoc.getvalue()
   assert(len(re.findall('<div class="phoneme-tier" style="grid-template-columns: 4ch 5ch 8ch 6ch 4ch 3ch 13ch 4ch ;">', htmlText)) == 1)
   assert(len(re.findall('div class="phoneme-cell">', htmlText)) == 8)

# ----------------------------------------------------------------------------------------------------
def test_freeTranslationToHtml():

   print("--- test_freeTranslationToHtml")

     # test the usual case: 4 tiers, each with content
   filename="../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc=etree.parse(filename)
   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
   line6=Line(doc, 6)
   freeText=line6.getTable().ix[2].to_dict()['TEXT']
   assert(freeText == '‘He left. He went looking for someone who could shout louder.’')
   tierCount=line6.getTable().shape[0]
   assert(tierCount == 4)
   assert(line6.classifyTier(2) == "freeTranslation")
   htmlDoc=Doc()
   line6.freeTranslationToHtml(htmlDoc, 2)
   assert(htmlDoc.getvalue() ==
          '<div class="speech-tier">‘He left. He went looking for someone who could shout louder.’</div>')

# ----------------------------------------------------------------------------------------------------
def test_toHTML():

   print("--- test_toHTML")

   filename="../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc=etree.parse(filename)
   lineCount=len(doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
   line=Line(doc, 6)
   html=line.toHtml()

# ----------------------------------------------------------------------------------------------------
def test_toHTML_daylight():

   print("--- test_toHTML_daylight")
   filename="../testData/daylight_1_4.eaf"
   doc=etree.parse(filename)
   lineCount=len(doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))

   htmlDoc=Doc()

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
                    line=Line(doc, lineNumber)
                    tierCount=line.getTable().shape[0]
                    for t in range(tierCount):
                       tierType=line.classifyTier(t)
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

# ----------------------------------------------------------------------------------------------------
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
#    1) text                        (practical orthography)
#    2) phonemes                    (phonemic transcription)
#    3) parsing                     (phoneme by phoneme)
#    4) glossing                    (each phoneme glossed)
#    5) free translation language 1
#    6) free translation language 2
#
#  this functions's first job is to idenitfy the tier type, using informal rules
#
def tierToHtml(tier):

  keys=list(tier.keys())
  assert(keys == ['ANNOTATION_ID', 'LINGUISTIC_TYPE_REF', 'START', 'END', 'TEXT', 'ANNOTATION_REF',
                'TIME_SLOT_REF1', 'TIME_SLOT_REF2', 'PARENT_REF', 'TIER_ID'])

     # 4 types thus far:  default-lt, phonemic, translation, translation
     # are there any tiers with divided text, recognized by tabs and a parent/child
     # relationship, childTier.ANNOTATION_REF = parentTier.ANNOTATION_ID

  tierRefType=tier['LINGUISTIC_TYPE_REF']
  startTime=tier['START']
  rawText=tier['TEXT']
  hasSeparatedWords=rawText.find("\t") >= 0

  tierType="unknown"
  if(tierRefType == "default-lt" and startTime >= 0):
     tierType="text"
  # elseif(tierRefType == "phonemic" and hasSeparatedWords):
  #   tierType = "phonemes"
  # elseif(tierTypeRef == "

# ----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 500)

# if __name__ == '__main__':
#   runTests()

# filename0 = "../testData/daylight77a.eaf"
# filename1 = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
# doc1 = etree.parse(filename0)
# doc2 = etree.parse(filename1)
# line0 = Line(doc2, 0)   # in spanish, just two non-empty tiers
# line6 = Line(doc2, 6)   # in ayapanec, 4 tiers:, default-lt, phonemic with 7 tokens, translation into english, trans by phoneme 7 tokens
# line0 = Line(doc, 0)
