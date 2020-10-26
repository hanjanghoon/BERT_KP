import numpy as np
import pickle
def get_values(file):
    """
    get label context and response.
    :param file: filel name
    :param get_c_d:
    :return:
    """
    data = open(file, 'r').readlines()
    data = [sent.split('\n')[0].split('\t') for sent in data]
    cr = ["\n".join([sen for sen in a[1:]]) for a in data]
    return cr

def get_evidence_values(file, tokenizer=None):
    """
    get label context and response.
    :param file: filel name
    :param get_c_d:
    :return:
    """
    data = open(file, 'r').read()
    data=data.split('\n\n')[:-1]
    data = [sent.split('\n') for sent in data]
    #data=data[:10000]
    evi = [ [sen for sen in a] for a in data]
    return evi

def __read_socre_file(score_file_path):
    sessions = []
    one_sess = []
    with open(score_file_path, 'r') as infile:
        i = 0
        for line in infile.readlines():
            i += 1
            tokens = line.strip().split('\t')
            one_sess.append((float(tokens[0]), int(tokens[1])))
            if i % 10 == 0:
                one_sess_tmp = np.array(one_sess)
                if one_sess_tmp[:, 1].sum() > 0:
                    sessions.append(one_sess)
                one_sess = []
    return sessions

def __recall_at_position_k_in_10(sort_data, k):
    sort_label = [s_d[1] for s_d in sort_data]#답.
    select_label = sort_label[:k]#답하나.
    return 1.0 * select_label.count(1) / sort_label.count(1)

def checkright(test_list,testevilist):
    sessions = __read_socre_file('score_base.txt')
    sessions2 = __read_socre_file('score_extern.txt')

    dockey = pickle.load(file=open("dockey.pkl", 'rb'))
    total_s = len(sessions)
    command_cnt=0
    cnt=0
    for i,(session1,session2) in enumerate(zip(sessions,sessions2)):
        sort_label = [s_d[0] for s_d in session2]
        idx=np.array(sort_label).argmax()
        max=np.array(sort_label).max()
        sort_data1 = sorted(session1, key=lambda x: x[0], reverse=True)
        r_1_base = __recall_at_position_k_in_10(sort_data1, 1)
        sort_data2 = sorted(session2, key=lambda x: x[0], reverse=True)
        r_1_extern = __recall_at_position_k_in_10(sort_data2, 1)

        if r_1_base== 0 and r_1_extern==1:
            cnt += 1
            print(i)
            print(sort_data1[0][0])
            print(test_list[10*i])
            print("\n")
            print(max, '\n')
            print(test_list[10*i+idx])
            print("\n")

            print(testevilist[10*i])
            print("\n")
            print(testevilist[10 * i + idx])
            print("\n")
            keylist=[]
            for key in dockey:
                if key in test_list[10*i].split("\n")[-1].split():
                    keylist.append(key)
            if keylist:
                command_cnt+=1

    print(command_cnt, cnt)


test_list = get_values('ubuntu_data/test.txt')
test_evi_list=get_evidence_values('bert_evi_test1_1_1.txt')
checkright(test_list,test_evi_list)


