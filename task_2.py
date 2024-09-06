from json import load


def t(data: list) -> list:
    """
    Функция рекурсивного поиска всех компаний собранных в Json файле
    """
    answer = []
    for d in data:
        print(d)
        if "children" in d.keys():
            answer.extend(t(d["children"]))
        else:
           answer.append((d["title"], d["id"]))
    return answer


with open('new_test_hw.json', encoding='utf-8') as file:
    data = load(file)
    print(data)
    answer = t(data["children"])
    print(answer)
    print(len(answer))
    print(type(answer))
    print(type(answer[0]))

