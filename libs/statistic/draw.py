import json
import csv
from graphviz import Digraph


# 生成first集
def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError
def write_first(first_set):
    with open('first.json','w') as json_file:
        json.dump(first_set, json_file ,default=set_default)
        
#生成语法分析表

def trans(actionpath,gotopath,csvpath,type):
    action_file = open(actionpath, 'r', encoding='utf8')
    goto_file = open(gotopath, 'r', encoding='utf8')
    csv_file = open(csvpath, type, newline='')
    keys = []
    writer = csv.writer(csv_file)
    
    action_data = action_file.read()
    action_dic_data = json.loads(action_data, encoding='utf8')
    
    goto_data = goto_file.read()
    goto_dic_data = json.loads(goto_data, encoding='utf8')

    for dic in action_dic_data:
        action_time = action_dic_data[dic]
        goto_time = goto_dic_data[dic]
        action_time.update(goto_time)
        keys = action_time.keys()
    keys = list(keys)
    keys.insert(0,'状态')
    writer.writerow(keys)


    for dic in action_dic_data:
        values = [dic,]
        dic = action_dic_data[dic]
        for key in keys:
            if key not in dic:
                dic[key] = ''
        values = values +list(dic.values())
        writer.writerow(values)
    action_file.close()
    goto_file.close()
    csv_file.close()

#     trans('action.json','goto.json', 'my.csv','w')

# 画项目集规范族
def write_sta_set(sta_set,sta_table):   
    dot = Digraph(comment='The Test Table', format="png")
    for dic in sta_set:
        sta_set_list = []
        data = list(sta_set[dic])
        for key in data:
            left = key[0]
            right_tar = key[1]
            add_tar = key[2]
            right = ''
            for str_ in right_tar:
                right+=str_
            add = ''
            for str_ in add_tar:
                if(add!=''):
                    add += (','+str_)
                else:
                    add += str_
            sta_set_list.append(left+'->'+right+','+add)
        all_sta = ''
        for j in sta_set_list:
            if(all_sta == ''):
                all_sta += j
            else:
                all_sta += ('\n'+j)
        dot.node(str(dic), str(dic)+'\n'+all_sta)
    for dic in sta_table:
        data = sta_table[dic]
        for key in data:
            value = data[key]
            dot.edge(str(dic), str(value), key)
    dot.save('test-table.gv')
    dot.render('test-table.gv')
