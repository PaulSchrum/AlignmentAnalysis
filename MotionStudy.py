import sys, os
from gpsAnalyst import dynamicCsvRecord, createInstanceFromCsv
import gpsAnalyst


testDir = os.path.join(os.getcwd(), 'testData')

inputFile = os.path.join(testDir, r"20180606 Albuquerque.csv")
newInstance = createInstanceFromCsv(inputFile)

outFile = os.path.join(testDir, '20180606 Albuquerque.kml')
theKml = gpsAnalyst.saveAsKML(newInstance, outFile)

dbg = True
