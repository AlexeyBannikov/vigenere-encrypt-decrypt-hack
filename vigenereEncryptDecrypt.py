ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def encrypt(key, letter):
    result = []

    keyIndex = 0
    key = key.upper()

    for symbol in letter:
        num = ALPHABET.find(symbol.upper())
        if num != -1:
            num += ALPHABET.find(key[keyIndex])
            num %= len(ALPHABET)

            if symbol.isupper():
                result.append(ALPHABET[num])
            elif symbol.islower():
                result.append(ALPHABET[num].lower())

            keyIndex += 1 
            if keyIndex == len(key):
                keyIndex = 0
        else:
            result.append(symbol)

    return ''.join(result)

def decrypt(key, letter):
    result = []

    keyIndex = 0
    key = key.upper()

    for symbol in letter:
        num = ALPHABET.find(symbol.upper())
        if num != -1:
            num -= ALPHABET.find(key[keyIndex])
            num %= len(ALPHABET)

            if symbol.isupper():
                result.append(ALPHABET[num])
            elif symbol.islower():
                result.append(ALPHABET[num].lower())

            keyIndex += 1 
            if keyIndex == len(key):
                keyIndex = 0
        else:
            result.append(symbol)

    return ''.join(result)



    
    
