"""

Uni project. Update literature.

Developer: Stanislav Alexandrovich Ermokhin

"""

dic = dict()

for item in ['_ru', '_en']:
    with open('literature'+item+'.txt') as a:
        lst = a.read().split(';')
        dic[item] = lst

new_lst = list()
for key in dic:
    dic[key] = sorted(['\t'+item.replace('\n', '') for item in dic[key]])
    for item in dic[key]:
        new_lst.append(item)

with open('literature.txt', 'w') as a:
    a.write('\n'.join(new_lst))
