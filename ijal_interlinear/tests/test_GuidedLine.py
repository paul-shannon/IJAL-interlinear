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
    test_lokono_line_3()
    test_extractAudio()
    test_toHTML()

#----------------------------------------------------------------------------------------------------
def test_buildTable():

    print("--- test_buildTable")

    filename = "../testData/lokono/LOKONO_IJAL_2.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testData/lokono/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
       tierGuide = yaml.load(f)

    x3 = GuidedLine(doc, 3, tierGuide)
    tbl = x3.getTable()
    assert(tbl.shape == (10,14))
    assert(tbl.columns.tolist() == ['ANNOTATION_ID', 'LINGUISTIC_TYPE_REF', 'START', 'END',
                                    'TEXT', 'ANNOTATION_REF', 'TIME_SLOT_REF1', 'TIME_SLOT_REF2',
                                    'PARENT_REF', 'TIER_ID', 'TEXT_LENGTH', 'HAS_TABS', 'HAS_SPACES',
                                    'category'])

    assert(tbl['category'].tolist() == ['speech', 'translation', 'morpheme', 'morphemeGloss',
                                        'morpheme', 'morphemeGloss', 'morpheme', 'morphemeGloss',
                                        'morpheme', 'morphemeGloss'])

    assert(tbl['ANNOTATION_ID'].tolist() == ['a26', 'a969', 'a20533', 'a22390', 'a20534', 'a22391',
                                             'a20535', 'a22392', 'a20536', 'a22393'])

    assert(tbl['TIER_ID'].tolist() == ['Orthographic represntation', 'English translation', 'morpheme', 'gloss',
                                        'morpheme', 'gloss', 'morpheme', 'gloss', 'morpheme', 'gloss'])

        # first element is empty, confusingly parsed out of xml as math.nan.  don't test for it - too peculiar
    assert(tbl['ANNOTATION_REF'].tolist()[1:] == ['a26', 'a12134', 'a12134', 'a12135', 'a12135', 'a12136',
                                                   'a12136', 'a12137', 'a12137'])

#----------------------------------------------------------------------------------------------------
def test_lokono_line_3():

    """
      used for early exploration and development of the GuidedLine class
    """
    print("--- test_lokono_line_3")

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

    assert(x3.getSpokenText() == 'thusa, aba hiyaro kiba.')
    assert(x3.getTranslation() == "‘[a] child, a woman as well.'")
    assert(x3.getMorphemes() == ['tʰ–ɨsa', 'aba', 'hijaro', 'kiba'])
    assert(x3.getMorphemeGlosses() == ['3FEM.POSS–child', 'INDF', 'woman', 'too'])
    assert(x3.getMorphemeSpacing() == [16, 5, 7, 5])

#----------------------------------------------------------------------------------------------------
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

#----------------------------------------------------------------------------------------------------
def test_toHTML(displayPage=False):

    print("--- test_toHTML")

    filename = "../testData/lokono/LOKONO_IJAL_2.eaf"
    xmlDoc = etree.parse(filename)
    tierGuideFile = "../testData/lokono/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
       tierGuide = yaml.load(f)

    x3 = GuidedLine(xmlDoc, 3, tierGuide)

    htmlDoc = Doc()
    x3.toHTML(htmlDoc)
    htmlText = htmlDoc.getvalue()
    assert(htmlText.find(x3.getSpokenText()) > 0)
    assert(htmlText.find(x3.getTranslation()) > 0)

    if(displayPage):
       filename = "tmp.html"
       f = open(filename, "w")
       f.write(indent(htmlText))
       f.close()
       os.system("open %s" % filename)


#----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    runTests()
