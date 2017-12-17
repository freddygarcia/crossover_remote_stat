from subprocess import Popen, PIPE
from datetime import datetime

class InformationGather:

	def get_uptime(self):
		p = Popen("systeminfo", shell=True, stdin=PIPE, stdout=PIPE)
		(child_stdin, child_stdout) = (p.stdin, p.stdout)
		lines = child_stdout.readlines()
		child_stdin.close()
		child_stdout.close() 

		info_cad = str(list(filter(lambda x: b'System Boot Time' in x, lines))[0])

		date, time, ampm = info_cad.split()[3:6]
		date = date.replace(',', '')

		m, d, y = [int(v) for v in date.split('/')]
		H, M, S = [int(v) for v in time.split(':')]

		return datetime(y, m, d, H, M, S)


