import sys
from Text import *
#----------------------------------------------------------------------------------------------------
def runTests():

   test_daylight()

#----------------------------------------------------------------------------------------------------
def test_daylight():

   print("--- test_daylight")
   filename = "../testData/daylight77a.eaf"
   text = Text(filename)

#----------------------------------------------------------------------------------------------------
def test_monkeyAndThunder():

   print("--- test_monkeyAndThunder")
   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   text = Text(filename)

#----------------------------------------------------------------------------------------------------
#if __name__ == '__main__':
#   runTests()

filename0 = "../testData/daylight77a.eaf"
filename1 = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
text1 = Text(filename1)
text1.show()





