import re
import sys
import unittest
from Line import *
import importlib
pd.set_option('display.width', 1000)

def runTests():

    test_line_0()

def test_line_0():

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    doc = etree.parse(filename)
    x0 = Line(doc, 0)
    x0.show()
    x0.classifyTier(0)
    x0.classifyTier(1)

    htmlDoc = Doc()
    x0.spokenTextToHtml(htmlDoc)
    assert(htmlDoc.getvalue() ==
           '<div class="speech-tier">Por ejemplo el, como se llama, el mono,</div>')

    htmlDoc = Doc()
    x0.freeTranslationToHtml(htmlDoc)
    html = htmlDoc.getvalue()
    expected = '<div class="freeTranslation-tier">‘For example it, what do you call it, the monkey,’</div>'
    assert(html == expected)


def test_line_6():

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    doc = etree.parse(filename)
    x = Line(doc, 6)
    x.show()
    x.classifyTier(0)
    x.classifyTier(1)
    x.classifyTier(2)
    x.classifyTier(3)

    htmlDoc = Doc()
    x.spokenTextToHtml(htmlDoc)
    html_spokenText = htmlDoc.getvalue()
    expected = '<div class="speech-tier">Ke jejn makput. Makndüj mbeʹ ii maknhwej maj.</div>'
    assert(html_spokenText == expected)

    htmlDoc = Doc()
    x.wordsToHtml(htmlDoc)
    htmlDoc.getvalue()

    htmlDoc = Doc()
    x.glossesToHtml(htmlDoc)
    htmlDoc.getvalue()


def output():

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    xmlDoc = etree.parse(filename)
    htmlDoc = Doc()
    x = Line(xmlDoc, 6)

    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                for lineNumber in range(6,7):
                    line = Line(xmlDoc, lineNumber)
                    with htmlDoc.tag("div",  klass="line-wrapper"):
                        with htmlDoc.tag("div", klass="line-sidebar"):
                            htmlDoc.text("%d)" % (lineNumber + 1))
                            htmlDoc.asis('<img src="https://www.americanlinguistics.org/wp-content/uploads/speaker.png"></img>')

                            with htmlDoc.tag("div", klass="line-content"):
                                with htmlDoc.tag("div", klass="line"):
                                    tierCount = line.getTable().shape[0]
                                    desiredTierDisplayOrder = [0,1,3,2]
                                    for t in desiredTierDisplayOrder: #range(tierCount):
                                        tierType = line.classifyTier(t)
                                        print("--- tier %d: %s" % (t, tierType))
                                        if(tierType == "spokenText"):
                                            line.spokenTextToHtml(htmlDoc)
                                        if(tierType == "nativeMorpheme"):
                                            line.wordsToHtml(htmlDoc)
                                        if(tierType == "nativeGlossOrFreeTranslation"):
                                            line.glossesToHtml(htmlDoc)
                                        if(tierType == "freeTranslation"):
                                            line.freeTranslationToHtml(htmlDoc)

    f = open("monkey.html", "w")
    f.write(indent(htmlDoc.getvalue()))
    f.close()
