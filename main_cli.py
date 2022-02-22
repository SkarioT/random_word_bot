import random
import asyncio


# async def get_and_genirate_words():
def get_and_genirate_words(): 
    file_name = '10_sloynik.txt'
    slowy = {}
    with open(file_name,'r',encoding='utf-8-sig') as read_sloy:
        # print(read_sloy.readlines())
        for line in read_sloy.readlines():
            split_line = line.replace(" – "," - ").replace("\n","").replace("\ufeff",'').split(" - ")
            # print(split_line)
            slowy[split_line[0]]=split_line[1]

    res_key = random.choice(list(slowy.keys()))
    res_val_true = slowy.get(res_key)

    #добиваюст рандомное слово из словоря/базы
    res_val = random.choice(list(slowy.values()))
    while res_val == slowy.get(res_key):
        res_val = random.choice(list(slowy.values()))
    res_val_2 = random.choice(list(slowy.values()))
    while (res_val_2 == slowy.get(res_key)) or res_val_2==res_val:
        res_val_2 = random.choice(list(slowy.values()))

    #верное слово + 2 рамдомных закиываю в один лист    
    res_list = [res_val_true,res_val,res_val_2]

    # "перемешиваю эти 3 слова"
    rand_pos_list = random.sample(res_list,3)
    # print('rand_pos_list',rand_pos_list)
    # print("res_key",res_key)
    # print('res_val_true',res_val_true)
    return res_key,res_val_true,rand_pos_list
    # print("_"*20+'\n',f"Слово {res_key}")
    # #при выводе вывожу по порядку "перемешенный" список
    # print(f"1){rand_pos_list[0]}")
    # print(f"2){rand_pos_list[1]}")
    # print(f"3){rand_pos_list[2]}")
    # inp = input("Выберите номер верного значения: ")

    # if rand_pos_list[int(inp)-1] == res_val_true:
    #     print(f"Всё верно {res_key} это {res_val_true}")
    # else:
    #     print(f"{rand_pos_list[int(inp)-1]} не является переводом для слова {res_key}")
    #     print(f"Верный перевод слова {res_key} - {res_val_true}")
        
# res = get_and_genirate_words()
# print(res)
