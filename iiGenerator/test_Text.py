import sys
from Text import *
#----------------------------------------------------------------------------------------------------
def runTests():

   test_constructor()

#----------------------------------------------------------------------------------------------------
def test_constructor():

   print("--- test_constructor for Text class")
   filename0 = "../testData/daylight77a.eaf"
   filename1 = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   text = Text(filename1)

#----------------------------------------------------------------------------------------------------
#if __name__ == '__main__':
#   runTests()

filename0 = "../testData/daylight77a.eaf"
filename1 = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
text1 = Text(filename1)
text1.show()





