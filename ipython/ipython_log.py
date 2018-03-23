# IPython log file

get_ipython().run_line_magic('pinfo', 'str')
import json
db = json.load(open('database.json'))
len(db)
#db中的每个条目都是一个含有某种食物全部数据的字典。nutrients字段是一个字典列表，其中每个字典对应一种营养成分
db[0].keys()
db[0]['nutrients'][0]
nutrients = DataFrame(db[0]['nutrients'])
nutrients[:7]
#将字典列表转换为DataFrame时可以只抽取一部分字段。这里将取出食物的名称、分类、编号以及制造商等信息
info_keys=['decription','group','id','manufacturer']
info = DataFrame(db,columns=info_keys)
info[:5]
info_keys=['description','group','id','manufacturer']
info = DataFrame(db,columns=info_keys)
info[:5]
#通过value_counts可以查看食物类别的分布情况
import pandas as pd
pd.value_counts(info.group)[:10]
#将所有食物的营养成分整合到一个大表中
#首先将各食物的营养成分列表转换为一个DataFrame，并添加一个表示编号的列，然后将该DataFrame添加到一个列表中
nutrients = []
    
for rec in db:
    fnuts = DataFrame(rec['nutrients'])
    fnuts['id'] = rec['id']
    nutrients.append(fnuts)
    
nutrients = pd.concat(nutrients, ignore_index=True)
nutrients
nutrients.duplicated().sum()
nutrients = nutrients.drop_duplicates()
col_mapping = {'description':'food',
                'group':'fgroup'}
                
info = info.rename(columns=col_mapping, copy=False)
info
col_mapping = {'description':'nutrient',
               'group':'butgroup'}
               
nutrients= nutrients.rename(columns=col_mapping, copy=False)
nutrients
#将info和nutrients合并
ndata = pd.merge(nutrients,info,on='id',how='outer')
ndata
result = ndata.groupby(['nutrient','fgroup'])['value'].quantile(0.5)
result['Zinc, Zn'].sort_values().plot(kind='barh')
ndata
by_nutrient=ndata.groupby(['butgroup','nutrient'])
get_max = lambda x: x.xs(x.value.idxmax())
get_min = lambda x: x.xs(x.value.idmin())
max_food = by_nutrient.apply(get_max)[['value','food']]
max_food.food = max_food.food.str[:50]
max_food
