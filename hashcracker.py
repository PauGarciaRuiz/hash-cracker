#!/usr/bin/env python

import argparse #prueba con argparse
import hashlib
import time
import concurrent.futures

#Cada modo apunta a su funcion de hash, asi me ahorro el bloque de ifs/match
ALGORITMOS = {1: hashlib.sha1, 2: hashlib.sha224, 3: hashlib.sha256, 4: hashlib.md5}
#El nombre "bonito" de cada modo, solo para el mensaje verbose
NOMBRES = {1: "SHA1", 2: "SHA224", 3: "SHA256", 4: "MD5"}

def funcion_principal(args):
    #Cojo la funcion de hash del diccionario segun el modo (una sola vez, no en cada vuelta)
    funcion_hash = ALGORITMOS[args.mode]
    #Abro el archivo en modo r (read)
    with open(args.wordlist, "r", encoding="latin-1") as archivo:
        #coge linea por linea del archivo
        for linea in archivo:
            #Al final de cada linea python pone \n, por tanto hay que limpiarlo (strip())
            palabra = linea.strip()
            #Para calcular el hash convertimos el texto a bytes y aplicamos el hash
            hash_bytes = funcion_hash(palabra.encode())
            #Lo extraemos en formato hexadecimal
            hash_limpio = hash_bytes.hexdigest()
            #print(f"Contraseña: {palabra} | Hash: {hash_limpio}")
            if args.target == hash_limpio:
                print(f"[+] ¡Ataque terminado! Contraseña encontrada: {palabra}")
                return True

        #Aqui solo llega si ha hecho todo el bucle y no ha hecho el return true
        print(f"Ataque Fallido! Contraseña no encontrada para el hash {args.target}")

def inicializacion():
    #Crear motor y añadir nombre a la herramienta
    parser = argparse.ArgumentParser(description="Cracker de contraseñas con wordlist")

    #Añadir los argumentos disponibles
    parser.add_argument("-t", "--target", required=True, help="El hash target que se quiere crackear")
    parser.add_argument("-w", "--wordlist", required=True, help="Ruta del archivo que contiene la wordlist")
    parser.add_argument("-m", "--mode", default=4, type=int, choices=[1, 2, 3, 4], help="Tipo de algoritmo de hasheo: 1 = (SHA1), 2 = (SHA224), 3 = (SHA256), 4 = (MD5)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Muestra mensajes extra")

    #Identificar los argumentos dados
    args = parser.parse_args()

    #Hago el print del modo verbose
    if args.verbose:
        print(f"[*] Cargando el diccionario: {args.wordlist}")
        print(f"[*] Analizando hash {args.target} usando el modo {args.mode} ({NOMBRES[args.mode]})")

    #devuelvo el objeto args directamente y luego accedo con args.target, args.wordlist, args.mode
    return args

if __name__ == "__main__":
    inicio=time.time()
    args = inicializacion()
    #Los threads estos no mejoran nada, ya que solo se ejecuta una vez
    #with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
        #executor.submit(funcion_principal, args)
    funcion_principal(args)
    final = time.time()
    print(f"Tiempo total: {final-inicio} segundos")
