import re
import sys
import os
import unittest
from line import *
from canonicalLine import *
from degenerateLine import *
from lineClassifier import *
import importlib
pd.set_option('display.width', 1000)
import pdb

filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
audioDirectory = "monkeyTest"
xmlDoc = etree.parse(filename)
lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
assert(lineCount == 41)

htmlDoc = Doc()

htmlDoc.asis('<!DOCTYPE html>')

with htmlDoc.tag('html', lang="en"):
     with htmlDoc.tag('head'):
         htmlDoc.asis('<meta charset="UTF-8">')
         htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
         htmlDoc.asis('<script src="ijalUtils.js"></script>')
         with htmlDoc.tag('body'):
             for i in range(lineCount):
                 x = Line(xmlDoc, i)
                 with htmlDoc.tag("div",  klass="line-wrapper"):
                     tbl = x.getTable()
                     lineID = tbl.ix[0]['ANNOTATION_ID']
                     classifier = LineClassifier(tbl)
                     classification = classifier.run()
                     print("%d: %s" % (i, classification))
                     with htmlDoc.tag("div", klass="line-sidebar"):
                         lineLeadIn(htmlDoc, i, lineID, audioDirectory)
                     if(classification == "CanonicalLine"):
                         xc = CanonicalLine(xmlDoc, i)
                         xc.toHtml(htmlDoc)
                     elif(classification == "DegenerateLine"):
                         xd = DegenerateLine(xmlDoc, i)
                         xd.toHtml(htmlDoc)


htmlText = htmlDoc.getvalue()

filename = "monkeyAndThunder2.html"
f = open(filename, "w")
f.write(indent(htmlText))
f.close()
os.system("open %s" % filename)
