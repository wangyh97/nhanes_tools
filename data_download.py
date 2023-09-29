'''
@author: wangyh, sun-yat-sen university
@data: 2023-9-25
@contact me: wangyh97@mail2.sysu.edu.cn

automatic create Hierarchical Folder, download of NHANES data from 1999-2017(prepandemic) and save 
'''


import os
from bs4 import BeautifulSoup 
import requests
import pandas as pd

# 定义参数
list_comp = ['Demographics', 'Dietary', 'Examination', 'Laboratory','Questionnaire']
list_year = list(range(1999, 2018, 2))

# 创建文件夹结构 
root_dir = './data'
if not os.path.exists(root_dir):
    os.mkdir(root_dir)

for i in range(len(list_year)-1):
    year_dir = os.path.join(root_dir, str(list_year[i])+'-'+str(list_year[i]+1))
    if not os.path.exists(year_dir):
        os.mkdir(year_dir)
        
    for comp in list_comp:
        comp_dir = os.path.join(year_dir, comp + ' data')
        if not os.path.exists(comp_dir):
            os.mkdir(comp_dir)

# 构建dataframe,包含文件路径，网页链接
data = [] 
for i in range(len(list_year)-1):
    for comp in list_comp:
        folder_path = './data/{}-{}/{} data'.format(list_year[i], list_year[i]+1, comp) 
        url = 'https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component={}&CycleBeginYear={}'.format(comp, list_year[i])
        # 爬取页面获取文件信息
        data.append([folder_path, url])

df = pd.DataFrame(data, columns=['Folder Path', 'URL'])

# 爬取每个网页下所有文件的下载链接及文件名，保存在csv
for index, row in df.iterrows():
    folder_path = row['Folder Path']  
    url = row['URL']
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    file_links = []
    file_names = []
    
    # 定位到文件table,遍历所有tr获取链接和文件名
    files_table = soup.find('table') 
    for tr in files_table.find_all('tr'):
        for td in tr.find_all('td'):
            if td.find('a'):
                link = td.find('a')['href']
                if link.endswith('.XPT'):  
                    file_links.append('https://wwwn.cdc.gov'+link)
                    file_names.append(link.split('/')[-1])
            
    # 添加两列到dataframe       
    df.loc[index, 'file_links'] = str(file_links)   #如果不转换为str则因数据类型为float64触发bug，读取csv信息时通过eval转换回list
    df.loc[index, 'file_names'] = str(file_names)
    
# 遍历dataframe，下载并重命名文件，保存到对应文件夹

for index, row in df.iterrows():
    folder_path = row['Folder Path']
    file_links = eval(row['file_links'])
    file_names = eval(row['file_names'])
        
    for link, name in zip(file_links, file_names):
        file_path = os.path.join(folder_path, name[1:])

        if not os.path.exists(file_path):
            #显示下载进度
            file_size = int(requests.head(link).headers["Content-Length"]) 
            with requests.get(link, stream=True) as r:
                downloaded = 0
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk: 
                            f.write(chunk)
                            downloaded += len(chunk)
                            print('\r',end='')
                            print("{} {:.2f}% downloaded".format(file_path, downloaded/file_size*100),end='')
                    print(f'{name[1:]} has been downloaded')
        else:
            print(f'{name[1:]} has been downloaded')

