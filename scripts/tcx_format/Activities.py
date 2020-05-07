from xml.etree.ElementTree import SubElement


class Activities:

    def __init__(self, root):
        """ Create Activities """

        self.activities = SubElement(root, 'Activities')
