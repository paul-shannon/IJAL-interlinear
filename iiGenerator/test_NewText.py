import sys, os
import unittest
from NewText import *
#----------------------------------------------------------------------------------------------------
#filename = "../testData/daylight77a.eaf"
#filename = "../testData/daylight_1_4.eaf"
#filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
#----------------------------------------------------------------------------------------------------
def runTests():

   test_daylight_0()


#----------------------------------------------------------------------------------------------------
def test_daylight_0():

    print("--- test_daylight_0")
    text = NewText("../testData/daylight77a.eaf", "daylight77a.html")
    text.toHtml()

#----------------------------------------------------------------------------------------------------
def test_daylight_1_4():

   print("--- test_daylight_1_4")
   filename = "../testData/daylight_1_4.eaf"
   text = NewText(filename, "daylight_1_4.html")
   text.toHtml()
   os.system("open daylight_1_4.html")

#----------------------------------------------------------------------------------------------------
