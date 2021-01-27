import os
import json
# import word2vec
# word2vecModel = word2vec.load('vec/corpusWord2Vec_skimgram.bin')
# from gensim.models import word2vec
# word2vecModel = word2vec.Word2vec.load('vec/newWord2vec')
import pkuseg
seg = pkuseg.pkuseg(postag=True, user_dict = "knowledgeRepository/SpaceLexicon.txt") 

from config import *

inputFolder = 'rawdata/'
outputFolder = 'outputs/'

result = []

with open("knowledgeRepository/SpaceLexicon.json", encoding="utf-8") as f:
  words = json.load(f)

def cosine(word, n):
    ls =[]
    try:
        a = word2vecModel.cosine(word, n)
        for i in range(n):
            ls.append(word2vecModel.vocab[a[0][i]])
    except KeyError:
        pass
    return ls

def getPOS(word):
    return seg.cut(word)[0][1]

def fromCuted(line):
    outputFileName = 'fromCuted.txt'
    foundCount = 0
    foundIndex = []
    entityIndex = []
    entityWords = set()
    moreEntityWords = set()
    # line = line.replace('<content>', '').replace('</content>', '')
    line = line.strip()
    if line:
        lineCuted = seg.cut(line)
        if len(lineCuted) > 6:
            with open(outputFolder + outputFileName, "a", encoding='utf-8') as f:
                for (index, word) in enumerate(lineCuted):
                    token = word[0]
                    pos = word[1]
                    if token in words and word not in stopWords and pos not in stopPos:
                        if pos in scoreMap:
                            foundCount += scoreMap[pos]
                        else:
                            foundCount += 1
                        foundIndex.append(index)
                    if pos in entityPos:
                        entityIndex.append(index)
                        entityWords = entityWords | {token}
                        # moreEntityWordsList = cosine(token, 1)
                        # for entity in moreEntityWordsList:
                        #     if getPOS(entity) in entityPos:
                        #         moreEntityWords = moreEntityWords | {entity}
                        #         break

                foundFre = round(foundCount / len(lineCuted), 3)
                entityCount = len(entityWords)
                # print(entityCount, foundCount, foundFre)
                if entityCount >= 3 and foundCount >= 15 and foundFre >= 0.3:
                    f.write(f"{line}\n#{lineCuted}\n##{foundFre}\n###")
                    for index in foundIndex:
                        f.write(f"{lineCuted[index][0]} ")
                    f.write(f"\n####{entityWords}")
                    f.write("\n\n")

                    result.append({
                        'line': line,   # 原句 
                        'lineCuted': lineCuted, # 分词后 
                        'foundFre': foundFre,   # 方位词语的密度
                        'foundIndex': foundIndex,   # 方位词语的索引
                        'foundWords': [lineCuted[index] for index in foundIndex],   # 具体的方位词语集合
                        'entityIndex': entityIndex, # 句中实体词的索引
                        'entityWords': list(entityWords),   # 句中具体的实体词集合
                        'moreEntityWords': list(moreEntityWords),   # 更多的实体词
                    })
                    
# def fromRaw(line):
#     outputFileName = 'fromRaw.txt'
#     count = 0
#     foundIndex = []
#     # line = line.replace('<content>', '').replace('</content>', '')
#     line = line.strip()
#     if line and len(line) > 12:
#         with open(outputFileName,"a") as f:
#             for word in line:
#                 if word in characters:
#                     count += 1
#                     foundIndex.append(word)
#                 # elif word in oneScore:
#                 #     count += 1
#             if count / len(line) >= 0.3 or count >= 6:
#                 f.write(f"{line}\n###{foundIndex}\n\n")

for root, dirs, files in os.walk(inputFolder):
    for fileName in files:
        try:
            with open(inputFolder + fileName, 'r', encoding='gb18030') as file:
                for line in file.readlines():
                    fromCuted(line)
                    # fromRaw(line)
        except UnicodeDecodeError:
            try:
                with open(inputFolder + fileName, 'r') as file:
                    for line in file.readlines():
                        fromCuted(line)
                        # fromRaw(line)
            except UnicodeDecodeError:
                print(fileName)

with open(outputFolder + 'extracted.json', "w", encoding='utf-8') as f:
    json.dump(result, f, indent=2, sort_keys=True, ensure_ascii=False)