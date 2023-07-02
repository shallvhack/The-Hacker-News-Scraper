import discord
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import argparse

token = ""
scrape_interval = 0
channel_id = ''

url = "https://thehackernews.com/search/label/hacking%20news"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

current_date = datetime.now().date()
previous_title = "New Mockingjay Process Injection Technique Could Let Malware Evade Detection"

def scrape_news():
    global previous_title
    articles = soup.find_all("div", class_="body-post clear")

    news_list = []

    for article in articles:
        # Extract the date
        date_string = article.find("span", class_="h-datetime").text.split("")[1]
        article_date = datetime.strptime(str(date_string), "%b %d, %Y").date()
        title = article.find("h2", class_="home-title").text.strip()

        if previous_title != title:
            image = article.find("img")['data-src']
            tags = article.find("span", class_ = "h-tags").text

            description = article.find("div", class_="home-desc").text.strip()
            news_list.append({
                "title": title,
                "image": image,
                "date": date_string,
                "tags": tags,
                "description": description
            })
        else:
            image = article.find("img")['data-src']
            tags = article.find("span", class_ = "h-tags").text

            description = article.find("div", class_="home-desc").text.strip()
            news_list.append({
                "title": title,
                "image": image,
                "date": date_string,
                "tags": tags,
                "description": description
            })
            previous_title = news_list[0]['title']
            break


    return news_list


def send_news(news_list):    
    intents = discord.Intents.default().all()
    client = discord.Client(intents=intents)


    @client.event
    async def on_ready():    
        channel = client.get_channel(channel_id)
       
        for news in news_list:
            embed = discord.Embed(title=news["title"], description=news["description"])
            embed.set_image(url=news["image"])
            embed.add_field(name="Tags", value=news["tags"], inline=False)
            embed.set_footer(text=news["date"])
            await channel.send(embed=embed)
            # time.sleep(2)
        await client.close()

    client.run(token)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-t', '--token', help='Discord Bot Token', required=True)
    parser.add_argument('-c', '--channel-id', help='Discord Channel Id', required=True)
    parser.add_argument("-s", "--interval", type=int, help="Scraping interval in seconds", required=True)
    parser.add_argument('-h', "--help", action="help", help="""Show this message and exit""")
    args = parser.parse_args()

    token = args.token
    channel_id = args.channel_id
    if (token and not(channel_id)) or (not(token) and channel_id) or (not(token) and not(channel_id)):
        parser.print_help() 
        exit(0)
    else:
        token = args.token
        channel_id = int(args.channel_id)
        scrape_interval = int(args.interval)
        print(scrape_interval)

    while True:
        news_list = scrape_news()
        if len(news_list) > 1:
            news_list.pop(0)
            send_news(news_list)
        
        time.sleep(scrape_interval)

