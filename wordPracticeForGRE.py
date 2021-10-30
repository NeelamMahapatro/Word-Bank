import docx
import glob
import cv2
import os
import numpy as np
import random

print("\n\n---------------------------------------------------")
print("Welcome to Word Bank !!! Boost your GRE Preparation")
print("---------------------------------------------------\n")

path_to_docx = "C:\\Users\\Admin\\OneDrive\\Documents\\"
path_to_backup = "E:\\Word-Bank\\"

def readDocx(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        split_list = para.text.split(':')
        if len(split_list) > 2:
            for i in range(len(split_list)-1):
                fullText.append(split_list[i].strip() + ':' + split_list[len(split_list)-1].strip())
        else:
            fullText.append(para.text)
    return fullText

def getPointer(pointer):
    pointer = pointer.split('.')
    pointer = pointer[len(pointer)-2]
    pointer = pointer.split('_')
    pointer = int(pointer[len(pointer)-1])
    return pointer

def renderWords(pointer, lines):
    key = 0
    num_total = len(lines)
    while key != 27 and pointer < len(lines):
        line = lines[pointer]
        line = line.split(':')
        word = np.zeros((200, 1800, 3), np.uint8)
        meaning = np.zeros((200, 1800, 3), np.uint8)
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 2
        thickness = 2
        word = cv2.putText(word, str(num_total - pointer), (50, 50), font, 
                    1, (255, 255, 255), thickness, cv2.LINE_AA)
        word = cv2.putText(word, line[0], (200, 100), font, 
                    fontScale, (0, 0, 255), thickness, cv2.LINE_AA)
        break_point = 45
        if len(line[1]) > break_point:
            line[1] = line[1][0:break_point] + "-\n" + line[1][break_point:]
        y0, dy = 50, 65
        for i, ln in enumerate(line[1].split('\n')):
            y = y0 + i*dy
            meaning = cv2.putText(meaning, ln, (50, y), font, 
                    fontScale, (0, 255, 0), thickness, cv2.LINE_AA)
        cv2.imshow('word', word)
        key = cv2.waitKey(0)
        if key == 52:
            if pointer > 0:
                pointer -= 1
            continue
        elif key == 27:
            continue
        cv2.imshow('meaning', meaning)
        key = cv2.waitKey(0)
        if key == 52 and pointer > 0:
            pointer -= 1
        elif key == 54 and pointer < len(lines):
            pointer += 1
        cv2.destroyAllWindows()
    return pointer

def generateBackup():
    print("Backup Not Found, Creating new backup")
    fullText = readDocx(path_to_docx + 'Word Bank.docx') 
    random.shuffle(fullText) 
    wordFile = open(path_to_backup + "wordBank_0.txt", "w")    
    for line in fullText:
        if len(line) > 0:
            wordFile.write(line + "\n") 
    wordFile.close()
    return path_to_backup + "wordBank_0.txt"

f = glob.glob(path_to_backup + 'wordBank_*.txt')
if len(f) == 0:
    f.append(generateBackup())
else:
    print("Backup Found, Reading from backup")
wordFile = open(f[0], "r")
pointer = getPointer(f[0])
lines = wordFile.readlines()
pointer = renderWords(pointer, lines)
if pointer == len(lines):
    print("Word List Complete. Thank You")
wordFile.close()
os.rename(f[0], path_to_backup + 'wordBank_' + str(pointer) + '.txt')