import unittest

from CrossOverAssignment.app.xml_handler import XMLHandler

class TestXMLHandler(unittest.TestCase):
	"""docstring for XMLHanlderTest"""

	def test_validate_xml_structure(self):
		is_valid = XMLHandler.validate_xml()
		self.assertTrue(is_valid)

	def test_validate_clients(self):
		clients = XMLHandler.get_clients()
		self.assertIsInstance(clients, list)

