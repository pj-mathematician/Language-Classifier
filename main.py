import difflib
import jellyfish
import json
import sys
import os


def check_if_english(word):
    if word in english_word_data:
        return True
    else:
        return False


def check_if_spanish(word):
    sp = ["á", "é", "í", "ñ", "ó", "ú", "ü"]
    for i in sp:
        if i in word:
            return True
    # print(difflib.get_close_matches(word, spanish_word_data))
    if word in spanish_word_data:
        return True
    else:
        return False


def check_if_hindi_raw(word):
    if word in hindi_roman_word_data:
        return True
    else:
        temp = difflib.get_close_matches(word, hindi_roman_word_data)
        # print(temp)
        for i in temp:
            if jellyfish.jaro_similarity(word, i) > 0.99:
                # print(i,jellyfish.jaro_similarity(word,i))
                return True
        else:
            return False


def check_if_hindi(word):
    if word in hindi_roman_word_data:
        return True
    else:
        temp = difflib.get_close_matches(word, hindi_roman_word_data)
        # print(temp)
        for i in temp:
            if jellyfish.jaro_similarity(word, i) > 0.9:
                # print(i,jellyfish.jaro_similarity(word,i))
                return True
        else:
            return False


def do(text):
    raw = text.split()
    worker = []
    for i in raw:
        i = i.strip().lower()
        for j in i:
            if j.isdigit():
                worker.append(i + "_token")
                break
        else:
            if "-" in i:
                temp = i.split("-")
                for j in temp:
                    j = ''.join(e for e in j if (e.isalnum() and not e.isdigit()))
                    worker.append(j)
            else:
                i = ''.join(e for e in i if (e.isalnum() and not e.isdigit()))
                worker.append(i)

    answer = []
    is_spa = False
    is_hin = False
    for i in worker:
        try:
            if i.endswith("_token"):
                answer.append(i)
                continue
            if check_if_english(i):
                # i+="_eng"
                if not is_hin and check_if_spanish(i):
                    answer.append(i + "_spa_eng")
                    is_spa = True
                    # if check_if_english_api(i):
                    #     answer[-1] += "_eng"
                    continue
                elif check_if_hindi_raw(i) and not is_spa:
                    answer.append(i + "_hin_eng")
                    is_hin = True
                    # if check_if_english_api(i):
                    #     answer[-1] += "_eng"
                    continue
                else:
                    answer.append(i + "_eng")
                    continue
            elif not is_hin and check_if_spanish(i):
                answer.append(i + "_spa")
                is_spa = True
                continue
            elif check_if_hindi(i) and not is_spa:
                answer.append(i + "_hin")
                is_hin = True
                continue
            else:
                answer.append(i + "_none")
        except:
            answer.append(i + "_none")
    print(text)
    return " ".join(answer)


# INITIALISING DATA FILES
f = open("./esp_data.txt", 'r')
spanish_word_data = list(eval(f.read()))
f.close()
f = open("./hindi_data.txt", 'r')
hindi_roman_word_data = []
for i in f.readlines():
    hindi_roman_word_data.append(i.strip())
f.close()
f = open("./english_data.txt", 'r')
english_word_data = []
for i in f.readlines():
    if len(i.strip()) > 1:
        english_word_data.append((i.strip()))
f.close()
english_word_data.extend(['a', 'i'])


def world_language_classification(inpp="input.json", outp="output.json"):
    fin = open(inpp, 'r',encoding="utf-8")
    js = json.load(fin)
    fin.close()
    answer = {"output_list": []}
    for strings in js["input_list"]:
        answer["output_list"].append(do(strings))
    fout = open(outp, 'w')
    json.dump(answer, fout, ensure_ascii=False)
    fout.close()


if __name__ == "__main__":

    args = list(sys.argv)
    if len(args) <= 1:
        if os.path.exists("input.json"):
            world_language_classification()
        else:
            print("please provide an input file! [Default name is 'input.json' in the same directory]")
    elif len(args) == 2:
        inp = args[1]
        if os.path.exists(inp):
            world_language_classification(inp)
        else:
            print("please provide a valid input file! [Default name is 'input.json' in the same directory]")
    else:
        inp = args[1]
        out = args[2]
        if os.path.exists(inp):
            world_language_classification(inp, out)
        else:
            print("please provide a valid input file! [Default name is 'input.json' in the same directory]")
