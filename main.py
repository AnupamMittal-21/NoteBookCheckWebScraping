import os

from dotenv import load_dotenv

from NoteBookCheckScraper import NoteBookCheck
from mobileDataScraper import MobileDataScraper
import pandas as pd
import pickle

if __name__ == '__main__':
    load_dotenv('data.env')
    driver_path_name = os.environ.get("DRIVER_PATH")

    with MobileDataScraper(driver_path_name) as bot:
        bot.getUrl("https://www.notebookcheck.net/Reviews.55.0.html")
        links = bot.scrapLinks()
        list_of_dict = []
        df = None
        cnt = 0
        for link in links:
            if cnt == 15:
                break
            cnt += 1
            with NoteBookCheck() as bot:
                # Functions Starts...
                bot.getUrl(link)
                bot.scrapName()
                bot.scrapSpecs()
                bot.scrapChassis()
                bot.scrapDetailTables()
                bot.scrapDisplay()
                bot.scrapHdd()
                data_dict = bot.collectData()
                list_of_dict.append(data_dict)

        df = pd.DataFrame(list_of_dict)
        print("Final DF...")
        print(df)

        with open("mobileData.pkl", "wb") as file:
            pickle.dump(df.to_dict(), file)

    with open("mobileData.pkl", "rb") as file:
        data_dict = pickle.load(file)

    df = pd.DataFrame.from_dict(data_dict)

    df.to_csv("mobileData.csv", index=False)