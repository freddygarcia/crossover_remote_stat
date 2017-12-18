import unittest

from CrossOverAssignment.app.client_side.client import SystemMonitor

class TestSystemMonitor(unittest.TestCase):
	"""docstring for TestSystemMonitor"""

	def test_get_system_state(self):
		systemmonitor = SystemMonitor()
		self.assertIsNot(systemmonitor.uptime, None)
		self.assertIsInstance(systemmonitor.platform, str)
		self.assertIsInstance(systemmonitor.cpu_percent, float)
		self.assertIsInstance(systemmonitor.memory_usage, float)
		self.assertIsInstance(systemmonitor.hostname, str)
