import re
import sys
import unittest
from line import *
from degenerateLine import *
import importlib
pd.set_option('display.width', 1000)

def runTests():
    test_constructor()
    test_toHTML()

def test_constructor():

    """
      MonkeyAndThunder starts off with a few introductory lines in Spanish, with English translation.
      No words, no glosses, just a line with time slots, and one child element, the free translation
    """
    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    doc = etree.parse(filename)
    x0 = DegenerateLine(doc, 0)
    assert(x0.getTierCount() == 2)
    print(x0.getTable())

def test_toHTML(displayPage=False):
    """
      create a barebones webpage, and htmlDoc, then render a DegenerateLine into it
    """
    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    doc = etree.parse(filename)
    x0 = DegenerateLine(doc, 0)

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                x0.toHtml(htmlDoc)
    htmlText = htmlDoc.getvalue()
    assert(htmlText.find("Por ejemplo") > 100)
    assert(htmlText.find("For example") > 200)
    assert(htmlText.count("line-content") == 1)
    assert(htmlText.count("speech-tier") == 1)
    assert(htmlText.count("freeTranslation-tier") == 1)
      # three divs only: line-content, speech-tier, freeTranslation-tier
    assert(htmlText.count("<div class") == 3)
    if(displayPage):
        f = open("degenerate.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "degenerate.html")
