import ssfAPI as ssf
from argparse import ArgumentParser
from re import search
from sys import argv
import os
import random

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


def getTotalCorpus():
    parser = ArgumentParser(description="This is a program for extracting raw sentences from dependency annotated treebanks.")
    parser.add_argument('-i', dest='inp')
    args = parser.parse_args()
    sentences = []
    if not os.path.isdir(args.inp):
        raw_sentences = extract_raw_sentences(args.inp)
        for item in raw_sentences:
            sentences.append(item)

    else:
        file_list = find_file_list(args.inp)
        for fl in file_list:
            raw_sentences = extract_raw_sentences(fl)
            for item in raw_sentences:
                sentences.append(item)

    
    return sentences

def write_lines_to_file(lines, file_path):
    with open(file_path, 'w', encoding='utf-8') as file_write:
        file_write.write('\n'.join(lines))

def main():
    BShift = []
    sentences = getTotalCorpus()
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

    for sentence in sentences:
        temp = random.randint(0,10)
        if temp <= 2:
            sentence = sentence.split(" ")
            b = random.randint(0,len(sentence)-1)
            c = random.randint(0,len(sentence)-1)
            while c == b :
                c = random.randint(0,len(sentence)-1)

            tmp = sentence[b]
            sentence[b] = sentence[c]
            sentence[c] = tmp
            sentence = " ".join(sentence)
            BShift.append("I"+"---"+sentence)
            print(sentence)
        elif temp >= 8:
            BShift.append("O"+"---"+sentence)

    
    write_lines_to_file(BShift, "BShift.txt")


if __name__ == '__main__':
    main()
