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


def write_lines_to_file(lines, file_path):
    """Write lines to a file."""
    with open(file_path, 'w', encoding='utf-8') as file_write:
        file_write.write('\n'.join(lines))

def getDepth(sentence):
    for chunknode in sentence.nodeList:
        sentence.addEdge(chunknode.parent, chunknode.name)
    namedict = {}
    namedict.update({"0":0})
    for key in sentence.edges:
        for item in sentence.edges[key]:
            if item not in namedict.keys():
                namedict.update({item:0})
    queue = []
    queue.append(sentence.edges["0"][0])
    namedict[str(sentence.edges["0"][0])] += 1 
    while(queue != []):
        popped = queue.pop(0)
        if popped in sentence.edges.keys():
            for item in sentence.edges[str(popped)]:
                queue.append(item)
                namedict[item] = namedict[popped]+1
    return max(namedict.values())
    

def main():
    parser = ArgumentParser()
    depth = []
    sentences = []
    parser.add_argument('-i', dest='inp')
    parser.add_argument('-o',dest='out')
    args = parser.parse_args()
    sentences_with_tc = []
    if not os.path.isdir(args.inp):
        ssf_doc = ssf.Document(args.inp)
        for sentence in ssf_doc.nodeList:
            try:
                # sentences_with_tc.append(str(getDepth(sentence))+"-"+sentence.generateSentence())
                depth.append(getDepth(sentence))
                sentences.append(sentence.generateSentence())
            except:
            #    sentences_with_tc.append("0"+"-"+sentence.generateSentence())
                depth.append(0)
                sentences.append(sentence.generateSentence())
 
    else:
        file_list = find_file_list(args.inp)
        sentences_with_tc = []
        for file in file_list:
            ssf_document = ssf.Document(file)
            for sentence in ssf_document.nodeList:
                try:
                    # sentences_with_tc.append(str(getDepth(sentence))+"-"+sentence.generateSentence())
                    depth.append(getDepth(sentence))
                    sentences.append(sentence.generateSentence())
                except:
                    # sentences_with_tc.append("0"+"-"+sentence.generateSentence())
                    depth.append(0)
                    sentences.append(sentence.generateSentence())
    # write_lines_to_file(sentences_with_tc, args.out)
    d = {"depth":depth,"sentences":sentences}
    df = pd.DataFrame(d)
    df.to_csv(args.out,index=False)

if __name__  == '__main__':
    main()