import re
import sys
import unittest
from line import *
from degenerateLine import *
import importlib
pd.set_option('display.width', 1000)

def runTests():
    test_constructor()

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

