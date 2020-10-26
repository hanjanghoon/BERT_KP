import requests
from bs4 import BeautifulSoup
import pickle
import re
from transformers import BertTokenizer
def make_post_text():
    namedict, descdict = pickle.load(file=open("ubuntu_manual_description.pkl", 'rb'))
    #namedict2, descdict2 = pickle.load(file=open("ubuntu_manual_description2.pkl", 'rb'))
    textlist = []
    cnt = 0
    dockey={}
    for name, desc in zip(namedict, descdict):
        if len(namedict[name])!=0 or len(descdict[desc])!=0:
            dockey[name]=len(dockey)
        textlist.append(namedict[name] + descdict[desc])

    file = open("post_train_ver2.txt", "w", encoding='utf-8')
    wholestring = ""

    for text in textlist:
        tempstring = ""
        for i, part in enumerate(text):

            origin=part
            part=re.sub('[^-a-zA-Z0-9 %/,\'\"\.()<>]', '', part)
            if i == 0:
                tempstring += part + '. '
            else:
                tempstring += part + ' '

        tempstring = tempstring[:-1]

        tempstring = " ".join(tempstring.split())

        tempstring = tempstring.replace(". ", ".\n")
        if len(tempstring)==0:
            print("0")
        wholestring += tempstring + "\n\n"
        cnt+=1
    wholestring = wholestring.replace("\n\n\n", "\n\n")
    wholestring = wholestring.replace("\n\n\n", "\n\n")
    wholestring = wholestring.replace("\n\n\n", "\n\n")
    file.write(wholestring)
    pickle.dump(dockey, file=open("dockey.pkl", 'wb'))
    print(cnt)

def spider(max_pages):
    co_command = pickle.load(file=open("co_command.pkl", 'rb'))
    page = 1
    namedict={}
    descdict={}
    while page < max_pages:
        url = 'https://manpages.ubuntu.com/manpages/xenial/en/man'+str(page)+'/'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        print(soup.a)
        cnt=0
        for link in soup.select('pre > a'):
            cnt+=1
            if cnt<3:
                continue
            try:
                title = (link.string).split('.')[0]
                if title not in co_command:
                    continue
                href = url + link.get('href')
                #print(href)
                print(title)
                namedict[title],descdict[title]=get_single_article(href)
            except:
                print(link,"error")

        page += 1
        print(cnt)
    pickle.dump([namedict,descdict], file=open("ubuntu_manual_description.pkl", 'wb'))

def new_spider(max_pages):
    co_command = pickle.load(file=open("co_command.pkl", 'rb'))
    page = 1
    namedict,descdict = pickle.load(file=open("ubuntu_manual_description.pkl", 'rb'))
    while page < max_pages:
        url = 'https://manpages.ubuntu.com/manpages/xenial/en/man'+str(page)+'/'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        print(soup.a)
        cnt=0
        for link in soup.select('pre > a'):
            cnt+=1
            if cnt<3:
                continue
            try:
                title = (link.string).split('.')[0]
                if title not in co_command:
                    continue
                if title in namedict:
                    continue
                href = url + link.get('href')
                #print(href)
                print(title)
                namedict[title],descdict[title]=get_single_article(href)
            except:
                print(link,"error")

        page += 1
        print(cnt)
    pickle.dump([namedict,descdict], file=open("ubuntu_manual_description.pkl", 'wb'))

def make_manual_dict(max_pages):
    page = 1
    manual_vocab = {}
    i = 0
    while page < max_pages:
        url = 'https://manpages.ubuntu.com/manpages/xenial/en/man' + str(page) + '/'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        print(soup.a)
        cnt = 0
        for link in soup.select('pre > a'):
            cnt += 1
            if cnt < 3:
                continue
            try:
                title = (link.string).split('.')[0]
                if title not in manual_vocab:
                    manual_vocab[title] = i
                    i += 1
            except:
                print(link, "error")

        page += 1
    pickle.dump(manual_vocab, file=open("manual_vocab.pkl", 'wb'))
    print(i)
def dict_compare():
    manual_vocab = pickle.load(file=open("manual_vocab.pkl", 'rb'))
    train_vocab = pickle.load(file=open("train_vocab.pkl", 'rb'))
    vocab = open('ori_vocab.txt', 'r').readlines()
    ori_vocab = {}
    for word in vocab:
        w = word.split('\n')[0].split('\t')
        ori_vocab[w[0]] = int(w[1])

    co_command={}
    i=0
    #for key in train_vocab:
     #   if len(key)>1 and key[-1]=='.':
      #      print(key)
    for key1 in manual_vocab:
        if key1 in train_vocab or (key1 in ori_vocab) :
            if key1 not in train_vocab and (key1 in ori_vocab):
                print(key1)

            co_command[key1]=i
            i+=1
    print(i)
    pickle.dump(co_command, file=open("co_command.pkl", 'wb'))

def get_single_article(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    namelist=[]
    desclist=[]
    for contents in soup.select('#tableWrapper'):

       # print(contents.text)
        text=contents.text
        nameflag=False
        descflag=False
        for line in text.split('\n'):
            if line.strip()=="NAME":
                nameflag=True
                continue
            if nameflag==True:
                if len(line)==0:
                    continue
                if line[0]!=" ":
                    nameflag=False
                    continue

                namelist.append(str(line.strip(" ")))

            if line.strip() == "DESCRIPTION":
                descflag = True
                continue
            if descflag == True:
                if len(line) == 0:
                    continue
                if line[0] != " ":
                    descflag = False
                    continue

                desclist.append(str(line.strip(" ")))
    return namelist,desclist

def dict_tokenize():
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased", do_lower_case=True)
    command_dict = pickle.load(file=open("co_command.pkl", 'rb'))
    token_dict={}
    for command in command_dict:
        tokens=tokenizer.tokenize(command)
        for token in tokens:
            if token not in token_dict:
                token_dict[token]=1
    pickle.dump(token_dict, file=open("manual_token_dict_ver2.pkl", 'wb'))

#make_manual_dict(10)
#dict_compare()
#new_spider(10)
#spider(10)
make_post_text()
#dict_tokenize()