import os
import discord
from dotenv import load_dotenv
import nltk
import random
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client(intents=discord.Intents.default())

if os.path.isfile("memorynoun.txt"):
    with open("memorynoun.txt", "r", encoding="utf-8") as file:
        noun = file.read()
        file.close()
    noun = noun.replace("[", "").replace("]", "").replace("'", "").replace(",", "")
    print(noun)
    noun = noun.split()
else:
    noun = []
if os.path.isfile("memoryverb.txt"):
    with open("memoryverb.txt", "r", encoding="utf-8") as file:
        verb = file.read()
        file.close()
    verb = verb.replace("[", "").replace("]", "").replace("'", "").replace(",", "")
    verb = verb.split()
else:
    verb = []
if os.path.isfile("memoryadjective.txt"):
    with open("memoryadjective.txt", "r", encoding="utf-8") as file:
        adjective = file.read()
        file.close()
    adjective = adjective.replace("[", "").replace("]", "").replace("'", "").replace(",", "")
    adjective = adjective.split()
else:
    adjective = []

controlMode = False
learningMode = False
kmsMode = False
sentence = ""

@client.event
async def on_message(message):
    global controlMode, kmsMode, learningMode, sentence, noun, verb, adjective
    _message = ""

    if message.author.name == "auracodestuff":
        if 'learning mode' in message.content.lower():
            learningMode = True
            await message.channel.send(f"learning mode on")

    if message.author.name == "auracodestuff":
        if 'control' in message.content.lower():
            controlMode = True
            await message.channel.send(f"control mode on")

        if 'kys' in message.content.lower():
            await message.channel.send("are you sure?(yes/no)")
            kmsMode = True
        if kmsMode:
            if 'yes' in message.content.lower():
                await message.channel.send("alright bet **kms**, im dead")
                with open("memorynoun.txt", "w", encoding="utf-8") as file___:
                    file___.write(str(noun))
                    file___.close()
                with open("memoryverb.txt", "w", encoding="utf-8") as file_:
                    file_.write(str(verb))
                    file_.close()
                with open("memoryadjective.txt", "w", encoding="utf-8") as file__:
                    file__.write(str(adjective))
                    file__.close()
                exit(1)
            if 'no' in message.content.lower():
                await message.channel.send("oh okay")
                kmsMode = False
        while controlMode:
            if 'stfu' not in message.content.lower():
                _message = input("message: ")
                await message.channel.send(_message)
            else:
                controlMode = False
                print("off")
                await message.channel.send(f"control mode off")

    if message.author == client.user and not controlMode:
        return

    if 'test' in message.content.lower() and not learningMode and not controlMode:
        await message.channel.send("auto send test")
        for i in range(1, 4):
            await message.channel.send(str(i))
        await message.channel.send(f"test pass <@{message.author.id}>")

    if learningMode:
        sentence_ = str(message.content).split()
        sentence = ""
        for n in range(1, len(sentence_)):
            sentence += sentence_[n] + " "
        print(sentence)
        tokens = nltk.word_tokenize(sentence)
        pos_tags = nltk.pos_tag(tokens)
        for i in pos_tags:
            if "VB" in i[1]:
                verb.append(i[0])
            if "NN" in i[1]:
                noun.append(i[0])
            if "JJ" in i[1]:
                adjective.append(i[0])
            if "PRP" in i[1]:
                noun.append(i[0])
        print("noun:", noun)
        print("verb:", verb)
        print("adjective:", adjective)
        if len(noun) >= 10 and len(verb) >= 10 and (random.randint(0, 1) == 0 or "forcetalk" in sentence.lower()):
            if random.randint(0, 3) == 0 or len(adjective) < 10:  # SVN
                await message.channel.send(random.choice(noun) + " " + random.choice(verb) + " " + random.choice(noun))
            elif len(adjective) >= 10:  # SVAN
                await message.channel.send(random.choice(noun) + " " + random.choice(verb) + " " + random.choice(adjective) + " " + random.choice(noun))

client.run(TOKEN)
