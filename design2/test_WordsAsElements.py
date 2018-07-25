import re
import sys
import unittest
from line import *
from wordsAsElementsLine import *
from lineClassifier import *
import importlib
pd.set_option('display.width', 1000)

def runTests():
    test_constructor()
    test_toHTML()

def test_constructor():

    """
      MonkeyAndThunder starts off with a few introductory lines in Spanish, with English translation.
      At and after line 6, wordsAsElements lines are found until another degenerate lines is found at the end
      of the story.
    """
    filename = "../testData/LOKONO_IJAL_2.eaf"
    xmlDoc = etree.parse(filename)
    x = WordsAsElementsLine(xmlDoc, 0)
    assert(x.getTierCount() == 20)
    assert(x.spokenTextRow == 0)
    assert(x.freeTranslationRow == 1)
    assert(x.words == ['b–aːmɨŋ', '=koba', 'tʰa', 'aba', 'loko', 'hijaro'])
    assert(x.glosses == ['2SG.A–have', '=REM.PST', 'RPRT', 'INDF', 'Lokono', 'woman'])
    assert(x.wordSpacing == [11, 9, 5, 5, 7, 7])


def test_toHTML(displayPage=False):
    """
      create a barebones webpage, and htmlDoc, then render a DegenerateLine into it
    """
    filename = "../testData/LOKONO_IJAL_2.eaf"
    xmlDoc = etree.parse(filename)
    x = WordsAsElementsLine(xmlDoc, 0)

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                x.toHtml(htmlDoc)

    htmlText = htmlDoc.getvalue()

    assert(htmlText.find("jejn") == 136)
    assert(htmlText.find("que") == 302)
    assert(htmlText.find("MOUTH") == 920)
    assert(htmlText.find("louder") == 1065)

    if(displayPage):
        f = open("wordsAsElementsLine.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "wordsAsElementsLine.html")


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
       if(classification == "WordsAsElementsLine"):
           xc = WordsAsElementsLine(xmlDoc, i)

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
                    if(classification == "WordsAsElementsLine"):
                        xc = WordsAsElementsLine(xmlDoc, i)
                        xc.toHtml(htmlDoc)
                        htmlDoc.asis("<p><hr><p>")

    htmlText = htmlDoc.getvalue()

    if(displayPage):
        filename = "monkeyAndThunder-wordsAsElements.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)



