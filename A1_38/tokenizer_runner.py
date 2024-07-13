from tokenizer import Tokenizer

tokenizeObj = Tokenizer("corpus.txt")
tokenizeObj.learn_vocabulary(500)
print("Learnt the Corpus Vocabulary")

sampleInputs = ["the feel lucky", "eeel$ and from", "my name is anthony gonsalves"]
tokenizeObj.tokenize(sampleInputs)

print("Tokenized the sentences")