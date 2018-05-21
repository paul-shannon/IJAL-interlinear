import sys, re
import unittest
from Line import *
from xml.etree import ElementTree as etree
from yattag import *

#------------------------------------------------------------------------------------------------------------------------
class NewText:

    xmlDoc: None
    lines: []
    htmlDoc: None
    inputFilename: None
    outputFilename: None

    def __init__(self, inputFilename, outputFilename):

       self.inputFilename = inputFilename
       self.outputFilename = outputFilename
       self.xmlDoc = etree.parse(inputFilename)
       self.htmlDoc = Doc()
       self.lineCount = len(self.xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))


    def toHtml(self):
       self.htmlDoc.asis('<!DOCTYPE html>')
       with self.htmlDoc.tag('html', lang="en"):
          with self.htmlDoc.tag('head'):
              self.htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
              with self.htmlDoc.tag('body'):

                 for lineNumber in range(self.lineCount):
                    line = Line(self.xmlDoc, lineNumber)
                    with self.htmlDoc.tag("div",  klass="line-wrapper"):
                       with self.htmlDoc.tag("div", klass="line-sidebar"):
                          self.htmlDoc.text("%d)" % (lineNumber + 1))
                          self.htmlDoc.asis('<img src="https://www.americanlinguistics.org/wp-content/uploads/speaker.png"></img>')

                       with self.htmlDoc.tag("div", klass="line-content"):
                          with self.htmlDoc.tag("div", klass="line"):
                             tierCount = line.getTable().shape[0]
                             desiredTierDisplayOrder = [0,1,3,2]
                             for t in desiredTierDisplayOrder: #range(tierCount):
                                tierType = line.classifyTier(t)
                                #print("--- tier %d: %s" % (t, tierType))
                                if(tierType == "spokenText"):
                                   line.spokenTextToHtml(self.htmlDoc, t)
                                if(tierType == "tokenizedWords"):
                                   line.tokenizedWordsToHtml(self.htmlDoc, t)
                                if(tierType == "tokenizedGlosses"):
                                   line.tokenizedGlossesToHtml(self.htmlDoc, t)
                                if(tierType == "freeTranslation"):
                                   line.freeTranslationToHtml(self.htmlDoc, t)

       f = open(self.outputFilename, "w")
       f.write(indent(self.htmlDoc.getvalue()))
       f.close()
