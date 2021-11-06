import itertools, re
import vigenereEncryptDecrypt, frequencyAnalysis, detectEnglishWord

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUM_FREQ_LETTERS = 4 #количество букв на подключ (оптимальный вариант)
KEY_LENGTH = 14 #максимальная длина ключа (можно поставить больше)
NON_LETTERS = re.compile('[^A-Z]')

def main():
    with open('encryptedLetterForVigenereHack.txt', 'r') as file:
        encryptedLetter = file.read().replace('\n', '')
    hackedLetter = hackVigenere(encryptedLetter)
    print(hackedLetter)

#Находит интервалы между повторяющимися последовательностями
def findIntervalsBetweenRepSeq(message):
    message = NON_LETTERS.sub('', message.upper())
    seqIntervals = {} 
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            seq = message[seqStart:seqStart + seqLen]

            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    if seq not in seqIntervals:
                        seqIntervals[seq] = [] 
                    seqIntervals[seq].append(i - seqStart)
    return seqIntervals

#Получаем список множителей меньше KEY_LENGTH + 1
def getListOfFactors(num):
    if num < 2:
        return [] 
    factors = [] 
    for i in range(2, KEY_LENGTH + 1): 
        if num % i == 0:
            factors.append(i)
            factors.append(int(num / i))
    if 1 in factors:
        factors.remove(1)
    return list(set(factors))

#Получаем элемент по первому индексу
def getElementAtIndexOne(el):
    return el[1]

def getMostCommonFactors(seqFactors):
    factorCounts = {}
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1
    factorsByCount = []
    for factor in factorCounts:
        if factor <= KEY_LENGTH:
            factorsByCount.append( (factor, factorCounts[factor]) )
    factorsByCount.sort(key=getElementAtIndexOne, reverse=True)
    return factorsByCount

#метод Касиски позволяет определить длину ключа
def kasiskiExamination(ciphertext):
    repeatedSeqIntervals = findIntervalsBetweenRepSeq(ciphertext)
    seqFactors = {}
    for seq in repeatedSeqIntervals:
        seqFactors[seq] = []
        for interval in repeatedSeqIntervals[seq]:
            seqFactors[seq].extend(getListOfFactors(interval))
    factorsByCount = getMostCommonFactors(seqFactors)
    allKeyLengths = []
    for twoIntTuple in factorsByCount:
        allKeyLengths.append(twoIntTuple[0])
    return allKeyLengths

#Получаем N-е буквы подключей
def getNSubkeysLetters(n, keyLength, message):
    message = NON_LETTERS.sub('', message.upper())
    i = n - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)


def tryHackWithKeyLength(ciphertext, mostPossibleKeyLength):
    ciphertextUp = ciphertext.upper()
    allFreqScores = []
    for nth in range(1, mostPossibleKeyLength + 1):
        nthLetters = getNSubkeysLetters(nth, mostPossibleKeyLength, ciphertextUp)
        freqScores = []
        for possibleKey in ALPHABET:
            decryptedText = vigenereEncryptDecrypt.decrypt(possibleKey, nthLetters)
            keyAndFreqMatchTuple = (possibleKey, frequencyAnalysis.englishFreqMatchScore(decryptedText))
            freqScores.append(keyAndFreqMatchTuple)
        freqScores.sort(key=getElementAtIndexOne, reverse=True)
        allFreqScores.append(freqScores[:NUM_FREQ_LETTERS])
    for i in range(len(allFreqScores)):
        print('Возможные буквы для %s буквы ключа: ' % (i + 1), end='')
        for freqScore in allFreqScores[i]:
            print('%s ' % freqScore[0], end='')
        print()
    for indexes in itertools.product(range(NUM_FREQ_LETTERS), repeat=mostPossibleKeyLength):
        possibleKey = ''
        for i in range(mostPossibleKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0]
        print('Попытка с ключом: %s' % (possibleKey))
        decryptedText = vigenereEncryptDecrypt.decrypt(possibleKey, ciphertextUp)
        if detectEnglishWord.isEnglish(decryptedText):
            origCase = []
            for i in range(len(ciphertext)):
                if ciphertext[i].isupper():
                    origCase.append(decryptedText[i].upper())
                else:
                    origCase.append(decryptedText[i].lower())
            decryptedText = ''.join(origCase)
            print('Возможный взлом шифра с помощью ключа %s:' % (possibleKey))
            print()
            print(decryptedText[:300]) 
            print()
            print('Нажмите Enter, если хотите продолжить')
            response = input('')
    return None


def hackVigenere(ciphertext):
    allKeyLengths = kasiskiExamination(ciphertext)
    keyLengthStr = ''
    for keyLength in allKeyLengths:
        keyLengthStr += '%s ' % (keyLength)
    print('Наиболеее вероятные длины ключа: ' + keyLengthStr + '\n')
    for keyLength in allKeyLengths:
        print('Попытка взломать шифр с ключом длиной %s (%s возможных ключей)...' % (keyLength, NUM_FREQ_LETTERS ** keyLength))
        hackedLetter = tryHackWithKeyLength(ciphertext, keyLength)
        if hackedLetter != None:
            break
    for keyLength in range(1, KEY_LENGTH + 1):
        if keyLength not in allKeyLengths:
            print('Попытка взломать шифр с ключом длиной %s (%s возможных ключей )...' % (keyLength, NUM_FREQ_LETTERS ** keyLength))
            hackedLetter = tryHackWithKeyLength(ciphertext, keyLength)
            if hackedLetter != None:
                break
    return hackedLetter

if __name__ == '__main__':
    main()
