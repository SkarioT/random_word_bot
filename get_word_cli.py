import random


file_name_all_words = 'all_words.txt'
file_name_all_verbs = 'verbs.txt'


def load_words(file_name):
    words_all = {}
    with open(file_name,'r',encoding='utf-8-sig') as read_sloy:
        for line in read_sloy.readlines():
            split_line = line.replace(" – "," - ").replace("\n","").replace("\ufeff",'').split(" - ")
            words_all[split_line[0]]=split_line[1]
    return words_all

all_words = load_words(file_name_all_words)
all_verbs = load_words(file_name_all_verbs)

def get_and_genirate_words(words): 

    quiestion_key = random.choice(list(words.keys()))
    answer_true = words.get(quiestion_key)

    #добиваюст рандомное слово из словоря/базы
    answer_fake_1 = random.choice(list(words.values()))
    while answer_fake_1 == words.get(quiestion_key):
        answer_fake_1 = random.choice(list(words.values()))
    answer_fake_2 = random.choice(list(words.values()))
    while answer_fake_2 == answer_true or answer_fake_2==answer_fake_1:
        answer_fake_2 = random.choice(list(words.values()))

    #верное слово + 2 рамдомных закиываю в один лист    
    res_list = [answer_true,answer_fake_1,answer_fake_2]

    # "перемешиваю эти 3 слова"
    rand_quiestion_list = random.sample(res_list,3)
    resault = {}
    resault = {'question_true' : quiestion_key,'answer_true':answer_true,'question_fake': rand_quiestion_list}
    return resault
    # return quiestion_key,answer_true,rand_quiestion_list

    #тестовый блок, для работы в консоли 
    
    
    # print("_"*20+'\n',f"Слово {quiestion_key}")
    # #при выводе вывожу по порядку "перемешенный" список
    # print(f"1){rand_pos_list[0]}")
    # print(f"2){rand_pos_list[1]}")
    # print(f"3){rand_pos_list[2]}")
    # inp = input("Выберите номер верного значения: ")

    # if rand_pos_list[int(inp)-1] == answer_true:
    #     print(f"Всё верно {quiestion_key} это {answer_true}")
    # else:
    #     print(f"{rand_pos_list[int(inp)-1]} не является переводом для слова {quiestion_key}")
    #     print(f"Верный перевод слова {quiestion_key} - {answer_true}")
        
# res = get_and_genirate_words()
# print(res.get('question_fake')[0])
