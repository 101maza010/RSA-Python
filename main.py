#Cciptosistema RSA

import random as rnd
import math

#VARIABLES GLOBALES:
minimo, maximo = 1000, 10000
e = 65537
lenght = 4 #longitud de numeros a encriptar

#FUNCIONES GLOBALES
def is_prime(n):
    top = n//2
    if n < 2:
        return False
    #test de primalidad
    for k in range(2, top):
        if n % k == 0:
            return False
    return True

def gen_prime(min, max):
    p = rnd.randint(min, max)
    while not is_prime(p) == True:
        p = rnd.randint(min, max)
    return p

#inverso mod n
def mod_inv(a, phi):
    for d in range(3, phi-1):
        if (d * a) % phi == 1:
            return d
    return -1

#funciones para codificar y decodificar el texto

def split_number(n, part_size):
    base = 10 ** part_size
    L = []
    while n:
        n, part = divmod(n, base)
        L.append(part)
    return L[::-1]
 
def join_number(L, part_size):
    base = 10 ** part_size
    n = 0
    L = L[::-1]
    while L:
        n = n * base + L.pop()
    return n

#funcion para codificar
def codif(m, part):
    m_ascii = [ord(car) for car in m] #lista con cada caracter en ascii
    m_ascii_join = join_number(m_ascii, 3)
    
    m_cod = split_number(m_ascii_join, part)
    return m_cod

#funcion para decodificar

def decodif(m, part):
    m_ascii_join = join_number(m, part)
    m_ascii_split = split_number(m_ascii_join, 3)
    
    m_dec = "".join(chr(c) for c in m_ascii_split) #lista con cada caracter en ascii
    return m_dec

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#CLASE USUARIO
class User:

    def __init__(self, j):
        self.plain_text = ""
        self.num_user = j
        

    #generacion de llaves
    def gen_key(self, min, max, e):
        self.d = -1
        #self.p = 9043
        #self.q = 4567
        #self.phi_n = (self.p-1) * (self.q-1)
        #self.d = mod_inv(e, self.phi_n)
        while self.d == -1:
            self.p = gen_prime(min, max)
            self.q = gen_prime(min, max)
            self.phi_n = (self.p-1) * (self.q-1)
            self.d = mod_inv(e, self.phi_n)
        self.n = self.p * self.q

    #cifrado global y descifrado personal
    def encrypt(self, n): 
        plain_text = str(self.plain_text) #convierte a variable utilizable
        message_encoded = codif(plain_text, lenght)
        self.ciphertext = [pow(c, e, n) for c in message_encoded]

    def decrypt(self):
        ciphertext = self.ciphertext #convierte a variable utilizable
        message_encoded = [pow(c, self.d, self.n) for c in ciphertext]
        message = decodif(message_encoded, lenght)
        return message

    #enviar llave publica
    def send_publickey(self):
        content = "Llave publica usuario " + str(self.num_user) + ": " + str(self.n)
        file = open("textos\publickey_users", "a", encoding="utf-8")
        file.write(content + "\n")
        file.close()

    #generar llave privada (solo para consulta o propositos educaivos)
    def private_keys(self):
        content = "p: " + str(self.p) + ", q: " + str(self.q)
        file = open("textos\privatekey_user"+str(self.num_user), "a", encoding="utf-8")
        file.write(content + "\n")
        file.close()

    #enviar mensaje
    def send_message(self, n):
        file1_name = "textos\chat_user" + str(self.num_user) + ".txt"
        file2_name = "textos\sent_messages_user" + str(self.num_user)
        file1 = open(file1_name, "r", encoding="utf-8")
        self.plain_text = file1.read()
        file1.close()
        file2 = open(file2_name, "w", encoding="utf-8")
        self.encrypt(n)
        for item in self.ciphertext:
            file2.write(str(item)+"\n")
        file2.close()

    #obtener mensaje(i.e, leer mensaje cifrado del otro usuario y usar mi llave privada para leerlo)
    def read_message(self, k):
        file1_name = "textos\sent_messages_user" + str(k)
        file2_name = "textos\\received_messages_user" + str(self.num_user)
        file1 = open(file1_name, "r", encoding="utf-8")
        ciphertext = file1.readlines()
        file1.close()
        self.ciphertext = []
        for item in ciphertext:
            self.ciphertext.append(int(item.rstrip('\n')))
        message = self.decrypt()
        file2 = open(file2_name, "w", encoding="utf-8")
        file2.write(message)
        file2.close()


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#INTERACCION CON EL USUARIO

#MENU:

def mostrar_menu(opciones):
    print('Seleccione una opción:')
    for clave in sorted(opciones):
        print(f' {clave}) {opciones[clave][0]}')

def leer_opcion(opciones):
    while (a := input('Opción: ')) not in opciones:
        print('Opción incorrecta, vuelva a intentarlo.')
    return a

def ejecutar_opcion(opcion, opciones):
    opciones[opcion][1]()

def generate_menu(opciones, opcion_salida):
    opcion = None
    while opcion != opcion_salida:
        mostrar_menu(opciones)
        opcion = leer_opcion(opciones)
        ejecutar_opcion(opcion, opciones)
        print()

def menu():
    opciones = {
        '1': ('Enviar mensaje de usuario 1', accion1),
        '2': ('Enviar mensaje de usuario 2', accion2),
        '3': ('Salir', salir)
    }

    generate_menu(opciones, '3')

def accion1():
    user1.send_message(user2.n)
    user2.read_message(1)


def accion2():
    user2.send_message(user1.n)
    user1.read_message(2)


def salir():
    print('Saliendo')


if __name__ == '__main__':
    print("CIFRADO RSA")

    #asignacion llave privada a usuario 1
    user1 = User(1)
    user1.gen_key(minimo, maximo, e)
    print("Usuario 1: Llave privada asignada.")


    #asignar llave privada a usuario 2
    user2 = User(2)
    user2.gen_key(minimo, maximo, e)
    print("Usuario 2: Llave privada asignada.")

    file = open("textos\publickey_users", "w")
    file.close

    user1.send_publickey()
    user1.private_keys()

    user2.send_publickey()
    user2.private_keys()


    menu()



