import os
import xml.etree.ElementTree
from text_parser import TextParser

def parse_dataset(input_dir, output_file):
    dirs = get_immediate_subdirectories(input_dir)
    open(output_file, 'w').close()
    counter = 1
    n_files = 0
    for d in dirs:
        print 'Parse dir: ' + d + '; ' + str(counter) + '/' + str(len(dirs))
        docs = parse_one_dir(d)
        append_to_file(output_file, docs)
        counter += 1
        n_files += len(docs)
        print 'Done dir: ' + d + '; File count:' + str(n_files)

def get_immediate_subdirectories(a_dir):
    return [os.path.join(a_dir, name) + '/' for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def get_immediate_files(a_dir):
    files = [os.path.join(a_dir, name) for name in os.listdir(a_dir)
            if os.path.isfile(os.path.join(a_dir, name))]
    return [f for f in files if f.endswith('.xml')]

def parse_one_dir(data_dir):
    files = get_immediate_files(data_dir)
    print 'Number of files in dir: ' + str(len(files))
    # print files
    docs = []
    # for f in files[:1]:
    for f in files:
        doc = parse_one_file(f)
        print 'File done: ' + doc[0]
        docs.append(doc)
    return docs

def parse_one_file(xml_file):
    doc_id = get_doc_id(xml_file)
    text = parse_xml(xml_file)
    tokens = tokenize(text)
    return (doc_id, tokens)

def get_doc_id(xml_file):
    item = xml_file.split('/')[-1]
    return item.rstrip('newsML.xml')

def parse_xml(xml_file):
    e = xml.etree.ElementTree.parse(xml_file).getroot()
    text = ''
    try:
        for atype in e.findall('headline'):
            text += atype.text
    except:
        pass
    text += ' '
    try:
        for atype in e.findall('text'):
            for p in atype:
                text += p.text
    except:
        pass
    return text

def tokenize(text):
    # print text
    tokenizer = TextParser(stopword_file = 'stopwords.txt')
    # tokens = tokenizer.parse_words(text)
    tokens = tokenizer.parse_words(text, stem=False)
    return tokens

def append_to_file(output_file, docs):
    with open(output_file, 'a') as fp:
        for doc in docs:
            doc_id, tokens = doc[0], doc[1]
            s = doc_id + ' ' + ' '.join(tokens)
            fp.write(s + '\n')

if __name__ == '__main__':
    # input_dir = '/Users/chao/data/source/rcv1/sample/'
    # output_file = '/Users/chao/data/projects/hierarchical-classification/rcv1/sample/docs.txt'
    input_dir = '/shared/data/yuningm2/datasets/rcv1/'
    output_file = '/shared/data/czhang82/projects/hierarchical_classification/rcv1/docs-nostem.txt'
    parse_dataset(input_dir, output_file)

