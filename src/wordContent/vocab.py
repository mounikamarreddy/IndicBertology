import ssfAPI as ssf
from argparse import ArgumentParser
from re import search
from sys import argv
import os


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
    wordContent = []
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

    sampled_words = []
    for item in vocabulary.keys():
        if vocabulary[item] > 100 and vocabulary[item] < 200:
            sampled_words.append(item)
    
    print(len(sampled_words))

    for word in sampled_words:
        count  = 0
        for sentence in sentences:
            if sentence.count(word) == 1 and count <= 2:
                count += 1
                wordContent.append(word+"---------"+sentence)
    
    write_lines_to_file(wordContent, "wordContent.txt")


if __name__ == '__main__':
    main()
