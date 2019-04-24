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

#Pemanggilan query
query = sys.argv[1]
confidence = {}
candidate_ques_ans = []
hasil = []

#Pre-processing query
if len(query) > 0:
    proc_query = remove_nwhitespace(remove_stopwords(remove_noise(to_lowercase(query))))

    #Exact matching query dengan proc_Q dengan kmp
    if len(proc_query) > 0:
        #Simpan seluruh sinonim dari tiap kata di query dan kata di query tsb
        query_words = get_words(proc_query)
        synonyms_word = [get_sinonim(word) for word in query_words]
        for i in range(len(query_words)):
            synonyms_word[i] += [query_words[i]]
        
        #Buat sebuah kombinasi kata dari synonnyms_word
        new_word_list = list(itertools.product(*synonyms_word))
        for words_list in new_word_list:
            new_sentence = " ".join(words_list)
            i = 0

            #cek dengan kmp untuk setiap pasangan yang mungkin dari new_sentence dan list pertanyaan di proc_Q
            for question in proc_Q:
                conf, _ = StringMatching.kmp(question, new_sentence)
                if i not in confidence:
                    confidence[i] = conf
                else:
                    confidence[i] += conf

                i += 1
        #Mengubah nilai jadi berkisar antara 0.00 - 1.00
        for i in range(len(Q)):
            if confidence[i] >= 100:
                confidence[i] /= (confidence[i]/len(get_words(proc_query)))*len(get_words(proc_Q[i]))

        #memasukkan pertanyaan yang mempunyai confidence level >= 50
        conf_max = 0.50
        for i in range(len(confidence)):
            if confidence[i] >= conf_max:
                candidate_ques_ans.append([confidence[i], Q[i], A[i]])

        #jika ada lebih dari 1 kandidat, pisah jadi kandidat dengan conf >= conf_max dan < conf_max
        conf_max = 0.80
        candidate_high = []
        candidate_low = []
        for candidate in candidate_ques_ans:
            if candidate[0] >= conf_max:
                candidate_high.append(candidate)
            else:
                candidate_low.append(candidate)

        #Menentukan yang mana akan di print, jika candidate_high tidak kosong, akan mengoutput jawaban
        #atau banyak pertanyan jika candidate_high > 1
        if len(candidate_high) >= 1:
            #Jika ada lebih dari 1 ambil yang terbesar saja agar tidak ditanya terus menerus
            conf_max = 0
            idx_max = 0
            if len(candidate_high) > 1:
                for i in range(len(candidate_high)):
                    if candidate_high[i][0] > conf_max:
                        conf_max = candidate_high[i][0]
                        idx_max = i
                    
            hasil = [candidate_high[idx_max][2]]
        #jika candidate_high kosong, akan mengoutput semua list pertanyaan di candidate_low
        elif len(candidate_low) >= 1:
            for candidate in candidate_low:
                hasil = ['Apakah', 'maksud', 'anda : ']
                for i in range(len(candidate_low)):
                    if i >= 3:
                        break
                    hasil.append('\n-')
                    hasil.append(candidate_low[i][1])
        else:
            hasil = ['saya', 'tidak', 'mengerti']

        hasil = " ".join(hasil)
        print(hasil)
    else:
        print("Query anda tidak lengkap!")
else:
    print("Tidak ada query yang dimasukkan!")
