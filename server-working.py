import time, socket, sys, rsa

print("\nWelcome to Chat Room\n")
print("Initialising....\n")
time.sleep(1)

s = socket.socket()
host = 'localhost'
ip = socket.gethostbyname(host)
port = 1234
s.bind((host, port))
print(host, "(", ip, ")\n")
name = input(str("Enter your name: "))

keydata = b'-----BEGIN RSA PRIVATE KEY-----\nMIICYwIBAAKBgQCHbeP3oP/tEffeTpjhsqptGscyYSKuYLXEx4Lf1gVemzgF6+6cwVE4odFQvVj9lGSirF9w4YqpGGWdMNcOBD9jkYwkgMrXpdRqBCj1Kr0gJDCD6N5HKhb4ec0rFHeUOjg8/VQOGEga/EYAaMJwwhJ7z9DWZv6Nhy99cbhGZudt6wIDAQABAoGBAIAkEEGsCrwL9lZYU/uqC+u0HKqkkiYgx5xrkn+sh+QeRgIEXP/hQrKtGdqlbmBxWk85fgzWu1aICQ2UuhGB9zeFHmZd88XGL7KZ6lnyPPqPxS1/AcskA0Dfe/6F5KjO6SHR2JUQS9iGyxqVnMvIuvnqBAS0pfVRvdGzN2ECv32RAkUAwBKpL0Cj2YtVFSU4GVQpnTlJYDsBy0f9i+63pSb96LKGMRQLjpaDG2H0bdmVbO3VpPlxjou7yITrepIjmLw3BFr5Qb0CPQC0gPokxV1vNu4pgpOm7xsH6LG9QBtlJMyXGvQ61I1MlsL48I6uW4vN5t4kfKgSUXpszNNlRD5OZ2IN5McCRQC/oh6wqXKQuyZBeaf2BXWbiyt9WoIYupPqyFrr6PJN98hRMSmystLOQDYqX3tpegW9mq7ExP+vOYbj/OiNG8RckRO9lQI9AJGKqad6iDMDfJd11O42P3pqEt6A0VYFjP2N2z2QYvpNWZp2BOXrpNd5/sY2ySI0Fl2h7hXqJ776NyLywwJFAI7JsOTpT/JrDp9yy+xk8+Qc27Jz5+qnskCY+YZ1PBss504cyz4HGZshGlDEWnDR3V8YL63LZ3jIPyUnixAd6JP1auaK\n-----END RSA PRIVATE KEY-----'
privkey = rsa.PrivateKey.load_pkcs1(keydata,'PEM')


pkeydata = b'-----BEGIN RSA PUBLIC KEY-----\nMIGJAoGBAJH9WnkCPhFIJIuu0lSTVfhqR60kMNb5RUWy+9kNxdueLLEU/LSgZAp6c0YILwsgfvy1/6iL6Yr9E3KoOP3+d7/X9w+g6dWQXpAt2Fgpkpb5eNiYbFIB05eioy8UT+X0v2Ip1PoVMyokErbf1NOUVb117NUxFDyDnQec6DCErbwbAgMBAAE=\n-----END RSA PUBLIC KEY-----'
clientpubkey = rsa.PublicKey.load_pkcs1(pkeydata)
           
s.listen(1)
print("\nWaiting for incoming connections...\n")
conn, addr = s.accept()
print("Received connection from ", addr[0], "(", addr[1], ")\n")

s_name = conn.recv(1024)
s_name = rsa.decrypt(s_name, privkey).decode()
print(s_name, "has connected to the chat room\nEnter [e] to exit chat room\n")
conn.send(rsa.encrypt(name.encode(), clientpubkey))

while True:
    message = input(str("Me : "))
    if message == "[e]":
        message = "Left chat room!"
        conn.send(rsa.encrypt(message.encode(), clientpubkey))
        print("\n")
        break
    conn.send(rsa.encrypt(message.encode(), clientpubkey))
    message = conn.recv(1024)
    print("Encrypted message from", s_name, ":", message)
    message = rsa.decrypt(message, privkey).decode()
    print("Decrypted message from", s_name, ":", message)