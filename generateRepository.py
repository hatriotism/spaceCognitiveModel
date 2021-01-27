from config import *

outputFolder = 'knowledgeRepository/'

# clustersCopy = anonym.copy()
# for word in clustersCopy:
#     anonym[anonym[word]] = word

def generalExtractStrategy(target, ghost, candidates):
    got = False
    for candidate in ghost:
        searchLength = len(target)
        while searchLength >= 1 and not got:
            if len(candidate) == searchLength: # 其次长度一致
                candidates = candidates | {candidate}
                got = True
                break
            else:
                searchLength -= 1
    else:
        if not got:
            candidates = candidates | {ghost[0]} # 最次取第一个词
    return candidates

for clusterList in clusterLists:
    for synonym in clusterList:
        for target in synonym:
            candidates = set()
            for ghost in clusterList:
                if target not in ghost:
                    got = False
                    for prefix in allPrefixes:
                        if prefix == target[:1] or prefix == target[:2]: # 如果有前缀
                            for candidate in ghost:
                                if candidate[0] == target[0]: # 优先要求前缀一致
                                    candidates = candidates | {candidate}
                                    got = True
                                    break
                            else:
                                candidates = generalExtractStrategy(target, ghost, candidates) # 其次采用通用策略
                                got = True
                                break
                    for suffix in allSuffixes:
                        if suffix == target[-1:] or suffix == target[-2:]: # 如果有后缀
                            for candidate in ghost:
                                if candidate[-1] == target[-1]: # 优先要求后缀一致
                                    candidates = candidates | {candidate}
                                    got = True
                                    break
                            else:
                                candidates = generalExtractStrategy(target, ghost, candidates) # 其次采用通用策略
                                got = True
                                break
                    if not got:
                        candidates = generalExtractStrategy(target, ghost, candidates)
                        got = True
                        
            if target not in anonym:
                anonym[target] = candidates
            else:
                anonym[target] = anonym[target] | candidates
for target in anonym:
    anonym[target] = list(anonym[target])


with open(outputFolder + "Anonym.json", "w", encoding='utf-8') as f:
    json.dump(anonym, f, indent=2, sort_keys=True, ensure_ascii=False)

# with open("synonym.json", "w", encoding='utf-8') as f:
#     json.dump(clusterLists, f, indent=2, sort_keys=True, ensure_ascii=False)

with open(outputFolder + "SpaceCognitiveModels.json", "w", encoding='utf-8') as f:
    json.dump(clusterLists, f, indent=2, sort_keys=True, ensure_ascii=False)

with open(outputFolder + "SpaceLexicon.txt", "w", encoding='utf-8') as f:
    for words in list(anonym.keys()):
        if len(words) > 1:
            f.write(f"{words}\n")

with open(outputFolder + "SpaceLexicon.json", "w", encoding='utf-8') as f:      
    json.dump(list(anonym.keys()), f, indent=2, sort_keys=True, ensure_ascii=False)