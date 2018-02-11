import sys
sys.path.append("../iiGenerator")
from iiGenerator import *

#----------------------------------------------------------------------------------------------------
def runTests():

   test_constructor()

#----------------------------------------------------------------------------------------------------
def test_constructor():

   print("--- test_constructor")
   filename = "../testData/daylight77a.eaf"
   iig = iiGenerator(filename)
      # do some simple sanity checks
   assert(iig.getTimeSlotCount() == 4)
   assert(iig.getTierCount() == 2)
   assert(iig.getLinguisticTypeCount() == 3)
   assert(iig.getTierLinguisticTypesTimeAlignable() == {'default-lt': True, 'phonemic': False, 'translation': False})

   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   iig = iiGenerator(filename)
   assert(iig.getTimeSlotCount() == 82)
   assert(iig.getTierCount() == 4)
   assert(iig.getLinguisticTypeCount() == 3)
   assert(iig.getTierLinguisticTypesTimeAlignable() == {'default-lt': True, 'phonemic': False, 'translation': False})

#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
   runTests()

filename0 = "../testData/daylight77a.eaf"
iig0 = iiGenerator(filename0)

filename1 = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
iig1 = iiGenerator(filename1)



