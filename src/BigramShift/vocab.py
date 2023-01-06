import ssfAPI as ssf
from argparse import ArgumentParser
from re import search
from sys import argv
import os
import random
import pandas as pd

def find_file_list(folder_path):
    """Find file list inside a folder."""
    file_list = ssf.folderWalk(folder_path)
    return file_list


def extract_raw_sentences(file_path):
    """Extract raw sentences from a dependency annotated file."""
    ssf_document = ssf.Document(file_path)
    raw_sentences = []
    for sentence in ssf_document.nodeList:
        raw_sentences.append(sentence.generateSentence())
    return raw_sentences


def getTotalCorpus(inp):
    sentences = []
    if not os.path.isdir(inp):
        raw_sentences = extract_raw_sentences(inp)
        for item in raw_sentences:
            sentences.append(item)

    else:
        file_list = find_file_list(inp)
        for fl in file_list:
            raw_sentences = extract_raw_sentences(fl)
            for item in raw_sentences:
                sentences.append(item)

    
    return sentences

def write_lines_to_file(lines, file_path):
    with open(file_path, 'w', encoding='utf-8') as file_write:
        file_write.write('\n'.join(lines))

def main():
    parser = ArgumentParser(description="This is a program for extracting raw sentences from dependency annotated treebanks.")
    parser.add_argument('-i', dest='inp')
    parser.add_argument('-o', dest='out')
    args = parser.parse_args()

    BShift = []
    sentences = getTotalCorpus(args.inp)
    vocabulary = {}
    data = ""
    for item in sentences:
        data += item
        data += " "
    vocab = []
    for sentence in sentences:
        for item in sentence.split(" "):
            vocab.append(item)
    vocab = list(set(vocab))
    with open("vocab.txt", "w") as f:
        for item in vocab:
            f.write(item)
            f.write("\t")
            f.write(str(data.count(item)))
            vocabulary.update({item:data.count(item)})
            f.write("\n")
        f.close()
    vocabulary = dict(sorted(vocabulary.items(), key=lambda item: item[1]))
    shifted_sentences = []
    print("vocabulary done")
    print(vocabulary)
    for sentence in sentences:
        temp = random.randint(0,10)
        try:
            if(len(sentence)>=4):
                if temp <= 2:
                    sentence = sentence.split(" ")
                    b = random.randint(0,len(sentence)-2)

                    tmp = sentence[b]
                    sentence[b] = sentence[b+1]
                    sentence[b+1] = tmp

                    sentence = " ".join(sentence)
                    BShift.append(1)
                    shifted_sentences.append(sentence)
                else:
                    BShift.append(0)
                    shifted_sentences.append(sentence)
            else:
                BShift.append(0)
                shifted_sentences.append(sentence)
        except:
            BShift.append(0)
            shifted_sentences.append(sentence)

    d = {"BShift":BShift,"sentences":shifted_sentences}
    df = pd.DataFrame(d)
    df.to_csv(args.out,index=False)

    df1 = pd.read_csv("../gold/kannada/bshift.csv")
    with open("../gold/kannada/shifted_sentences.txt", "w") as f:
        for item in df1["sentences"]:
            f.write(item)
            f.write("\n")
        f.close()



if __name__ == '__main__':
    main()
