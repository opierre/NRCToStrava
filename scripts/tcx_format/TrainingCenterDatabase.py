from xml.etree.ElementTree import Element


class TrainingCenterDatabase:

    def __init__(self):
        """ Create TrainingCenterDatabase """

        self.root = Element('TrainingCenterDatabase',
                            attrib={
                                'xsi:schemaLocation': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd',
                                'xmlns:ns5': 'http://www.garmin.com/xmlschemas/ActivityGoals/v1',
                                'xmlns:ns3': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2',
                                'xmlns:ns2': 'http://www.garmin.com/xmlschemas/UserProfile/v2',
                                'xmlns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
                                'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'
                            })
