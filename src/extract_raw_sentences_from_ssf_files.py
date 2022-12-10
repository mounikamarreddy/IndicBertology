"""Extract raw sentences from dependency treebanks."""
import ssfAPI as ssf
from argparse import ArgumentParser
from re import search
from sys import argv
import os


def find_file_list(folder_path):
    """Find file list inside a folder."""
    file_list = ssf.folderWalk(folder_path)
    return file_list


def write_lines_to_file(lines, file_path):
    """Write lines to a file."""
    with open(file_path, 'w', encoding='utf-8') as file_write:
        file_write.write('\n'.join(lines))


def extract_raw_sentences(file_path):
    """Extract raw sentences from a dependency annotated file."""
    ssf_document = ssf.Document(file_path)
    raw_sentences = []
    for sentence in ssf_document.nodeList:
        raw_sentences.append(sentence.generateSentence())
    return raw_sentences


def main():
    parser = ArgumentParser(description="This is a program for extracting raw sentences from dependency annotated treebanks.")
    parser.add_argument('-i', dest='inp', help='Enter the input folder of treebank files.')
    parser.add_argument('-o', dest='out', help='Enter the output folder where raw sentences will be written to.')
    args = parser.parse_args()
    sentences_final = []
    if not os.path.isdir(args.inp):
        raw_sentences = extract_raw_sentences(args.inp)
        for item in raw_sentences:
            sentences_final.append(item)

    else:
        file_list = find_file_list(args.inp)
        for fl in file_list:
            raw_sentences = extract_raw_sentences(fl)
            for item in raw_sentences:
                sentences_final.append(item)

    write_lines_to_file(sentences_final, args.out)


if __name__ == '__main__':
    main()
