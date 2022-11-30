import ssfAPI as ssf
from argparse import ArgumentParser
from re import search
from sys import argc
import os

def find_file_list(folder_path):
    """Find file list inside a folder."""
    file_list = ssf.folderWalk(folder_path)
    return file_list


def write_lines_to_file(lines, file_path):
    """Write lines to a file."""
    with open(file_path, 'w', encoding='utf-8') as file_write:
        file_write.write('\n'.join(lines))

def getTense(sentence):
    return "PRESENT"

def main():
    parser = ArgumentParser()
    parser.add_argument('-i',dest='inp')
    parser.add_argument('-o',dest='out')
    args = parser.parse_args()

    sentences_with_tense = []

    if not os.path.isdir(args.inp):
        ssf_doc = ssf.Document(args.inp)
        for sentence in ssf_doc.nodeList:
            sentences_with_tense.append(getTense(sentence)+"--"+sentence.generateSentence())
    else:
        file_list = find_file_list(args.inp)
        for file in file_list:
            ssf_doc = ssf.Document(file)
            for sentence in ssf_doc.nodeList:
                sentences_with_tense.append(getTense(sentence)+"--"+sentence.generateSentence())
    
    write_lines_to_file(sentences_with_tense, args.out)


if __name__ == '__main__':
    main()
