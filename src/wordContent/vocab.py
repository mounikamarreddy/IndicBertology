import ssfAPI as ssf
from argparse import ArgumentParser
from re import search
from sys import argv
import os
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
    parser.add_argument('-o',dest='out')
    args = parser.parse_args()

    wordContent = []
    sent = []
    sentences = getTotalCorpus(args.inp)
    vocabulary = {}
    data = ""

    for item in sentences:
        data += item
        data += " "
    data = data.split(" ")
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
    # print(vocabulary)


    sampled_words = []
    for item in vocabulary.keys():
        if vocabulary[item] > 25 and vocabulary[item] < 100:
            sampled_words.append(item)

    for word in sampled_words:
        count  = 0
        for sentence in sentences:
            if sentence.count(word) == 1 and count <= 5:
                count += 1
                wordContent.append(word)
                sent.append(sentence)

    
    # write_lines_to_file(wordContent, "wordContent.txt")
    d = {"WordContent":wordContent,"sentences":sent}
    df = pd.DataFrame(d)
    df.to_csv(args.out,index=False)


if __name__ == '__main__':
    main()
