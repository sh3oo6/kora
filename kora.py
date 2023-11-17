import requests,csv
import bs4
from time import *
from telethon.sync import *
DEX = '6140911166'
people = 1
api_id = 2192036
api_hash = '3b86a67fc4e14bd9dcfc2f593e75c841'
bot_token = '5994181633:AAGllwOtQnu2geWM0oA4MRMxxywwfIbBPfo'
bot = TelegramClient('botkora', api_id, api_hash).start(bot_token=bot_token)
time = time()
@bot.on(events.CallbackQuery(data="Matches"))
async def Matches(event):
    global time
    s = strftime("%m/%d/%Y", gmtime(time))
    url = f'https://www.yallakora.com/match-center/مركز-المباريات?date={s}'
    page = requests.get(url)
    src = page.content
    soup = bs4.BeautifulSoup(src, "lxml")
    champions = soup.find_all("div", {'class': 'matchCard'})
    for champion in champions:
        ch_title = champion.contents[1].find('h2').text.strip()
        ch_machs = champion.contents[3].find_all("div", {'class': 'liItem'})
        Matches_list = []
        Matches_list.append(f'🎦{ch_title}⚽')
        for mach in ch_machs:
            teamA = mach.find("div", {'class': 'teams teamA'}).text.strip()
            teamB = mach.find("div", {'class': 'teams teamB'}).text.strip()
            scores = mach.find("div", {'class': 'MResult'}).find_all('span', {'class': 'score'})
            time = mach.find("div", {'class': 'MResult'}).find('span', {'class': 'time'}).text.strip()
            score = f'  {scores[0].text.strip()} - {scores[1].text.strip()}  '
            Matches = (teamA + score + teamB + ' ' + time)
            Matches_list.append(Matches)
        message = "\n\n".join(Matches_list)
        await bot.send_message(event.chat_id,message)
async def StartButtons(event):
    buttons = [[Button.inline("Matches", "Matches")]]
    await event.reply("⚽Fire Ball - ", buttons=buttons)

@bot.on(events.NewMessage(pattern='/start'))
async def BotOnStart(event):
    file_r = open('peopel.txt', 'r')
    if str(event.chat_id) in file_r.read():
        await StartButtons(event)
        file_r.close()
    else:
        global people
        await event.delete()
        file_a = open('peopel.txt', 'a')
        file_a.write(str(event.chat_id) + '\n')
        file_a.close()
        await StartButtons(event)
        entity = await bot.get_entity(event.chat_id)
        info_Ac = f'first_name : {entity.first_name}\nlast_name : {entity.last_name}\nid : {entity.id}\nusername : {entity.username}\nphone : {entity.phone}\nXX : {str(people)}'
        people += 1
        await bot.send_message(int(DEX), info_Ac)




bot.run_until_disconnected()

