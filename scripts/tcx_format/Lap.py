from xml.etree.ElementTree import SubElement

from utils.functions import epochToReadable


class Lap:

    def __init__(self, activity, ident, totalTime, distanceMeters, calories, structValues):
        """ Create Lap """

        """ Create main Lap """
        self.lap = SubElement(activity, 'Lap', attrib={'StartTime': epochToReadable(ident)})

        """ Set total time in seconds """
        self.totalTimeSeconds = SubElement(self.lap, 'TotalTimeSeconds')
        self.totalTimeSeconds.text = str(totalTime/1000.0)

        """ Set total distance meters """
        self.distanceMeters = SubElement(self.lap, 'DistanceMeters')
        self.distanceMeters.text = str(distanceMeters)

        """ Set Calories """
        self.calories = SubElement(self.lap, 'Calories')
        self.calories.text = str(calories)

        """ Set Intensity """
        self.intensity = SubElement(self.lap, 'Intensity')
        self.intensity.text = 'Active'

        """ Set TriggerMethod """
        self.triggerMethod = SubElement(self.lap, 'TriggerMethod')
        self.triggerMethod.text = 'Manual'

        """ Set Track """
        self.track = SubElement(self.lap, 'Track')

        """ Initialize Track structure """
        self.trackpoint = None
        self.time = None
        self.position = None
        self.latitude = None
        self.longitude = None
        self.distance = None

        self.buildTrack(structValues)


    def buildTrack(self, structValues):
        """ Create trackpoint """

        for idx in range(0, len(structValues)):
            """ Set trackpoint """
            self.trackpoint = SubElement(self.track, 'Trackpoint')

            """ Set time """
            self.time = SubElement(self.trackpoint, 'Time')
            self.time.text = epochToReadable(structValues[idx]['time'])

            """ Set position """
            self.position = SubElement(self.trackpoint, 'Position')

            """ Set GPS data """
            self.latitude = SubElement(self.position, 'LatitudeDegrees')
            self.latitude.text = str(structValues[idx]['latitude'])
            self.longitude = SubElement(self.position, 'LongitudeDegrees')
            self.longitude.text = str(structValues[idx]['longitude'])

            """ Set current distance """
            self.distance = SubElement(self.trackpoint, 'DistanceMeters')
            self.distance.text = str(structValues[idx]['distance'])
