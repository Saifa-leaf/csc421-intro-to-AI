import matplotlib.pyplot as plt
import pickle 
import numpy as np
import os 
  
print("Q6")
wordCheck = ["awful", "bad", "boring", "dull", "effective", "enjoyable", "great", "hilarious"]
    
posCount = [0,0,0,0,0,0,0,0]
posResult = [0,0,0,0,0,0,0,0]
wCount = 0    
fileCount = 0
path = r"C:\Users\Leaf\Downloads\txt_sentoken\pos"
os.chdir(path) 
priorProbPos = {}
priorProbNeg = {}
  
# for txt in os.listdir(): 
for filename in os.scandir(path):
    if filename.is_file():
#         print(filename.path
        fileCount +=1
#         file_path = f"{path}\{txt}"

        f = open(filename.path, "r")
    #     print(f.read()) 
        for line in f:
            for word in line.split():
                if word.isalpha():
                    wCount += 1
                if (word.lower() == "awful"):
                    posCount[0] =1
                elif (word.lower() == "bad"):
                    posCount[1] =1
                elif (word.lower() == "boring"):
                    posCount[2] =1
                elif (word.lower() == "dull"):
                    posCount[3] =1
                elif (word.lower() == "effective"):
                    posCount[4] =1
                elif (word.lower() == "enjoyable"):
                    posCount[5] =1
                elif (word.lower() == "great"):
                    posCount[6] =1
                elif (word.lower() == "hilarious"):
                    posCount[7] =1
        

        for i in range(len(posCount)):
            posResult[i] += posCount[i]
        posCount = [0,0,0,0,0,0,0,0]

        f.close()
print("\n")
print("positive")
# print(wordCheck)
# print(posCount)
print("word count: "+ str(wCount))
print("file count: " + str(fileCount))
# print(posResult)
for i in range(0,len(posCount)):
    priorProbPos[wordCheck[i]] = posResult[i]/fileCount
print(priorProbPos)
    
negCount = [0,0,0,0,0,0,0,0]
negResult = [0,0,0,0,0,0,0,0]
wCount = 0    
fileCount = 0
path = r"C:\Users\Leaf\Downloads\txt_sentoken\neg"
os.chdir(path) 
  
# for txt in os.listdir(): 
for filename in os.scandir(path):
    if filename.is_file():
#         print(filename.path
        fileCount +=1
#         file_path = f"{path}\{txt}"

        f = open(filename.path, "r")
    #     print(f.read()) 
        for line in f:
            for word in line.split():
                if word.isalpha():
                    wCount += 1
                if (word.lower() == "awful"):
                    negCount[0] =1
                elif (word.lower() == "bad"):
                    negCount[1] =1
                elif (word.lower() == "boring"):
                    negCount[2] =1
                elif (word.lower() == "dull"):
                    negCount[3] =1
                elif (word.lower() == "effective"):
                    negCount[4] =1
                elif (word.lower() == "enjoyable"):
                    negCount[5] =1
                elif (word.lower() == "great"):
                    negCount[6] =1
                elif (word.lower() == "hilarious"):
                    negCount[7] =1
        

        for i in range(len(negCount)):
            negResult[i] += negCount[i]
        negCount = [0,0,0,0,0,0,0,0]

        f.close()
print("\n")
print("negative")
# print("word count: " + wordCheck)
# print("file count: " + negCount)
print("word count: "+ str(wCount))
print("file count: " + str(fileCount))
# print(negResult)
for i in range(0,len(negCount)):
    priorProbNeg[wordCheck[i]] = negResult[i]/fileCount
print(priorProbNeg)


def calprob(text):
    negProb = 1.0
    posProb = 1.0
    negCount = [0,0,0,0,0,0,0,0]
    for word in text.split():
        if (word.isalpha() and word in priorProbPos):
            if word.isalpha():
                if (word.lower() == "awful"):
                    negCount[0] =1
                elif (word.lower() == "bad"):
                    negCount[1] =1
                elif (word.lower() == "boring"):
                    negCount[2] =1
                elif (word.lower() == "dull"):
                    negCount[3] =1
                elif (word.lower() == "effective"):
                    negCount[4] =1
                elif (word.lower() == "enjoyable"):
                    negCount[5] =1
                elif (word.lower() == "great"):
                    negCount[6] =1
                elif (word.lower() == "hilarious"):
                    negCount[7] =1
                
    for i in range(len(negCount)):
        if (negCount[i] == 0):
            prob = 1 - priorProbNeg[wordCheck[i]]
        else:
            prob = priorProbNeg[wordCheck[i]]
        negProb *= prob

    for i in range(len(negCount)):
        if (negCount[i] == 0):
            prob = 1 - priorProbPos[wordCheck[i]]
        else:
            prob = priorProbPos[wordCheck[i]]
        posProb *= prob
    
    return negProb, posProb

def predict(text): 
    neg, pos = calprob(text)
    if (neg > pos):
        return 'Negative'
    else:
        return 'Positive'
    
print("\nQ7")
    
text1 = "as with most of the effective courtroom dramas , the cinematography is crisp and rich ."    
print(text1)
print("negative prob, positive prob")
print(calprob(text1))
print(predict(text1))

text2 = "shao khan has decided that he's going to take over the earth * anyways * , and to hell with some silly rule about mortals winning the tournament . \
thereafter follows approximately 85 minutes of film that alternates between being confused , being trite , being silly , and being just plain stupid . \
one gets the general impression that the producers of the movie thought hey , that last movie was such a success that we can get more money and make a * real * movie now . too bad they didn't simply stick with the formula from the first movie . i could write volumes about the things that are wrong with this picture , but here are the high points : * the acting is truly bad ."
print(text2)
print("negative prob, positive prob")
print(calprob(text2))
print(predict(text2))


path = r"C:\Users\Leaf\Downloads\txt_sentoken\pos"


def predict_set(path, ground_truth_label): 
    os.chdir(path) 
    score = 0 
    listScore = [0,0]
#     for r in test_set: 
    for filename in os.scandir(path):
        if filename.is_file():
#             print(filename.path)
            f = open(filename.path, "r")
            line = f.read()
            if predict(line) == ground_truth_label: 
                score += 1
                listScore.append(1)
            else:
                listScore.append(0) 
    # convert to percentage 
            f.close()
    score = score / 10.0 
    return score, listScore

truePos, listPos = predict_set(r"C:\Users\Leaf\Downloads\txt_sentoken\pos", 'Positive')
trueNeg, listNeg = predict_set(r"C:\Users\Leaf\Downloads\txt_sentoken\neg", 'Negative')

print("\nQ8")
print("Positive accuracy% = ", truePos)
print("Negative accuracy% = ", trueNeg)

# print("confusion matrix")
# print( str(truePos) + " | " + str(100-trueNeg))
# print("---------")
# print("{:.1f}".format(100.0-truePos) + " | " + str(trueNeg))

for i in range(len(listNeg)):
    listNeg[i] = abs(listNeg[i]-1)
trueList = [1]*1002 + [0]*1002
l = listPos + listNeg

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import classification_report

print(classification_report(trueList, l))
color = 'white'
cmSVM = confusion_matrix(trueList, l)
disp = ConfusionMatrixDisplay(cmSVM, display_labels=['negative', 'positive'])
disp.plot()
plt.xticks(rotation=45, ha='right')
plt.show()
print('')