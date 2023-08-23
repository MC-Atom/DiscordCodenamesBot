import random
import discord
from time import sleep
from PIL import Image, ImageDraw, ImageFont
import os

from discord import channel

#Opening all files I need
xMargin = 60
yMargin = xMargin
globalFont = 'Inkfree.ttf' 
fontSize = 35

def loadImage():
    size = (1015 + xMargin, 715 + yMargin)
    img = Image.new("RGB", size, "#ffffff")
    return img

# Randomly chooses words and puts them into a Matrix
def pickWords():
    wordsMatrix = []
    wordsFile = open("words.txt","r")
    words = wordsFile.read()
    wordList = words.split("\n")
    wordsFile.close()

    for i in range(5):
        wordsMatrixList = []
        x = 0
        while x < 5:
            chosenWord = wordList[random.randint(0,len(wordList)-1)]
            sameWord = False
            for thing in wordsMatrix:
                if chosenWord in thing:
                    sameWord = True

            if chosenWord in wordsMatrixList:
                sameWord = True

            if len(chosenWord) <= 10 or sameWord != True:
                wordsMatrixList.append(chosenWord)
            else:
                x -= 1
            x += 1
        wordsMatrix.append(wordsMatrixList)
    return wordsMatrix

def printMatrix(Matrix):
    #prints a matrix
    for list in Matrix:
        for word in list:
            print(word,end=' - ')
        print('')
        print(Matrix)

def drawLines(draw):
    global xMargin
    global yMargin
    global globalFont
    global fontSize
    fnt = ImageFont.truetype(globalFont,fontSize)
    img = ImageDraw.Draw(draw)
    #Draws Lines6
    for i in range(7):
        x = i * 201 + 5 + xMargin
        img.line([(x,0),(x,715+yMargin)],fill = (0,0,0),width = 10)

    for z in range(6):
        y = z * 141 + 5 + yMargin
        img.line([(0,y),(1015+xMargin,y)],fill = (0,0,0),width = 10)

    #Draws coordinate letters and numbers
    for i in range(1,6):
        x = i * 201 - 110 + xMargin
        img.text((x,9),str(i),font = fnt,fill = (0,0,0))

    for z in range(5):
        y = z * 141 + 55 + yMargin
        wordDict = {0:'a',1:'b',2:'c',3:'d',4:'e'}
        word = wordDict[z]
        img.text((20,y),word,font = fnt,fill = (0,0,0))

    

#Draws Squares
def makeColorMatrix ():
    #Make color Matrix
    colors = ['0','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1','2','2','2','2','2','2','2','2','3']

    colorMatrix = []
    for i in range(5):
        colorList = []
        for x in range(5):
            color = colors.pop(random.randint(0,len(colors)-1))
            colorList.append(color)
        colorMatrix.append(colorList)
    
    return colorMatrix

def drawSquares(draw,colorMatrix):
    global xMargin
    global yMargin
    img = ImageDraw.Draw(draw)
    row = 0
    column = 0
    for colorList in colorMatrix:
        for color in colorList:
            boxColor = (0,0,0)
            x = 0
            y = 0
            if color == '0':
                boxColor = (236,223,10)
            elif color == '1':
                boxColor = (28,168,241)
            elif color == '2':
                boxColor = (200,60,60)
            elif color == '3':
                boxColor = (0,0,0)

            x = column * 201 + 10 + xMargin
            y = row * 141 + 10 + yMargin
            
            img.rectangle([(x,y),(x+191,y+131)],fill = boxColor, width = 0)

            if column == 4:
                column = -1
                row += 1
            column += 1

def addText(draw,wordsMatrix,colorMatrix,isColor=0):
    #Add the Text
    global xMargin
    global yMargin
    global globalFont
    global fontSize
    fnt = ImageFont.truetype(globalFont,fontSize)
    img = ImageDraw.Draw(draw)
    
    for column in range(5):
        for row in range(5):
            x = row * 201 + 20 + xMargin
            y = column * 141 + 50 + yMargin
            
            word = wordsMatrix[column][row]
            color = colorMatrix[column][row]

            if isColor == 1 and color == '3':
                color = (255,255,255)
            else:
                color = (0,0,0)
            img.text((x,y),word,font = fnt,fill = color)

def writeImage(string,img):
    img.save(string)

def makeFullBoard():
    img = loadImage()
    imgColor = loadImage()
    wordsMatrix = pickWords()
    colorMatrix = makeColorMatrix()

    drawLines(img)
    addText(img,wordsMatrix,colorMatrix)

    drawLines(imgColor)
    drawSquares(imgColor,colorMatrix)
    addText(imgColor,wordsMatrix,colorMatrix,1)

    writeImage('boardWhite.png',img)
    writeImage('board.png',img)
    writeImage('boardColor.png',imgColor)

    return [colorMatrix,wordsMatrix]

def interpretString(string):
    columnDict = {'a':0,'b':1,'c':2,'d':3,'e':4}
    rowDict = {'1':0,'2':1,'3':2,'4':3,'5':4}
    if string[0] in columnDict and string[1] in rowDict:
        column = columnDict[string[0].lower()]
        row = rowDict[string[1]]
    else:
        return 'Error'
        
    return [column,row]
    
def drawTile(matricies,tile):
    global xMargin
    global yMargin
    global globalFont
    global fontSize
    fnt = ImageFont.truetype(globalFont,fontSize)
    row = tile[0]
    column = tile[1]
    color = matricies[0][row][column]
    word = matricies[1][row][column]
    draw = Image.open("board.png")
    img = ImageDraw.Draw(draw)

    if color == '0':
        boxColor = (236,223,10)
    elif color == '1':
        boxColor = (28,168,241)
    elif color == '2':
        boxColor = (200,60,60)
    elif color == '3':
        boxColor = (0,0,0)

    x = column * 201 + 10 + xMargin
    y = row * 141 + 10 + yMargin

    img.rectangle([(x,y),(x+191,y+131)],fill = boxColor,width = 0)

    x = column * 201 + 20 + xMargin
    y = row * 141 + 50 + yMargin

    if color == '3':
        color = (255,255,255)
    else:
        color = (0,0,0)
    img.text((x,y),word,font = fnt,fill = color)
    writeImage('board.png',draw)

async def getMessageById(id,channelList):
    if id == "-1":
        return -1
    else:
        for channelId in channelList:
            channel = client.get_channel(channelId)
            try:
                return await channel.fetch_message(id)
            except discord.errors.NotFound:
                print("Not Found")
                return -1

def reveal(matricies,tileString):
    tile = interpretString(tileString)
    if tile == 'Error':
        return True
    drawTile(matricies,tile)

def react(message,emojiName):
    emoji = '❌'
    for thing in message.guild.emojis:
        if thing.name == emojiName:
            emoji = thing
    return emoji

    


#Discord
#https://discord.com/api/oauth2/authorize?client_id=1143743595032084551&permissions=8&scope=bot
#https://discord.com/api/oauth2/authorize?client_id=1143743595032084551&permissions=40666961279040&scope=bot

TOKEN = os.environ['BOT_TOKEN']

print(TOKEN)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

matrices = []

@client.event #-----------------------------------------client.event------------------------

async def on_message(message):
    
    global matrices

    if message.content.upper().startswith('!START'):
        matrices = makeFullBoard()
        mentioned = message.mentions
        for person in mentioned:
            if person.dm_channel == None:
                await person.create_dm()
            await person.dm_channel.send(file=discord.File('boardColor.png'))
        await message.channel.send(file=discord.File('board.png'))

    if message.content.upper().startswith('!SENDKEY'):
        mentioned = message.mentions
        for person in mentioned:
            if person.dm_channel == None:
                await person.create_dm()
            await person.dm_channel.send(file=discord.File('boardColor.png'))
        await message.channel.send("Board Sent")

    if message.content.upper().startswith('!GO'):
        if matrices == []:
            await message.channel.send('Please start a game first')
        tileString = message.content[3:].strip()
        isError = reveal(matrices,tileString)
        if isError:
            await message.channel.send('Please format choice as [Letter][Number] as in "!Go f6"')
        else:
            await message.channel.send(file=discord.File('board.png'))

    if message.content.upper().startswith('!REVEAL'):
        await message.channel.send(file=discord.File('boardColor.png'))

    if message.content.upper().startswith('!EXPLODE'):
        await message.channel.send('Boom')

    if message.content.upper().startswith('NO U') and message.author != client.user:
        await message.channel.send('no u')

    if message.content.upper().startswith('!HELP'):
        await message.channel.send("""
`!Start [@user] [@user] ...   ` Start a game and send the answer key to the mentioned users
`!SendKey [@user] [@user] ... ` Send the answer key to the mentioned users
`!Go [a-e]#                   ` Guess the given space (ie: `!Go e3`)
`!Reveal [@user] [@user] ...  ` Reveal the full board""")

    # maybe add a way of deleting one off the top of a stack      



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
client.run(TOKEN)