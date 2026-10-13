# Hash Cracker

A dictionary-attack tool that tries to recover the plaintext behind a hash by
hashing every word in a wordlist and comparing it against the target. I wrote it
while studying how password hashing works and why unsalted hashes fall so fast to
a good wordlist.

It walks the wordlist line by line, hashes each candidate with the algorithm you
pick, and stops the moment it finds a match.

## Requirements

- Python 3.9+
- **No external dependencies** — it only uses the standard library (`hashlib`),
  so there's no `requirements.txt` and nothing to `pip install`. It runs on any
  Python 3.

## Usage

```bash
python hashcracker.py -t <hash> -w <wordlist> [-m <mode>] [-v]
```

| Option | Description |
| --- | --- |
| `-t`, `--target` | The hash you want to crack (required) |
| `-w`, `--wordlist` | Path to the wordlist file (required) |
| `-m`, `--mode` | Algorithm: `1` = SHA-1, `2` = SHA-224, `3` = SHA-256, `4` = MD5 (default: `4`) |
| `-v`, `--verbose` | Print extra info while running |

### Example

```bash
# MD5 of "password"
python hashcracker.py -t 5f4dcc3b5aa765d61d8327deb882cf99 -w rockyou.txt -m 4 -v
```

```
[*] Cargando el diccionario: rockyou.txt
[*] Analizando hash 5f4dcc3b5aa765d61d8327deb882cf99 usando el modo 4 (MD5)
[+] ¡Ataque terminado! Contraseña encontrada: password
Tiempo total: 0.03 segundos
```

## Notes and limitations

- Only as good as the wordlist — if the password isn't in the list, it won't find it.
- Handles unsalted hashes only; salted schemes (bcrypt, Argon2, …) are out of scope by design.
- The wordlist is read with `latin-1` so it won't choke on non-UTF-8 lines like `rockyou.txt`.
- Wordlists aren't included in the repo (they're large and have their own licensing).
  On Kali, `rockyou.txt` lives in `/usr/share/wordlists/`.

## Disclaimer

For use only on hashes from your own systems or from authorized security
exercises and CTFs. Cracking credentials you don't own is illegal.
