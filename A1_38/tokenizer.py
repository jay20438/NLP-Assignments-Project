from collections import defaultdict


def calcFreq(filePath):
    result = defaultdict(int)
    with open(filePath, 'r') as inputFile:
        for inpLine in inputFile:
            curWords = inpLine.split()
            for word in curWords:
                word = word + "$"
                result[word] = result[word] + 1
    return result


def allSubstrMethod(wordFrequencies):
    allSubstrFreq = defaultdict(int)
    for word in wordFrequencies:
        wordLen = len(word)
        for index in range(wordLen-1):
            for subIndex in range(index+1, wordLen):
                intWord = word[index:subIndex+1]
                allSubstrFreq[intWord] += wordFrequencies[word]
    
    return allSubstrFreq


def initializeTPF(wordFrequencies):
    tokenPairFrequency = defaultdict(int)
    for word in wordFrequencies.keys():
        reqLen = len(word)
        for index in range(reqLen-1):
            tokenPairFrequency[f"{word[index]}-{word[index+1]}"] += wordFrequencies[word]
    
    return tokenPairFrequency


def performMerge(allSubstrFreq, vocab, tokPairFreq, mergeRules):

    maxTokenPair = max(tokPairFreq, key=tokPairFreq.get)
    splitTokens = maxTokenPair.split('-')
    mergedToken = splitTokens[0]+splitTokens[1]
    vocab.append(mergedToken)
    mergeRules.append(f"{splitTokens[0]}, {splitTokens[1]}")

    # Till this point, the newly merged token has been added to the list, along with the merge rule.
    # Now, for all previous tokens, combine to form a string, check and update freq.

    refList = vocab[:-1] # Excludes recently added new token
    newestToken = vocab[-1]
    for option in refList:
        trial1 = newestToken + option
        trial2 = option + newestToken
        
        tokPairFreq[f"{newestToken}-{option}"] += allSubstrFreq[trial1]
        tokPairFreq[f"{option}-{newestToken}"] += allSubstrFreq[trial2]

    # Merge rule, vocab updated. TokPairFreq frequency also updated with all previous tokens.
    # Since this token has been merged and added, set its frequency to 0.
    tokPairFreq[maxTokenPair] = 0


def tokenize_word(word, vocab):
    wordTok = []
    index = 0
    while index<len(word):
        isPresent = False
        tokLen = 0
        maxLenToken = ""
        for token in vocab:
            if(word[index:index+len(token)]==token and len(token)>tokLen):
                tokLen = len(token)
                maxLenToken = token
                isPresent = True
        
        if isPresent:
            wordTok.append(maxLenToken)
            index += len(maxLenToken)
        # Adding single char as token
        else:
            wordTok.append(word[index])
            index += 1
    # Final list of token in words....
    return wordTok


def writeToFile(pathOfFile, listWrite):
    with open(pathOfFile, 'w') as curFile:
        for obj in listWrite:
            curFile.write(str(obj) + '\n')


class Tokenizer:
    # Class constructor to initialize attributes.
    def __init__(self, filePath):
        self.corpus = filePath   # File path to 'corpus.txt'
        self.wordFrequencies = calcFreq(filePath)   # Frequency count of each word
        self.allSubstrFreq = allSubstrMethod(self.wordFrequencies)  # Frequency count of all possible substrings in corpus.
        self.vocabulary = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '$']
        self.tokenPairFrequency = initializeTPF(self.wordFrequencies)
        self.mergeRules = []
        self.uniqueVocabulary = []


    def learn_vocabulary(self, numMerges):
        # Running numMerges number of iterations.
        for _ in range(numMerges):
            performMerge(self.allSubstrFreq, self.vocabulary, self.tokenPairFrequency, self.mergeRules)

        # Till this point, the vocabulary and merge rules have been learnt.
        uniqueTokens = []
        tokenSet = set()
        for token in self.vocabulary:
            if token not in tokenSet:
                uniqueTokens.append(token)
                tokenSet.add(token)
        
        self.uniqueVocabulary = uniqueTokens
        # Prepared a separate list of unique tokens.
        # Now, we will write these to output text files.
        tokenFilePath = "tokens.txt"
        mergeRuleFilePath = "merge_rules.txt"
        tokenUniqueFilePath = "tokens_unique.txt"
        # Calling the required function.
        writeToFile(tokenFilePath, self.vocabulary)
        writeToFile(mergeRuleFilePath, self.mergeRules)
        writeToFile(tokenUniqueFilePath, self.uniqueVocabulary)
    

    def tokenize(self, sentences):
        if len(sentences)<=0:
            print("No sample sentence provided.")
            return
        
        # Assuming sentences to be a list of sentences
        totalResult = []
        for sentence in sentences:
            senWords = sentence.split()
            senTokens = []   # Elements of this to be printed on a single line.
            for senWord in senWords:
                tempList = tokenize_word(senWord, self.uniqueVocabulary)
                for ele in tempList:
                    senTokens.append(ele)

            totalResult.append(senTokens)
        
        # Tokens obtained and stored in senTokens list...
        tokenizeResultPath = "tokenized_samples.txt"
        with open(tokenizeResultPath, 'w') as outpFile:
            for ele in totalResult:
                content = ",".join(ele)
                outpFile.write(str(content) + '\n')



