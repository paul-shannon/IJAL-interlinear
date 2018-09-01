# text.py: a class to represent a complete IJAL interlinear text, and to transform its
# represention in ELAN xml (eaf) format, accompanied by audio, into html
#----------------------------------------------------------------------------------------------------
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
#----------------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------------------------------
class Text:

   xmlFilename = ''
   audioPath = ''
   audioPathIsDirectory = False
   grammaticalTerms = []
   xmlDoc = None
   htmlDoc = None
   lineCount = 0

   def __init__(self, xmlFilename, audioPath, audioPathIsDirectory, grammaticalTermsFile):
     self.xmlFilename = xmlFilename
     self.audioPath = audioPath
     self.audioPathIsDirectory = audioPathIsDirectory
     self.grammaticalTermsFile = grammaticalTermsFile
     self

   def validInputs(self):
     assert(os.path.isfile(self.xmlFilename))
     if(self.audioPathIsDirectory):
        assert(os.path.isdir(self.audioPath))
     else:
        assert(os.path.isfile(self.audioPath))
     if(not self.grammaticalTermsFile == None):
        assert(os.path.isfile(self.grammaticalTermsFile))
        self.grammaticalTerms = open(self.grammaticalTermsFile).read().split("\n")
        assert(len(self.grammaticaTerms) > 0)
     return(True)

   def toHTML(self):
     self.xmlDoc = etree.parse(self.xmlFilename)
     self.lineCount = len(self.xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))

     htmlDoc = Doc()

     htmlDoc.asis('<!DOCTYPE html>')
     with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<meta charset="UTF-8">')
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            htmlDoc.asis('<script src="ijalUtils.js"></script>')
            with htmlDoc.tag('body'):
                for i in range(self.lineCount):
                    x = Line(self.xmlDoc, i)
                    with htmlDoc.tag("div",  klass="line-wrapper"):
                        tbl = x.getTable()
                        lineID = tbl.ix[0]['ANNOTATION_ID']
                        classifier = LineClassifier(tbl)
                        classification = classifier.run()
                        print("%3d: %s" % (i, classification))
                        with htmlDoc.tag("div", klass="line-sidebar"):
                            x.htmlLeadIn(htmlDoc, self.audioPath)
                        if(classification == "CanonicalLine"):
                            xc = CanonicalLine(self.xmlDoc, i, self.grammaticalTerms)
                            xc.toHtml(htmlDoc)
                        elif(classification == "DegenerateLine"):
                            xd = DegenerateLine(self.xmlDoc, i)
                            xd.toHtml(htmlDoc)
     self.htmlDoc = htmlDoc
     self.htmlText = htmlDoc.getvalue()
     return(self.htmlText)

