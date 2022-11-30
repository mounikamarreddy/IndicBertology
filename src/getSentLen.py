import os
from sys import orig_argv
from re import search
from argparse import ArgumentParser
import ssfAPI as ssf

def find_file_list(folder_path):
    """Find file list inside a folder."""
    file_list = ssf.folderWalk(folder_path)
    return file_list


def write_lines_to_file(lines, file_path):
    """Write lines to a file."""
    with open(file_path, 'w', encoding='utf-8') as file_write:
        file_write.write('\n'.join(lines))

def getlen(sentence):
    str_temp = sentence.generateSentence()
    return len(str_temp.split(" "))

def main():
    parser = ArgumentParser()
    parser.add_argument('-i', dest='inp', help='Enter the input folder or file for which object number should be extracted.')
    parser.add_argument('-o', dest='out', help='Enter the output file to which object number info will be written to.')
    args = parser.parse_args()
    sentences_with_length = []
    if not os.path.isdir(args.inp):
        ssf_doc = ssf.Document(args.inp)
        for sentence in ssf_doc.nodeList:
            sentences_with_length.append(str(getlen(sentence))+"--"+sentence.generateSentence())
    else:
        file_list = find_file_list(args.inp)
        for file in file_list:
            ssf_doc = ssf.Document(file)
            for sentence in ssf_doc.nodeList:
                sentences_with_length.append(str(getlen(sentence))+"--"+sentence.generateSentence())


    write_lines_to_file(sentences_with_length,args.out)


if __name__ == '__main__':
    main()