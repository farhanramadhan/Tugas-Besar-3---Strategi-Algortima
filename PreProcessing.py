import string
from FileOperation import read_txt

#Menghapus noise (huruf selain alfabet, angka dan beberapa karakter special)
def remove_noise(line, notNoise=list(string.ascii_letters)+list(string.digits)+list(string.whitespace)):
    hasil = line
    i = 0

    for char in line:
        if char not in notNoise:
            hasil = hasil[:i] + " " + hasil[i+1:]
        i += 1

    return "".join(hasil)

#Mengganti semua huruf jadi lower case
def to_lowercase(line):
    hasil = line

    for char in line:
        if ord(char) >=65 and ord(char) <=90:
            hasil = hasil.replace(char, chr(ord(char) + 32))
    return "".join(hasil)

#Mengganti semua huruf menjadi upper case
def to_uppercase(line):
    hasil = line

    for char in line:
        if ord(char) >=97 and ord(char) <=122:
            hasil = hasil.replace(char, chr(ord(char) - 32))
    return "".join(hasil)

#Menghapus stop-words
stopWords = read_txt("stopwords-id.txt")
def remove_stopwords(line):
    hasil = line
    word = []
    
    for char in line:
        if char != ' ':
            word.append(char)
        else:
            if "".join(word) in stopWords:
                hasil = hasil.replace("".join(word), "")
            word = []
    
    if "".join(word) in stopWords:
        hasil = hasil.replace("".join(word), "")
    return "".join(hasil)

#Menhapus spasi yang berlebihan di awal, akhir, atau antar kata
def remove_nwhitespace(line):
    return " ".join(line.split())

#print(remove_nwhitespace(remove_stopwords(to_lowercase(remove_noise("   !SeoR @ang Y* anG Tang GUH)   ")))))

#Menghitung berapa banyak kata dalam suatu string dengan cara menghitung berapa banyak
#spasinya
def get_nbchar(line):
    count = 0
    for char in line:
        if char == string.whitespace or char == ' ':
            count += 1

    return len(line)-count

#Mereturn tiap kata dalam suatu line
def get_words(line):
    word = []
    words = []
    for char in line:
        if char != ' ':
            word.append(char)
        else:
            words.append("".join(word))
            word = []
    
    words.append("".join(word))
    return words