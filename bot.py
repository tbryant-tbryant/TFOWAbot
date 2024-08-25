import os

import discord
from dotenv import load_dotenv
import time
import json

score_file = open('./time_records.json', "r+")
score_json = json.load(score_file)
#print(score_json)

members_in_voice = {}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents()
intents.voice_states = True
intents.messages = True
intents.guilds = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@tree.command(
    name="activity",
    description="Show top 5 active members",
    guild=discord.Object(id=373951871821283343)
)
async def activity_scoreboard(interaction):
    sorted_dict = sorted(score_json["scores"].items(), key=lambda kv: kv[1], reverse=True)
    #print(sorted_dict)
    message = discord.Embed(
        title="Top 5 most active members",
    )
    message.add_field(name=f"{sorted_dict[0][0]}", value=f"{int(sorted_dict[0][1] // 3600)} hours, {int(sorted_dict[0][1] % 3600 // 60)} minutes, {int(sorted_dict[0][1] % 3600 % 60 // 1)} seconds")
    message.add_field(name=f"{sorted_dict[1][0]}", value=f"{int(sorted_dict[1][1] // 3600)} hours, {int(sorted_dict[1][1] % 3600 // 60)} minutes, {int(sorted_dict[1][1] % 3600 % 60 // 1)} seconds")
    message.add_field(name=f"{sorted_dict[2][0]}", value=f"{int(sorted_dict[2][1] // 3600)} hours, {int(sorted_dict[2][1] % 3600 // 60)} minutes, {int(sorted_dict[2][1] % 3600 % 60 // 1)} seconds")
    message.add_field(name=f"{sorted_dict[3][0]}", value=f"{int(sorted_dict[3][1] // 3600)} hours, {int(sorted_dict[3][1] % 3600 // 60)} minutes, {int(sorted_dict[3][1] % 3600 % 60 // 1)} seconds")
    #message.add_field(name="5", value=f"{sorted_dict[4][0]}: {sorted_dict[4][1]}")
    await interaction.response.send_message(embeds=[message])

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=373951871821283343))
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_voice_state_update(member, before, after):
    #print(member)
    #print(before)
    #print(after)

    if before.channel is None and after.channel is not None:
        #print(f"{member} joined {after.channel}")
        members_in_voice[member.name] = time.time()
        print(members_in_voice)

    if before.channel is not None and after.channel is None:
        #print(f"{member} left {before.channel}")
        join_time = members_in_voice[member.name]
        duration = time.time() - join_time
        print(f"User was in voice channel for {duration} seconds")
        members_in_voice.pop(member.name)

        if member.name in score_json["scores"]:
            print("User exists in score file")
            score_json["scores"][member.name] += duration
        else:
            print("User does not exist in score file")
            score_json["scores"][member.name] = duration

        score_file.seek(0)
        json.dump(score_json, score_file, indent=4)
        score_file.truncate()

        print(score_json)



""" @client.event
async def on_message(message):
    print(message) """


client.run(TOKEN)