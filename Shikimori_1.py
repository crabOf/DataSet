import requests
import fake_useragent
import bs4
import pandas as pd
import random
import time  # Импортируем библиотеку time

def convert_duration_to_minutes(duration_str):
    # Инициализируем переменные для часов и минут
    hours = 0
    minutes = 0
    
    # Проверяем, содержит ли строка "час" или "часа"
    if 'час' in duration_str:
        # Извлекаем часы
        hours_part = duration_str.split('час')[0].strip()
        if hours_part.isdigit():
            hours = int(hours_part)
    
    # Проверяем, содержит ли строка "мин"
    if 'мин' in duration_str:
        # Извлекаем минуты
        minutes_part = duration_str.split('мин')[0].split()[-1]
        if minutes_part.isdigit():
            minutes = int(minutes_part)
    
    # Конвертируем часы в минуты и возвращаем общее количество минут
    total_minutes = hours * 60 + minutes
    return total_minutes


columns = [
    "raiting", "name", "data", "epis", "isreal", "reit", "score", "leng", "studio",
    "Avant-garde", "Gourmet", "Drama", "Comedy", "Slice of Life", "Adventure", 
    "Romance", "Supernatural", "Sports", "Mystery", "Thriller", "Horror", 
    "Science Fiction", "Fantasy", "Action", "Ecchi", "Erotica", "Hentai", 
    "Shounen", "Shoujo", "Seinen", "Josei", "Kids"
]

data_df = pd.DataFrame(columns=columns)

url = "https://shikimori.one/animes/page/"

le = 0

pages = 1102

agent = fake_useragent.UserAgent()

for i in range(0, pages + 2, 1):
    urls = url + str(i)
    
    header = {
        "User-Agent": agent.random
    }

    err = 0
    while (err < 5):
        ans = requests.get(urls, headers=header)
        if (ans.status_code != 200):
            time.sleep(float(random.randint(10, 20)) / 10.)
            err += 1
        if (ans.status_code == 200):
            break
    if err > 5:
        continue

    ans = ans.text

    soup = bs4.BeautifulSoup(ans, features='lxml')

    # print(soup)
    # input()

    animes = soup.find_all('a', class_ = "cover anime-tooltip")

    # print(len(animes))

    for anime in animes:
        
        info = {
            "raiting": le,
            "name": "",
            "data": "",
            "epis": 1,
            "isreal": False,
            "reit": "",
            "score": "",
            "leng": "",
            "studio": "",
            "Avant-garde": 0,
            "Gourmet": 0,
            "Drama": 0,
            "Comedy": 0,
            "Slice of Life": 0,
            "Adventure": 0,
            "Romance": 0,
            "Supernatural": 0,
            "Sports": 0,
            "Mystery": 0,
            "Thriller": 0,
            "Horror": 0,
            "Science Fiction": 0,
            "Fantasy": 0,
            "Action": 0,
            "Ecchi": 0,
            "Erotica": 0,
            "Hentai": 0,
            "Shounen": 0,
            "Shoujo": 0,
            "Seinen": 0,
            "Josei": 0,
            "Kids": 0
        }
        
        le += 1
        
        
        try:
            info["name"] = anime.find(class_ = 'name-ru').text
        except:
            pass
            # print("Error in name")
        
        try:
            info["data"] = anime.find('span', class_ = 'misc').find_all('span')[1].text
        except:
            continue
            # print(info["name"], " Error in data")
            
        header = {
            "User-Agent": agent.random
        }
        
        err = 0

        while (err < 5):
            subans = requests.get(anime['href'], headers=header)
            if (subans.status_code != 200):
                time.sleep(1)
                err += 1
            if (subans.status_code == 200):
                break
        if err > 5:
            continue

        subans = subans.text
        
        subsoup = bs4.BeautifulSoup(subans, features='lxml')
        subdata = subsoup.find_all('div', class_='line-container')
        
        for a in subdata:
            if a.find('div', class_='key').text == "Эпизоды:":
                info["epis"] = a.find(class_='value').text
            if a.find('div', class_='key').text == "Статус:":
                info["isreal"] = True if a.find(class_='value').find('span')['data-text'] == "вышло" else False
            elif a.find('div', class_='key').text == "Рейтинг:":
                info["reit"] = a.find(class_='value').find('span').text
            elif a.find('div', class_='key').text == "Длительность эпизода:":
                info["leng"] = convert_duration_to_minutes(a.find(class_='value').find('span').text)   
        try:
            nj = subsoup.find_all(class_="genre-ru")
            for a in nj:
                # print(a.text)
                # input()
                if a.text == "Авангард":
                    info["Avant-garde"] = 1
                elif a.text == "Гурман":
                    info["Gourmet"] = 1
                elif a.text == "Драма":
                    info["Drama"] = 1
                elif a.text == "Комедия":
                    info["Comedy"] = 1
                elif a.text == "Повседневность":
                    info["Slice of Life"] = 1
                elif a.text == "Приключения":
                    info["Adventure"] = 1
                elif a.text == "Романтика":
                    info["Romance"] = 1
                elif a.text == "Сверхъестественное":
                    info["Supernatural"] = 1
                elif a.text == "Спорт":
                    info["Sports"] = 1
                elif a.text == "Тайна":
                    info["Mystery"] = 1
                elif a.text == "Триллер":
                    info["Thriller"] = 1
                elif a.text == "Ужасы":
                    info["Horror"] = 1
                elif a.text == "Фантастика":
                    info["Science Fiction"] = 1
                elif a.text == "Фэнтези":
                    info["Fantasy"] = 1
                elif a.text == "Экшен":
                    info["Action"] = 1
                elif a.text == "Этти":
                    info["Ecchi"] = 1
                elif a.text == "Эротика":
                    info["Erotica"] = 1
                elif a.text == "Хентай":
                    info["Hentai"] = 1
                elif a.text == "Сёнен":
                    info["Shounen"] = 1
                elif a.text == "Сёдзё":
                    info["Shoujo"] = 1
                elif a.text == "Сэйнэн":
                    info["Seinen"] = 1
                elif a.text == "Дзёсей":
                    info["Josei"] = 1
                elif a.text == "Детское":
                    info["Kids"] = 1
        except:
            # print("Error in g")
            # continue
            pass
        # print("g")
            

        subdata2 = subsoup.find('div', class_='c-info-right')
        try:
            info["studio"] = subdata2.find_all('div', class_='block')[2].find('a')['title'].split(' ')[-1]
        except:
            # print(info["name"], " Error in studio")
            try:
                # print(subdata2.find_all('div', class_='block')[1].find('a')['title'].split(' ')[-1])
                # input()
                info["studio"] = subdata2.find_all('div', class_='block')[1].find('a')['title'].split(' ')[-1]
            except:
                pass
                # print(i, info["name"], " Error in studio even more")
        
        try:
            info["score"] = subsoup.find('div', class_='text-score').find_all('div')[0].text
        except:
            # print(info["name"], " Error in score")
            try:
                # print(subdata2.find('div', class_='scores').find_all('meta')[2]["content"])
                # input()
                info["studio"] = subdata2.find('div', class_='scores').find_all('meta')[2]["content"]
            except:
                pass
                # print(i, info["name"], " Error in studio even more")

        for a in info:
            print(info[a], end = ', ')
        print()
        data_df.loc[len(data_df)] = info
    print(i)
 
data_df.to_csv("data.csv", index=False, encoding="utf-8")