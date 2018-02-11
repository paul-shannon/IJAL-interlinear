import sys
import unittest
from Line import *
#----------------------------------------------------------------------------------------------------
def runTests():

   test_daylight_0()
   test_monkey_0()
   test_monkey_all()

#----------------------------------------------------------------------------------------------------
def test_daylight_0():

   print("--- test_daylight_0")
   filename = "../testData/daylight77a.eaf"
   doc = etree.parse(filename)
   line0 = Line(doc, 0)
   tbl = line0.getTable()
   assert(tbl.shape == (2, 10))
   assert(list(tbl.ix[0, ["ANNOTATION_ID", "START", "END", "TEXT"]]) ==['a1', 0.0, 768.0, 'dil tu'])
   assert(list(tbl.ix[1, ["ANNOTATION_ID", "TEXT"]]) == ['a332', 'focal'])
   assert(tbl.ix[0, "ANNOTATION_ID"] == tbl.ix[1, "ANNOTATION_REF"])

#----------------------------------------------------------------------------------------------------
def test_monkey_0():

   print("--- test_monkey_0")
   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc = etree.parse(filename)

   line0 = Line(doc, 0)
   tbl = line0.getTable()
   assert(tbl.shape == (4, 10))
   #assert(tbl.ix[0, ["ANNOTATION_ID", "LINGUISTIC_TYPE_REF", "START", "END", "TEXT"]])
   row0_actual =  list(tbl.ix[0, ["ANNOTATION_ID", "LINGUISTIC_TYPE_REF", "START", "END", "TEXT"]])
   row0_expected = ['a1', 'default-lt', 388.0, 8895.0, 'Por ejemplo el, como se llama, el mono,']
   assert(row0_actual == row0_expected)
   assert(list(tbl.ix[:, "LINGUISTIC_TYPE_REF"]) == ["default-lt", "phonemic", "translation", "translation"])

#----------------------------------------------------------------------------------------------------
def test_monkey_all():

   print("--- test_monkey_all")

   filename = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   doc = etree.parse(filename)
   lineCount = len(doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
   for i in range(lineCount):
      line = Line(doc, i)
      print("%2d) %s" % (i, line.getTable().ix[0, "TEXT"]))

#----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 500)

if __name__ == '__main__':
   runTests()

filename0 = "../testData/daylight77a.eaf"
filename1 = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
doc1 = etree.parse(filename0)
doc2 = etree.parse(filename1)
#line0 = Line(doc2, 0)

# line0 = Line(doc, 0)



