import re
import sys
import unittest
from Line import *
import importlib
pd.set_option('display.width', 1000)


def runTests():
    showVariedTables()

def showVariedTables():

    filename = "../testData/LOKONO_IJAL_2.eaf"
    doc = etree.parse(filename)
    x3 = Line(doc, 3)
    print(x3.getTable())

    filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    doc = etree.parse(filename)
    x0 = Line(doc, 0)
    print(x0.getTable())

    x6 = Line(doc, 6)
    print(x6.getTable())

    filename = "../testData/daylight_1_4.eaf"
    doc = etree.parse(filename)
    x1 = Line(doc, 1)
    print(x1.getTable())
