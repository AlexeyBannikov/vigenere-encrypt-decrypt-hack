import subprocess
import sys
import os
from tkinter import *
from tkinter import messagebox
from vigenereEncryptDecrypt import encrypt, decrypt

root = Tk()
root.title("Vigenere Cipher")
root.geometry("650x200")
    
def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)
 
def encryptClicked():
    result = encrypt(keyText.get(), letterText.get())
    messagebox.showinfo("Encrypted text - текст скопирован в буфер обмена", result)
    copy2clip(result)

def decryptClicked():
    result = decrypt(keyText.get(), letterText.get())
    messagebox.showinfo("Decrypted text - текст скопирован в буфер обмена", result)
    copy2clip(result)

def hackClicked():
    result = encryptedText.get()
    with open('encryptedLetterForVigenereHack.txt', 'w') as file:
        f = file.write(result)
    os.system('python vigenereHack.py')

letterText = StringVar()
keyText = StringVar()
encryptedText = StringVar()
 
letter_label = Label(text="Введите текст:")
key_label = Label(text="Введите ключ:")
encrypted_label = Label(text="Зашифрованный текст:")
 
letter_label.grid(row=0, column=0)
key_label.grid(row=1, column=0)
encrypted_label.grid(row=4,column=0)
 
letter_entry = Entry(width="50", textvariable=letterText)
key_entry = Entry(width="50", textvariable=keyText)
encrypted_entry = Entry(width="55", textvariable=encryptedText)
 
letter_entry.grid(row=0, column=1)
key_entry.grid(row=1, column=1)
encrypted_entry.grid(row=4, column=1)

letter_entry.insert(0, "The Vigenere cipher is a method of encrypting alphabetic text by using a series of interwoven Caesar ciphers, based on the letters of a keyword. It employs a form of polyalphabetic substitution")
key_entry.insert(0, "albkde")
 
encryptButton = Button(text="Encrypt", command=encryptClicked)
encryptButton.grid(row=2, column=1)

decryptButton = Button(text="Decrypt", command=decryptClicked)
decryptButton.grid(row=3, column=1)

decryptButton = Button(text="HACK", comman=hackClicked)
decryptButton.grid(row=5, column=1)
 
root.mainloop()

