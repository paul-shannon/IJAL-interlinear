import re
import sys
sys.path.append("..")
from line import *
import importlib
import os
import pdb
#----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)
#----------------------------------------------------------------------------------------------------

def runTests():
    showVariedTables()
    test_extractAudio()

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
