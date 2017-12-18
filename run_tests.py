import unittest

# importing test modules
from CrossOverAssignment.tests import test_xml_handler
from CrossOverAssignment.tests import test_system_monitor
from CrossOverAssignment.tests import test_crossover_assignment

# initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_xml_handler))
suite.addTests(loader.loadTestsFromModule(test_system_monitor))
suite.addTests(loader.loadTestsFromModule(test_crossover_assignment))

# initialize runner
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
