import re
import sys
import unittest
from line import *
from canonicalLine import *
from degenerateLine import *
from lineClassifier import *
import importlib
pd.set_option('display.width', 1000)


filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
xmlDoc = etree.parse(filename)
lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
assert(lineCount == 41)

htmlDoc = Doc()

htmlDoc.asis('<!DOCTYPE html>')
with htmlDoc.tag('html', lang="en"):
     with htmlDoc.tag('head'):
         htmlDoc.asis('<meta charset="UTF-8">')
         htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
         with htmlDoc.tag('body'):
             for i in range(lineCount):
                 x = Line(xmlDoc, i)
                 with htmlDoc.tag("div",  klass="line-wrapper"):
                     with htmlDoc.tag("div", klass="line-sidebar"):
                         htmlDoc.text("%d)" % (i + 1))
                         htmlDoc.asis('<img src="https://www.americanlinguistics.org/wp-content/uploads/speaker.png"></img>')
                     classifier = LineClassifier(x.getTable())
                     classification = classifier.run()
                     print("%d: %s" % (i, classification))
                     if(classification == "CanonicalLine"):
                         xc = CanonicalLine(xmlDoc, i)
                         xc.toHtml(htmlDoc)
                     elif(classification == "DegenerateLine"):
                         xd = DegenerateLine(xmlDoc, i)
                         xd.toHtml(htmlDoc)


htmlText = htmlDoc.getvalue()

filename = "monkeyAndThunder.html"
f = open(filename, "w")
f.write(indent(htmlText))
f.close()
os.system("open %s" % filename)



