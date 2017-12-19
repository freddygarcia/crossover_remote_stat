import unittest

from crossover_remote_stat import get_config

class TestCrossOverAssigment(unittest.TestCase):
	"""docstring for TestCrossOverAssigment"""

	def test_exists_config(self):
		config = get_config()
		self.assertNotEqual(config.sections(), [])