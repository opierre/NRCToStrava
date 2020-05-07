from xml.etree.ElementTree import SubElement

from utils.functions import epochToReadable


class Activity:

    def __init__(self, activities, ident):
        """ Create Activity """

        self.activity = SubElement(activities, 'Activity', attrib={'Sport': 'Running',
                                                                 'Notes': 'Generated from NRCToStrava'})

        self.id = SubElement(self.activity, 'Id')
        self.id.text = epochToReadable(ident)
