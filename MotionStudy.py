import sys, os
from gpsAnalyst import dynamicCsvRecord, createInstanceFromCsv
import gpsAnalyst
import ExtendedPointSequence as EPS


testDir = os.path.join(os.getcwd(), 'testData')

inputFile = os.path.join(testDir, r"20180606 Albuquerque.csv")
gpsPointSequence = createInstanceFromCsv(inputFile)

# outFile = os.path.join(testDir, '20180606 Albuquerque.kml')
# theKml = gpsAnalyst.saveAsKML(gpsPointSequence, outFile)

ExtendedPointSequence = EPS.CreateExtendedPointSequenceFromLatLong(gpsPointSequence)
maxSpeed = max([x.speed for x in ExtendedPointSequence])

dbg = True
