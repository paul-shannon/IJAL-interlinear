import pandas as pd
from xml.etree import ElementTree as etree
from scipy.io.wavfile import *

def getAudioSpecs(filename):
   xmlDoc = etree.parse(filename)
   timeSlots = xmlDoc.findall("TIME_ORDER/TIME_SLOT")
   startTimes = [int(x.attrib["TIME_VALUE"]) for x in timeSlots]
   soundFileElement = xmlDoc.findall("HEADER/MEDIA_DESCRIPTOR")
   soundFileURI = soundFileElement[0].attrib["RELATIVE_MEDIA_URL"]
   #soundTimeOrigin = soundFileElement[0].attrib["TIME_ORIGIN"]
   print(soundFileURI)
   print(startTimes)

test_getSpecs():
   getAudioSpecs("../testData/daylight_1_4.eaf")
   getAudioSpecs("../testData/LOKONO_IJAL_2.eaf")
   getAudioSpecs("../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf")

def getAllTimes(filename):
   xmlDoc = etree.parse(filename)
   timeSlotElements = xmlDoc.findall("TIME_ORDER/TIME_SLOT")
   audioTiers = xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")
   timeIDs = [x.attrib["TIME_SLOT_ID"] for x in timeSlotElements]
   times = [int(x.attrib["TIME_VALUE"]) for x in timeSlotElements]
   audioIDs = [x.attrib["ANNOTATION_ID"] for x in audioTiers]
   tsRef1 = [x.attrib["TIME_SLOT_REF1"] for x in audioTiers]
   tsRef2 = [x.attrib["TIME_SLOT_REF2"] for x in audioTiers]
   d = {"id": audioIDs, "t1": tsRef1, "t2": tsRef2}
   tbl_t1 = pd.DataFrame({"id": audioIDs, "t1": tsRef1})
   tbl_t2 = pd.DataFrame({"id": audioIDs, "t2": tsRef2})
   tbl_times = pd.DataFrame({"id": timeIDs, "timeValue": times})
   tbl_t1m = pd.merge(tbl_t1, tbl_times, left_on="t1", right_on="id")
   tbl_t2m = pd.merge(tbl_t2, tbl_times, left_on="t2", right_on="id")
   tbl_raw = pd.merge(tbl_t1m, tbl_t2m, on="id_x")
   tbl = tbl_raw.drop(["id_y_x", "id_y_y"], axis=1)
     # still need to rename, maybe also reorder columns
   tbl.columns = ["lineID", "t1", "start", "t2", "end"]
   list(tbl.columns)
   tbl = tbl[["lineID", "start", "end", "t1", "t2"]]
   return(tbl)


def test_getAllTimes():
   filename_xml = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   tbl_times = getAllTimes(filename_xml)
   assert(tbl_times.shape == (41, 5))
   assert(list(tbl_times.columns) == ["lineID", "start", "end", "t1", "t2"])
   (a28_start, a28_end) = tbl_times.loc[tbl_times['lineID'] == 'a28'][['start', 'end']].iloc[0].tolist()
   assert(a28_start == 93905)
   assert(a28_end == 96368)

   filename_audio = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder-32bit.wav"
   xmlDoc = etree.parse(filename_xml)
   timeSlots = xmlDoc.findall("TIME_ORDER/TIME_SLOT")
   startTimes = [int(x.attrib["TIME_VALUE"]) for x in timeSlots]
   rate, mtx = read(filename_audio)
   mtx.shape
   mtx.shape[0]/rate   # 5812410, 2
   samples = mtx.shape[0]
   duration = mtx.shape[0] / rate
   startTime = startTimes[0]/1000
   endTime = startTimes[1]/1000
   startIndex = round(startTime * rate)
   endIndex = round(endTime * rate)
   phrase = mtx[startIndex:endIndex, ]
   phrase.shape
   write('../testData/monkeyAndThunder/audioByPhrase/a1.wav', rate, phrase)


rate, mtx = read("../testData/daylight_1_4.wav")
mtx.shape
mtx.shape[0]/rate   # about 23 seconds

# [0, 6600, 12700, 17800]
start = 0
end = int(6000 * rate/1000)
phrase = mtx[start:end, ]
phrase.shape
write('daylight.01.wav', rate, phrase)
