from transformers import BertTokenizer
import pickle

def get_values(file,vocab_dict):
    """
    get label context and response.
    :param file: filel name
    :param get_c_d:
    :return:
    """
    data = open(file, 'r').readlines()
    data = [sent.split('\n')[0].split('\t') for sent in data]
    #data=data[:10000]
    y = [int(a[0]) for a in data]
   # for a in data:
    #    print(a[1:-1])
     #   print(' __EOS__ '.join(a[1:-1]))
    #print(tokenizer.convert_tokens_to_ids(tokenizer.tokenize("tt")))
    cr = [ [sen.split() for sen in a[1:]] for a in data]

    i = 0
    for set in cr:
        for sen in set:
            for word in sen:
                if word not in vocab_dict:
                    vocab_dict[word] = i
                    i += 1
    return vocab_dict

if __name__ == '__main__':
    #load the vocab file

    train, test, valid = {}, {}, {}
    vocab_dict={}
    vocab_dict=get_values('ubuntu_data/train.txt',vocab_dict)
    vocab_dict = get_values('ubuntu_data/valid.txt', vocab_dict)
    vocab_dict = get_values('ubuntu_data/test.txt', vocab_dict)
    pickle.dump(vocab_dict, file=open("ubuntu_data/whole_vocab.pkl", 'wb'))

    #test['y'], test['cr']= get_values('ubuntu_data/test.txt',tokenizer=bert_tokenizer)
    #valid['y'], valid['cr']= get_values('ubuntu_data/valid.txt',tokenizer=bert_tokenizer)
    #char_vocab = defaultdict(float)
    dataset = train, valid, test
    #pickle.dump(dataset, open('ubuntu_data/dataset_1M.pkl', 'wb'))