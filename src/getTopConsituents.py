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

def getTopConstituents(sentence):
    tc = []
    for chunknode in sentence.nodeList:
        if chunknode.parentRelation  == "root":
            for node in chunknode.nodeList:
                tc.append(node.name)
    return tc

    # root_name = ""
    # root_relation = ""
    # for chunknode in sentence.nodeList:
    #     if(chunknode.parent == "root"):
    #         root_relation = chunknode.


def main():
    parser = ArgumentParser()
    parser.add_argument('-i', dest='inp')
    parser.add_argument('-o', dest='out')
    args = parser.parse_args()
    sentences_with_tc = []
    if not os.path.isdir(args.inp):
        ssf_doc = ssf.Document(args.inp)
        for sentence in ssf_doc.nodeList[0:1]:
            sentences_with_tc.append(str(",".join(getTopConstituents(sentence))))
    else:
        file_list = find_file_list(args.inp)
        sentences_with_tc = []
        for file in file_list:
            ssf_document = ssf.Document(file)
            for sentence in ssf_document.nodeList:
                sentences_with_tc.append(str(",".join(getTopConstituents(sentence))))
    write_lines_to_file(sentences_with_tc, args.out)

if __name__  == '__main__':
    main()