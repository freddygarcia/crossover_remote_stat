from lxml import etree
from xml.etree import ElementTree

class XMLHandler(object):
	"""Handle all interactions with clients xml file"""
	CLIENTS_FILE = './crossover_remote_stat/data/clients.xml'
	SCHEMA_FILE  = './crossover_remote_stat/data/clients_xml.xsd'

	@staticmethod
	def read_source():
		""""Return the root element of clints file"""
		try:
			return ElementTree.parse(XMLHandler.CLIENTS_FILE).getroot()
		except ElementTree.ParseError as e:
			raise ElementTree.ParseError('Malformed clients xml file')

	@staticmethod
	def validate_xml():
		"""Make sure clients.xml has the rigth estructure"""
		validation = False
		try:
			# load xml schema (xsd file) 
			schema = etree.parse(XMLHandler.SCHEMA_FILE)
			# load xml clients (xml file) 
			xml = etree.parse(XMLHandler.CLIENTS_FILE)

			# generate a xmlschema validator
			XMLSchema = etree.XMLSchema(schema)
			# obtain xml valition
			validation = XMLSchema.validate(xml)
		except OSError as e:
			# fail if either xml or xsd file doest not exist 
			raise Exception('Ensure {} exist'.format(' and '.join([XMLHandler.CLIENTS_FILE, XMLHandler.SCHEMA_FILE])))
		except Exception as e:
			# fail if either xml or xsd file aren't rigth defined 
			raise Exception('{} may not be rigth formatted'.format(' or '.join([XMLHandler.CLIENTS_FILE, XMLHandler.SCHEMA_FILE])))

		return validation

	@staticmethod
	def get_clients():
		""""Return a dict list with clients config """
		ITERATOR_CLIENT_TAG = 'client'
		ITERATOR_ALERT_TAG = 'alert'
		xml_root = XMLHandler.read_source()

		def get_client_alert(client_node):
			"""Get alert node inside clients node"""
			client = client_node.attrib
			# for each 'client' node, append a 'alert' key to the dict
			# with alert data
			client[ITERATOR_ALERT_TAG] = [alert.attrib for alert in client_node]
			return client

		return [ get_client_alert(node) for node in xml_root.findall(ITERATOR_CLIENT_TAG)]
