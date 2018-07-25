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


rate, mtx = read("../testData/daylight_1_4.wav")
mtx.shape
mtx.shape[0]/rate   # about 23 seconds

# [0, 6600, 12700, 17800]
start = 0
end = int(6000 * rate/1000)
phrase = mtx[start:end, ]
phrase.shape
write('daylight.01.wav', rate, phrase)
