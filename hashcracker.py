#!/usr/bin/env python

import argparse #prueba con argparse
import hashlib
import time
import concurrent.futures

def funcion_principal(argumentos, hash_target, modo):
    #Abro el archivo en modo r (read)
    with open(argumentos.wordlist, "r", encoding="latin-1") as archivo:
        #coge linea por linea del archivo
        for linea in archivo:
            #Al final de cada linea python pone \n, por tanto hay que limpiarlo (strip())
            palabra = linea.strip()
            #Para calcular el hash convertimos el texto a bytes y aplicamos el hash
            #Aqui habria que poner ifs y calcular el hash correspondiende en funcion de modo
            if modo == 1:
                hash_bytes = hashlib.sha1(palabra.encode())
            elif modo == 2:
                hash_bytes = hashlib.sha224(palabra.encode())
            elif modo == 3:
                hash_bytes = hashlib.sha256(palabra.encode())
            else:
                hash_bytes = hashlib.md5(palabra.encode())
            #Lo extraemos en formato hexadecimal
            hash_limpio = hash_bytes.hexdigest()
            #print(f"Contraseña: {palabra} | Hash: {hash_limpio}")
            if hash_target == hash_limpio:
                print(f"[+] ¡Ataque terminado! Contraseña encontrada: {palabra}")
                return True
        
        #Aqui solo llega si ha hecho todo el bucle y no ha hecho el return true
        print(f"Ataque Fallido! Contraseña no encontrada para el hash {hash_target}")

def inicializacion():    
    #Crear motor y añadir nombre a la herramienta
    parser = argparse.ArgumentParser(description="Cracker de contraseñas con wordlist")
    
    #Añadir los argumentos disponibles
    parser.add_argument("-t", "--target", required=True, help="El hash target que se quiere crackear")
    parser.add_argument("-w", "--wordlist", required=True, help="Ruta del archivo que contiene la wordlist")
    parser.add_argument("-m", "--mode", default=4, type=int, help="Tipo de algoritmo de hasheo: 1 = (SHA1), 2 = (SHA224), 3 = (SHA256), 4 = (MD5)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Muestra mensajes extra")
    
    #Identificar los argumentos dados
    argumentos = parser.parse_args()
    
    algortimoHash = ""
    #pongo a cada num un modo de hash mas bonito que un num
    match argumentos.mode:
        case 1:
            algortimoHash = "SHA1"
        case 2:
            algortimoHash = "SHA224"
        case 3:
            algortimoHash = "SHA256"
        case 4:
            algortimoHash = "MD5"    
    
    #Hago el print del modo verbose
    if argumentos.verbose:
        print(f"[*] Cargando el diccionario: {argumentos.wordlist}")
        print(f"[*] Analizando hash {argumentos.target} usando el modo {argumentos.mode} ({algortimoHash})")
    
    #pongo el hash a crackear en una variable
    hash_target = argumentos.target
    return argumentos, hash_target, argumentos.mode 

if __name__ == "__main__":
    inicio=time.time()
    argums = inicializacion()
    args = argums[0]
    hash_victima = argums[1]
    modo = argums[2]
    #Los threads estos no mejoran nada, ya que solo se ejecuta una vez  
    #with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
        #executor.submit(funcion_principal, args, hash_victima)
    funcion_principal(args, hash_victima, modo)
    final = time.time()
    print(f"Tiempo total: {final-inicio} segundos")







