import docx
import glob
import cv2
import os
import numpy as np

print("\n\n---------------------------------------------------")
print("Welcome to Word Bank !!! Boost your GRE Preparation")
print("---------------------------------------------------\n")

path_to_docx = "C:\\Users\\Admin\\OneDrive\\Documents\\"

def readDocx(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        split_list = para.text.split(':')
        if len(split_list) > 2:
            for i in range(len(split_list)-1):
                fullText.append(split_list[i].strip() + ':' + split_list[len(split_list)-1])
        else:
            fullText.append(para.text)
    return fullText

def renderWords(pointer, lines):
    key = 0
    while key != 27:
        line = lines[pointer]
        line = line.split(':')
        word = np.zeros((200, 1800, 3), np.uint8)
        meaning = np.zeros((200, 1800, 3), np.uint8)
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 2
        thickness = 2
        word = cv2.putText(word, line[0], org, font, 
                    fontScale, (255, 0, 0), thickness, cv2.LINE_AA)
        if len(line[1]) > 50:
            line[1] = line[1][0:50] + "-\n" + line[1][50:]
        y0, dy = 50, 65
        for i, ln in enumerate(line[1].split('\n')):
            y = y0 + i*dy
            meaning = cv2.putText(meaning, ln, (50, y), font, 
                    fontScale, (0, 255, 0), thickness, cv2.LINE_AA)
        cv2.imshow('word', word)
        key = cv2.waitKey(0)
        cv2.imshow('meaning', meaning)
        key = cv2.waitKey(0)
        if key == 52 and pointer > 0:
            pointer -= 1
        elif key == 54 and pointer < len(lines)-1:
            pointer += 1
        cv2.destroyAllWindows()
    return pointer

try:
    f = glob.glob(path_to_docx + 'wordBank_*.txt')
    wordFile = open(f[0], "r")
    print("Backup Found, Reading from backup")
    pointer = int(f[0].split('.')[0].split('_')[1])
    lines = wordFile.readlines()
    pointer = renderWords(pointer, lines)
    wordFile.close()
    os.rename(f[0], path_to_docx + 'wordBank_' + str(pointer) + '.txt')
except:
    print("Backup Not Found, Creating new backup")
    fullText = readDocx(path_to_docx + 'Word Bank.docx')  
    wordFile = open(path_to_docx + "wordBank_0.txt", "w")    
    for line in fullText:
        wordFile.write(line + "\n") 
    wordFile.close()