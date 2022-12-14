#####################################################################################################
#Important
#####################################################################################################
#Importing Libraries
import discord
import requests
import json

#Importing Constants
from constants import (CommandKey, CommandList, Creator, CreatorSocials,
                        CryptoPriceClassName, DiscordToken, HelpIntro,
                        HelpGreeting, HelpNote, TenorToken)
from bs4 import BeautifulSoup

#Variables
client = discord.Client(intents=discord.Intents.default())
embedColour = 0x00ff00

#####################################################################################################
#Helper Functions
#####################################################################################################

#Embeds Message
def embed_message(title, description, color):
    embeddedMessage = discord.Embed(title=title, description=description, color=color)
    return embeddedMessage

#Retrieves Quote from site
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    jsonData = json.loads(response.text)
    quote = "\"" + jsonData[0]['q'] + "\" ~ " + jsonData[0]['a']
    return quote

#Retrieves GIF from site
def get_gif(searchTerm):
    response = requests.get(f"https://g.tenor.com/v1/search?q={searchTerm}&key={TenorToken}&limit=1")
    jsonData = response.json()
    jsonData = jsonData['results'][0]['media'][0]['gif']['url']
    return jsonData

#Retrieves Price of Crypto Coin, Currency, and Stocks
def get_price(coin):
    url = f"https://www.google.com/search?q={coin}+price"
    HTML = requests.get(url)
    soup = BeautifulSoup(HTML.text, 'html.parser')
    data = soup.find("div", attrs={'class':f'{CryptoPriceClassName}'}).find("div", attrs={'class':f'{CryptoPriceClassName}'}).text
    return data


#####################################################################################################
#Bot Functions
#####################################################################################################

#When Program is run, Bot will be online
@client.event
async def on_ready():
    print(f"{client.user}"[:-5] + " is now Online!")

#When Bot is online, do the following commands
@client.event
async def on_message(message):
    #Makes sure Bot doesn't reply to itself
    if (message.author == client.user):
        return

    #Creator
    elif (message.content.lower().startswith(f"{CommandKey}creator")):
        embeddedMessage = embed_message(f"I was Created by {Creator[:-5]}!", f"{CreatorSocials}\n\n{HelpNote}", embedColour)
        await message.channel.send(embed=embeddedMessage)
    
    #Help
    elif (message.content.lower().startswith(f"{CommandKey}help")):
        embeddedMessage = embed_message(HelpGreeting, f"Hi there {message.author.name}! {HelpIntro}", embedColour)
        embeddedMessage.add_field(name="Commands", value=CommandList, inline=False)
        await message.author.create_dm()
        await message.author.dm_channel.send(embed=embeddedMessage)

    #Greetings for Creator
    elif (message.content.lower().startswith(f"{CommandKey}hello") and f"{message.author}" == Creator):
        embeddedMessage = embed_message(f"Ara Ara {message.author.name}!", HelpNote, embedColour)
        await message.channel.send(embed=embeddedMessage)
    
    #Greetings for Public
    elif (message.content.lower().startswith(f"{CommandKey}hello")):
        embeddedMessage = embed_message(f"Hello {message.author.name}.", HelpNote, embedColour)
        await message.channel.send(embed=embeddedMessage)
    
    #Quote
    elif (message.content.lower().startswith(f"{CommandKey}quote")):
        quote = get_quote()
        embeddedMessage = embed_message(quote, f"**Source:** ZenQuotes.io\n\n{HelpNote}", embedColour)
        await message.channel.send(embed=embeddedMessage)

    #GIF
    elif (message.content.lower().startswith(f"{CommandKey}gif ")):
        gifURL = get_gif(message.content.lower()[5:])
        embeddedMessage = discord.Embed(description=f"**Source:** Tenor.com", color=embedColour)
        embeddedMessage.set_image(url=gifURL)
        await message.channel.send(embed=embeddedMessage)
    
    #Price
    elif (message.content.lower().startswith(f"{CommandKey}price ")):
        coin = message.content.lower()[7:]
        price = get_price(coin)
        embeddedMessage = embed_message(f"Price: {price}s", f"**Source:** Google.com", embedColour)
        await message.channel.send(embed=embeddedMessage)


#####################################################################################################
#Other
#####################################################################################################

#Running the Bot
client.run(DiscordToken)

#####################################################################################################
#####################################################################################################