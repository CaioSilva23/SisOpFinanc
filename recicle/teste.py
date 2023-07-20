from hashlib import sha256


senha = 'Caiokaiak@1'

hash_senha = sha256(senha.encode('utf-8')).hexdigest()
print('HASH SALVA',hash_senha)




