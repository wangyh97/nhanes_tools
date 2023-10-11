import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pathlib import Path

# 定义参数
COMPONENTS = ['Demographics', 'Dietary', 'Examination', 'Laboratory', 'Questionnaire']
YEARS = list(range(1999, 2018, 2))

# 创建文件夹结构
ROOT_DIR = Path('data')


def create_folders():
    for year in YEARS:
        for comp in COMPONENTS:
            (ROOT_DIR / f"{year}-{year + 1}" / f"{comp} data").mkdir(parents=True, exist_ok=True)


def get_file_info():
    data = []
    for year in YEARS[:-1]:
        for comp in COMPONENTS:
            folder_path = ROOT_DIR / f"{year}-{year + 1}" / f"{comp} data"
            url = f'https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component={comp}&CycleBeginYear={year}'
            data.append([folder_path, url])
    return pd.DataFrame(data, columns=['Folder Path', 'URL'])


def fetch_file_links_and_names(df):
    for index, row in df.iterrows():
        folder_path, url = row['Folder Path'], row['URL']

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        file_links, file_names = [], []
        files_table = soup.find('table')
        for tr in files_table.find_all('tr'):
            for td in tr.find_all('td'):
                if td.find('a'):
                    link = td.find('a')['href']
                    if link.endswith('.XPT'):
                        file_links.append('https://wwwn.cdc.gov' + link)
                        file_names.append(link.split('/')[-1])

        df.loc[index, 'file_links'] = str(file_links)
        df.loc[index, 'file_names'] = str(file_names)
    df.to_csv('temp_path.csv')
    print('temp_file has been generated')

def download_files(df):
    for index, row in df.iterrows():
        folder_path = Path(row['Folder Path'])
        file_links = eval(row['file_links'])
        file_names = eval(row['file_names'])

        for link, name in zip(file_links, file_names):
            file_path = folder_path / name
            if not file_path.exists():
                file_size = int(requests.head(link).headers["Content-Length"])
                with requests.get(link, stream=True) as r, file_path.open('wb') as f:
                    downloaded = 0
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            print(f"\r{file_path} {downloaded / file_size * 100:.2f}% downloaded", end='')
                    print(f'\n{name} has been downloaded')
            else:
                print(f'{name} has been downloaded')
    print('all done, temp file removed')
    os.remove('temp_path.csv')

# 主函数
def main():
    if not os.path.exists('temp_path.csv'):
        print('starting make path file for parsing')
        create_folders()
        df = get_file_info()
        fetch_file_links_and_names(df)
        df = pd.read_csv('temp_path.csv')
    else:
        print('path file already exists')
        df = pd.read_csv('temp_path.csv')
    download_files(df)


if __name__ == "__main__":
    main()
