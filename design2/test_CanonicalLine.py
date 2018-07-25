import re
import sys
import unittest
from line import *
from canonicalLine import *
from lineClassifier import *
import importlib
pd.set_option('display.width', 1000)

def runTests():
    test_constructor()
    test_toHTML()

def test_constructor():

    """
      MonkeyAndThunder starts off with a few introductory lines in Spanish, with English translation.
      At and after line 6, canonical lines are found until another degenerate lines is found at the end
      of the story.
    """
    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    xmlDoc = etree.parse(filename)
    x = CanonicalLine(xmlDoc, 6)
    assert(x.getTierCount() == 4)
    assert(x.spokenTextRow == 0)
    assert(x.freeTranslationRow == 2)
    assert(x.wordRow == 1)
    assert(x.glossRow == 3)
    assert(x.words == ['que', 'heM', 'mak=put', 'mak=nǝh', 'meʔ', 'ʔiː', 'mak=ŋ•weh', 'mas'])
    assert(x.glosses == ['that', 'there', 'CMP=exit', 'CMP=go', 'DIST', 'who', 'CMP=MOUTH•cry', 'more'])
    assert(x.wordSpacing == [5, 6, 9, 8, 5, 4, 14, 5])
    #print(x.getTable())


def test_toHTML(displayPage=False):
    """
      create a barebones webpage, and htmlDoc, then render a DegenerateLine into it
    """
    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    xmlDoc = etree.parse(filename)
    x0 = CanonicalLine(xmlDoc, 6)

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                x0.toHtml(htmlDoc)

    htmlText = htmlDoc.getvalue()

    assert(htmlText.find("jejn") == 136)
    assert(htmlText.find("que") == 302)
    assert(htmlText.find("MOUTH") == 920)
    assert(htmlText.find("louder") == 1065)

    if(displayPage):
        f = open("canonicalLine.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "canonicalLine.html")


def readAll():

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
    assert(lineCount == 41)
    for i in range(lineCount):
       x = Line(xmlDoc, i)
       classifier = LineClassifier(x.getTable())
       classification = classifier.run()
       print("%d: %s" % (i, classification))
       if(classification == "CanonicalLine"):
           xc = CanonicalLine(xmlDoc, i)

def allToHTML():

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
    assert(lineCount == 41)

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                for i in range(lineCount):
                    x = Line(xmlDoc, i)
                    classifier = LineClassifier(x.getTable())
                    classification = classifier.run()
                    print("%d: %s" % (i, classification))
                    if(classification == "CanonicalLine"):
                        xc = CanonicalLine(xmlDoc, i)
                        xc.toHtml(htmlDoc)
                        htmlDoc.asis("<p><hr><p>")

    htmlText = htmlDoc.getvalue()

    if(displayPage):
        filename = "monkeyAndThunder-canonical.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)



