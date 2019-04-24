import re
from Sinonim import get_sinonim
from PreProcessing import *
import StringMatching
import FileOperation
import itertools
import sys

#Baca file faq
Q, A = FileOperation.read_faq('pertanyaan.txt')

#Pre-processing tiap pertanyaan
proc_Q = [remove_nwhitespace(remove_stopwords(remove_noise(to_lowercase(question)))) for question in Q]

#Bentuk dictionary dengan key-nya sebuah string dan valuenya merupakan indeks dari pertanyaan
#atau jawaban yang mengandung kata tersebut, (keyword akan dibutuhkan saat regex(?))
keywords = {}

#Mengisi dictionary keywords
indeks = 0
for question in proc_Q:
    words = get_words(question)

    for word in words:
        wordExist = False
        sinonimExist = False

        if word not in keywords:
            list_sinonim = get_sinonim(word)
            for sinonim in list_sinonim:
                if sinonim in keywords:
                    sinonimExist = True
                    break
        else:
            wordExist = True

        if not (wordExist or sinonimExist):
            keywords[word] = [indeks]
        elif sinonimExist:
            keywords[sinonim] += [indeks] 
        elif wordExist:
            keywords[word] += [indeks]

    indeks += 1

#Pemanggilan query
query = sys.argv[1]
keys = keywords.keys()
candidate_ques_ans = []
default = "Halo, ada yang bisa dibantu?"
if len(query) > 0:
    #Pre-processing query
    proc_query = remove_nwhitespace(remove_stopwords(remove_noise(to_lowercase(query))))

    if (len(proc_query)>0):
        #Simpan seluruh sinonim dari tiap kata di query dan kata di query tsb
        query_words = get_words(proc_query)
        synonyms_word = [get_sinonim(word) for word in query_words]
        for i in range(len(query_words)):
            synonyms_word[i] += [query_words[i]]
        
        #Buat sebuah kombinasi kata dari synonnyms_word
        new_word_list = list(itertools.product(*synonyms_word))
        for words_list in new_word_list:
            #regex
            regex_query = "(.*)"
            match_words = ""
            indeks = -1
            len_query = len(" ".join(words_list))
            for w in words_list:
                regex_query = regex_query + w + "(.*)"
            for q in proc_Q:
                indeks = indeks + 1
                match_words = re.match(regex_query,q)
                len_question = 0
                presentase = 0
                if (match_words!=None):
                    len_question = len(q)
                    presentase = len_query/len_question
                    if (presentase>=0.30):
                        candidate_ques_ans.append((q,A[indeks],presentase))

        if (len(candidate_ques_ans)>0):
            high_ans = []     
            low_ans = []
            ans = ""
            for a in candidate_ques_ans:
                if a[2]>0.80:
                    high_ans.append(a)
                else:
                    low_ans.append(a)

            if (len(high_ans)>0):
                max = high_ans[0][2]
                i = 0
                indeks_max = 0
                for ans in high_ans:
                    if (ans[2]>max):
                        indeks_max = i
                        max = ans[2]
                    i += 1
                ans = high_ans[indeks_max][1]
            else:
                ans = "Apa maksud anda : \n"
                for q in low_ans:
                    ans += "-" + q[0] + "\n"
            print(ans)
        else:
            print("Saya tidak mengerti")
    else:
        print("Saya tidak mengerti")