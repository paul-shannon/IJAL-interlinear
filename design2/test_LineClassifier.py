import re
import sys
import unittest
from Line import *
from LineClassifier import *
import importlib
pd.set_option('display.width', 1000)
import pdb

def runTests():
    test_recognizeDegenerateLine()
    test_recognizeCanonicalLine()
    test_recognizeWordsAsElementsLine()
    test_MonkeyAndThunder_allLinesRecognized()
    test_LOKONO_allLinesRecognized()

def test_recognizeDegenerateLine():

    """
      MonkeyAndThunder starts off with a few introductory lines in Spanish, with English translation.
      No words, no glosses, just a line with time slots, and one child
    """
    print("--- test_recognizeDegenerateLine")

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    xmlDoc = etree.parse(filename)
    x0 = Line(xmlDoc, 0)
    assert(x0.getTierCount() == 2)
    classifier = LineClassifier(x0.getTable())
    assert(classifier.run() == "DegenerateLine")

def test_recognizeCanonicalLine():

    """
      MonkeyAndThunder line 6 fits the canonical form:
        1) a time line
    """

    print("--- test_recognizeCanonicalLine")

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    xmlDoc = etree.parse(filename)
    x = Line(xmlDoc, 6)
    assert(x.getTierCount() == 4)
    classifier = LineClassifier(x.getTable())
    assert(classifier.run() == "CanonicalLine")

def test_recognizeWordsAsElementsLine():

    """
      LOKONO has the canonical spokenText tier, its translation, but each word in the
      spokenText is its own element, each with two children: morpheme and gloss
    """

    print("--- test_recognizeWordsAsElementsLine")

    filename = "../testData/LOKONO_IJAL_2.eaf"
    xmlDoc = etree.parse(filename)
    x = Line(xmlDoc, 1)
    # print(x.getTable())
    assert(x.getTierCount() == 20)
    classifier = LineClassifier(x.getTable())
    assert(classifier.run() == "WordsAsElementsLine")

def test_MonkeyAndThunder_allLinesRecognized():

    print("--- test_MonkeyAndThunder_allLinesRecognized")

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
    assert(lineCount == 41)
    for i in range(lineCount):
       x = Line(xmlDoc, i)
       classifier = LineClassifier(x.getTable())
       classification = classifier.run()
       #print("%d: %s" % (i, classification))
       assert(classification in ["DegenerateLine", "CanonicalLine"])

def test_LOKONO_allLinesRecognized():

    print("--- test_LOKONO_allLinesRecognized")

    filename = "../testData/LOKONO_IJAL_2.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
    assert(lineCount == 344)
    for i in range(lineCount):
       x = Line(xmlDoc, i)
       classifier = LineClassifier(x.getTable())
       classification = classifier.run()
       #print("%d: %s" % (i, classification))
       assert(classification in ["WordsAsElementsLine"])


#x = Line(xmlDoc, 28)
#x.getTable()

