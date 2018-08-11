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
         htmlDoc.asis('<script src="ijalUtils.js"></script>')
#         htmlDoc.asis('<script>')
#         htmlDoc.asis('function playSample(audioID){console.log(audioID); document.getElementById(audioID).play();}')
#         htmlDoc.asis('</script>')
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
                         htmlDoc.text("%d)" % (i + 1))
                         audioTag = '<audio id="%s"><source src="monkeyTest/%s.wav"/></audio>' % (lineID, lineID)
                         #print(audioTag)
                         htmlDoc.asis(audioTag)
                         buttonTag = '<button onclick="playSample(\'%s\')"><img src="https://www.americanlinguistics.org/wp-content/uploads/speaker.png"/></button>' % lineID
                         #print(buttonTag)
                         htmlDoc.asis(buttonTag)
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
