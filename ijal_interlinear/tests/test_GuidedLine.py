import re
import sys
sys.path.append("..")
from guidedLine import *
import importlib
import os
import pdb
import guidedLine
import yaml
#----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)
#----------------------------------------------------------------------------------------------------

def runTests():
    test_buildTable()
    showVariedTables()
    test_extractAudio()

def test_sampleLine():

    print("--- test_sampleLine")

    filename = "../testData/lokono/LOKONO_IJAL_2.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testData/lokono/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
       tierGuide = yaml.load(f)

    x3 = GuidedLine(doc, 3, tierGuide)
    assert(x3.speechRow == 0)
    assert(x3.translationRow == 1)
    assert(x3.morphemeRows == [2, 4, 6, 8])
    assert(x3.morphemeGlossRows == [3, 5, 7, 9])

def test_buildTable():

    print("--- test_buildTable")

    filename = "../testData/lokono/LOKONO_IJAL_2.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testData/lokono/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
       tierGuide = yaml.load(f)

    x3 = Line(doc, 3, tierGuide)
    tbl = x3.getTable()
    assert(tbl.shape == (14,13))
    assert(tbl['ANNOTATION_ID'].tolist() == ['a26', 'a969', 'a12134', 'a12135', 'a12136', 'a12137', 'a20533',
                                             'a22390', 'a20534', 'a22391', 'a20535', 'a22392', 'a20536', 'a22393'])
    assert(tbl['TIER_ID'].tolist() == ['Orthographic represntation', 'English translation', 'Word division-cp',
                                       'Word division-cp', 'Word division-cp', 'Word division-cp', 'morpheme',
                                       'gloss', 'morpheme', 'gloss', 'morpheme', 'gloss', 'morpheme', 'gloss'])
        # first element is empty, confusingly parsed out of xml as math.nan.  don't test for it - too peculiar
    assert(tbl['ANNOTATION_REF'].tolist()[1:] == ['a26', 'a26', 'a26', 'a26', 'a26', 'a12134', 'a12134',
                                              'a12135', 'a12135', 'a12136', 'a12136', 'a12137', 'a12137'])

def test_stamdardizeTable():

    xmlFilename = "../testData/lokono/LOKONO_IJAL_2.eaf"
    tierGuideFile = "../testData/lokono/tierGuide.yaml"
    doc = etree.parse(filename)
    x3 = Line(doc, 3)
    tbl = x3.getTable()
    with open(tierGuideFile, 'r') as f:
       tierGuide = yaml.load(f)

    tbl2 = standardizeTable(tbl, tierGuide)


def showVariedTables():

    filename = "../testData/lokono/LOKONO_IJAL_2.eaf"
    doc = etree.parse(filename)
    x3 = Line(doc, 3)
    print(x3.getTable())

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    doc = etree.parse(filename)
    x0 = Line(doc, 0)
    print(x0.getTable())

    x6 = Line(doc, 6)
    print(x6.getTable())

    filename = "../testData/harryMosesDaylight/daylight_1_4.eaf"
    doc = etree.parse(filename)
    x1 = Line(doc, 1)
    print(x1.getTable())

def test_extractAudio():

    print("--- test_extractAudio")
    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    assert(os.path.exists(filename))
    xmlDoc = etree.parse(filename)
    mediaDescriptors = xmlDoc.findall("HEADER/MEDIA_DESCRIPTOR")
    assert(len(mediaDescriptors) == 1)
    soundFileElement = mediaDescriptors[0]
    soundFileURI = soundFileElement.attrib["RELATIVE_MEDIA_URL"]
    directory = os.path.dirname(os.path.abspath(filename))
    fullPath = os.path.join(directory, soundFileURI)
    assert(os.path.exists(fullPath))

if __name__ == '__main__':
    runTests()
