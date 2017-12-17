import xml.etree.ElementTree as ElementTree

class XML(object):
	CLIENTS_FILE = 'clients.xml'

	def read_source(self):
		""""Return the root element of clints file"""
		try:
			return ElementTree.parse(self.CLIENTS_FILE).getroot()
		except ElementTree.ParseError as e:
			raise ElementTree.ParseError('Malformed clients xml file')

	def get_clients(self):
		""""Return a dict list with clients config """
		ITERATOR_TAG = 'client'
		xml_root = self.read_source()

		return	[{ key: node.get(key) for key in node.keys()} for node in xml_root.findall(ITERATOR_TAG)]
