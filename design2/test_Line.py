import re
import sys
import unittest
from Line import *
import importlib
import os
pd.set_option('display.width', 1000)


def runTests():
    showVariedTables()

def showVariedTables():

    filename = "../testData/LOKONO_IJAL_2.eaf"
    doc = etree.parse(filename)
    x3 = Line(doc, 3)
    print(x3.getTable())

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    doc = etree.parse(filename)
    x0 = Line(doc, 0)
    print(x0.getTable())

    x6 = Line(doc, 6)
    print(x6.getTable())

    filename = "../testData/daylight_1_4.eaf"
    doc = etree.parse(filename)
    x1 = Line(doc, 1)
    print(x1.getTable())

def test_extractAudio():

    print("--- test_extractAudio")
    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    xmlDoc = etree.parse(filename)
    soundFileElement = xmlDoc.findall("HEADER/MEDIA_DESCRIPTOR")[0]
    attributes = list(soundFileElement.attrib.keys())
    assert("RELATIVE_MEDIA_URL" in attributes))
    soundFileURI = soundFileElement[0].attrib["RELATIVE_MEDIA_URL"]
    directory = os.path.dirname(os.path.abspath(filename))
    fullPath = os.path.join(directory, soundFileURI)
    assert(os.path.exists(fullPath))


