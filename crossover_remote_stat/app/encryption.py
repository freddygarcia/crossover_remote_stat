from cryptography.fernet import Fernet

class Encription():

	def __init__(self, cipher_key):
		self.cipher = Fernet(cipher_key)

	def encrypt(self, cad):
		return self.cipher.encrypt(cad)

	def decrypt(self, cad):
		return self.cipher.decrypt(cad)

