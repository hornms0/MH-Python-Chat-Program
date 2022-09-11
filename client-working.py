import time, socket, sys, rsa

print("\nWelcome to Chat Room\n")
print("Initialising....\n")
time.sleep(1)

s = socket.socket()
shost = socket.gethostname()
ip = 'localhost'
print(shost, "(", ip, ")\n")
host = 'localhost'
name = input(str("\nEnter your name: "))
port = 1234
print("\nTrying to connect to ", host, "(", port, ")\n")
time.sleep(1)
s.connect((host, port))
print("Connected...\n")

keydata = b'-----BEGIN RSA PRIVATE KEY-----\nMIICYgIBAAKBgQCR/Vp5Aj4RSCSLrtJUk1X4aketJDDW+UVFsvvZDcXbniyxFPy0oGQKenNGCC8LIH78tf+oi+mK/RNyqDj9/ne/1/cPoOnVkF6QLdhYKZKW+XjYmGxSAdOXoqMvFE/l9L9iKdT6FTMqJBK239TTlFW9dezVMRQ8g50HnOgwhK28GwIDAQABAoGAOjdDmrmwMogIOsNuEFfoknUfPAYQi8k/PHoRQA7j9Z3vyHXMB+NlwV/vE+AzkkZVHUUePAH/EXO2C6TVL6Mob6wEmHVkvbajrlN70CGSrN8rCm8ax6c2k+vyy7k5oVfE/irw5cOfMsnsblFlkqYxkX0EOmBmEP0k+w4VVQ6IyGECRQDWusdrUneTVq0IT8NLyogu6m8hfn4KSJI6np48ztdec0MhfISwR3R3KZE6JS4J8WW/E5q36Lk+XJ6mPyNgtweJ6kMYSQI9AK4MZry4PV0ETarZrAmK4IqpIKeFoRY027FtVVBxHbBq5XixlhZWUdxrPGnWmuEJh/NolpUyBnRCpkVZQwJFAIRfVmpJx180Eq1KBpnle/h4GxQp12ddf4/VkrTnygr2wU6WZXIKSrjfDiErJGuKve+CFWIEfJX+IOtZhuSrUGFr4frJAj0AglvrfyIHY+nbOkH6ptMLxw9R0+c0det1OPkI001FzWLjKHjqTySr/4maIDOKoU6AMwF895YWW3GoE3z9AkUApiGI8+X0T94L2Nvb5cpjf0oqZXN0DKrBX0rDyxBNFAuV1uH63x6TG4TDGwfj5MjQ14hmX1+/VXSnhQLMZHqx1DantwM=\n-----END RSA PRIVATE KEY-----'
privkey = rsa.PrivateKey.load_pkcs1(keydata,'PEM')

pkeydata = b'-----BEGIN RSA PUBLIC KEY-----\nMIGJAoGBAIdt4/eg/+0R995OmOGyqm0axzJhIq5gtcTHgt/WBV6bOAXr7pzBUTih0VC9WP2UZKKsX3DhiqkYZZ0w1w4EP2ORjCSAytel1GoEKPUqvSAkMIPo3kcqFvh5zSsUd5Q6ODz9VA4YSBr8RgBownDCEnvP0NZm/o2HL31xuEZm523rAgMBAAE=\n-----END RSA PUBLIC KEY-----'

serverpubkey = rsa.PublicKey.load_pkcs1(pkeydata)

s.send(rsa.encrypt(name.encode(), serverpubkey))
s_name = s.recv(1024)
s_name = rsa.decrypt(s_name, privkey).decode()
print(s_name, "has joined the chat room\nEnter [e] to exit chat room\n")

while True:
    message = s.recv(1024)
    print("Encrypted message from", s_name, ":", message)
    message = rsa.decrypt(message, privkey).decode()
    print("Decrypted message from", s_name, ":", message)
    message = input(str("Me : "))
    if message == "[e]":
        message = "Left chat room!"
        s.send(rsa.encrypt(message.encode(), serverpubkey))
        print("\n")
        break
    s.send(rsa.encrypt(message.encode(), serverpubkey))
