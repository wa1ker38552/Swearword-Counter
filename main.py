from discord.ext import commands
from collections import Counter
from database import Database
from alive import keepAlive
import os

client = commands.Bot(command_prefix='!', self_bot=True)

def contains_blacklisted(message):
  for word in open('blacklisted.txt', 'r').read().split('\n'):
    if word in message.lower() or word in ''.join(message.lower().split()) or word in ''.join(list(Counter(list(message.lower())).keys())):
      return True, word
  return False, None

@client.event
async def on_ready():
  print(client.user)

@client.event
async def on_message_edit(before, after):
  async for message in before.channel.history(limit=50):
    if message.id == before.id:
      c, w = contains_blacklisted(message.content)
      if c:
        db = Database().load()
        if str(message.author.id) in db:
          db[str(message.author.id)]['swears'] += 1
          db[str(message.author.id)]['words'].append(w)
          Database().set_key(str(message.author.id), db[str(message.author.id)])
        else:
          Database().set_key(str(message.author.id), {'swears': 1, 'words': [w]})
        await message.reply(f"That's a very naughty word ({w})")

@client.event
async def on_message(message):
  global target_server, admin
  if message.guild.id == target_server:
    if message.author != client.user:
      async for message in message.channel.history(limit=1): message_content = message.content
      if message_content.split()[0] == '!swears':
        user = message_content.split()[1].replace('<@', '').replace('>', '')
        db = Database().load()
        if user in db:
          lst = db[user]['words']
          word = max(set(lst), key=lst.count)
          iti = ' '.join(lst).count(word)
          await message.channel.send(f'> `{await client.fetch_user(int(user))}` has sworn `{db[user]["swears"]}` time(s). Their favorite swearword is `{word}` ({iti} times)')
        else:
          await message.channel.send(f'> `{await client.fetch_user(int(user))}` has not sweared yet')
      
      elif message_content == '!banned':
        await message.channel.send('```'+'\n'.join(open('blacklisted.txt', 'r').read().split('\n'))+'```')
      
      elif message_content.split()[0] == '!ban' and message.author.id in admin:
        word = message_content.split()[1]
        list = open('blacklisted.txt', 'r').read().split('\n')
        list.append(word)
        with open('blacklisted.txt', 'w') as file:
          file.write('\n'.join(list))
        await message.channel.send(f'> Blacklisted `{word}`')
      
      elif message_content.split()[0] == '!unban' and message.author.id in admin:
        word = message_content.split()[1]
        list = open('blacklisted.txt', 'r').read().split('\n')
        list.remove(word)
        with open('blacklisted.txt', 'w') as file:
          file.write('\n'.join(list))
        await message.channel.send(f'> Un-blacklisted `{word}`')
      
      elif message_content.split()[0] == '!multiban' and message.author.id in admin:
        words = message_content.split()[1:]
        list = open('blacklisted.txt', 'r').read().split('\n')
        list.extend(words)
        with open('blacklisted.txt', 'w') as file:
          file.write('\n'.join(list))
        await message.channel.send(f'> Blacklisted `{", ".join(words)}`')

      elif message_content.split()[0] == '!remove' and message.author.id in admin:
        user = message_content.split()[1].replace('<@', '').replace('>', '')
        db = Database().load()
        db[user]['swears'] -= int(message_content.split()[2])
        db[user]['words'] = db[user]['words'][:len(db[user]['words'])-int(message_content.split()[2])-1]
        Database().set_key(user, db[user])
        await message.channel.send(f'> Removed `{int(message_content.split()[2])}` swears from `{await client.fetch_user(int(user))}`')
      
      elif message_content == '!leaderboard':
        db = Database().load()
        users = [{'user': key, 'num': db[key]['swears']} for key in db]

        for a in range(len(users)-1):
          for b in range(len(users)-1):
            if users[b+1]['num'] > users[b]['num']:
              save = users[b+1]
              users[b+1] = users[b]
              users[b] = save

        if len(users) > 5: users = users[:5]
        users = [f'{i+1}. {await client.fetch_user(int(k["user"]))} with {k["num"]} swears' for i, k in enumerate(users)]
        await message.channel.send('```'+'\n'.join(users)+'```')
      else:
        c, w = contains_blacklisted(message_content)
        if c:
          db = Database().load()
          if str(message.author.id) in db:
            db[str(message.author.id)]['swears'] += 1
            db[str(message.author.id)]['words'].append(w)
            Database().set_key(str(message.author.id), db[str(message.author.id)])
          else:
            Database().set_key(str(message.author.id), {'swears': 1, 'words': [w]})
          await message.reply(f"That's a very naughty word ({w})")

keepAlive()
target_server = 0 # put target server as an int here
admin = [] # put your discord id as an int here
client.run('TOKEN', bot=False)
