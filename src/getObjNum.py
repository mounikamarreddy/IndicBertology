"""Find object number from dependency trees for main clause."""
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


def find_object_number_from_sentence(sentence):
    """Find object number from a sentence."""
    main_verb = '0'
    object_parent = ''
    object_token = ''
    object_pos = ''
    # every sentence consists of chunks
    for chunk_node in sentence.nodeList:
        if chunk_node.parentRelation == 'k2' and search('^NP\d+', str(chunk_node.name)):
            # k1 relation is similar dobj in universal dependencies
            object_parent = chunk_node.parent
            object_number = ''
            # every chunks consists of tokens
            for node in chunk_node.nodeList:
                if node.type == 'N_NN' and not search('^NULL', node.lex):
                    # N_NN pos tag is for common noun, can also consider N_NNP for proper noun
                    morph_feats = node.getAttribute('af')
                    # af attributes consists of 8 fields, 4th field is number feature
                    if morph_feats:
                        object_number = morph_feats.split(',')[3]
                        object_token = node.lex
                        object_pos = node.type
        elif chunk_node.name == object_parent and chunk_node.parent == main_verb:
            if object_token:
                # if the number of the object is missing, then ignore it
                return object_number
    return None


def main():
    count = 0
    objnum = []
    sentences = []
    """Pass arguments and call functions here."""
    # this program runs on both folder and file level.
    parser = ArgumentParser(description="This is a program for finding the object number from dependency annotated treebanks.")
    parser.add_argument('-i', dest='inp', help='Enter the input folder or file for which object number should be extracted.')
    args = parser.parse_args()
    if not os.path.isdir(args.inp):
    # Create a document object for an SSF annotated file
        ssf_document = ssf.Document(args.inp)
        object_with_number_and_sentences = []
        for sentence in ssf_document.nodeList:
            # object_with_number_and_sentence = find_object_number_from_sentence(sentence)
            # if object_with_number_and_sentence:
                # object_with_number_and_sentences.append(object_with_number_and_sentence)
            objnum.append(find_object_number_from_sentence(sentence))
            sentences.append(sentence.generateSentence())
    else:
        file_list = find_file_list(args.inp)
        object_with_number_and_sentences = []
        for fl in file_list:
            ssf_document = ssf.Document(fl)
            for sentence in ssf_document.nodeList:
                count += 1
                # object_with_number_and_sentence = find_object_number_from_sentence(sentence)
                # if object_with_number_and_sentence:
                    # object_with_number_and_sentences.append(object_with_number_and_sentence)
                objnum.append(find_object_number_from_sentence(sentence))
                sentences.append(str(sentence.generateSentence()))
                
                # print(object_with_number_and_sentences)

    # write_lines_to_file(object_with_number_and_sentences, args.out)
    d = {"objnum":objnum,"sentences":sentences}
    df = pd.DataFrame(d)
    df.to_csv("./gold/urdu/objnum.csv",index=False)



if __name__ == '__main__':
    main()
