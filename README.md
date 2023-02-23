# Swearword-Counter
A short swearword counter discord bot that's also a self bot

An instance of the bot will only work for **1** server, this bot is not meant to be deployed for public use!

**Setup ⚙️**
1. Import repository preferably to [Replit](https://replit.com/repls)
2. Download discord-py v 1.7.3 (`pip install discord-py==1.7.3`)
3. Copy your token and run it. ctrl/cmd+shift+i -> application -> Local Storage -> `https://discord.com` -> token
4. Add blacklisted words to `blacklisted.txt`
5. Setup a pinger to keep the bot alive, [UptimeRobot](https://uptimerobot.com/dashboard)

**Features ✨**
- Smart filtering, `badddd` -> `bad`
- Replace bad words with custom character, default is `#`
- Counter bad words for individual server members
- Show leaderboard for bad words
- Add new words using a command
- Wipe bad word data
- No invite permissions needed (selfbot)
- Automatic message intents, bypassed

**Commands 🤖**
- `!swears @user` Lists the swears of specified user
- `!banned` Lists all the banned words
- `!ban word` Ban a specific word (admin only)
- `!multiban word1 word2 word3` Bans a list of words (admin only)
- `!unban word` Unbans a word
- `!remove @user x` Removes x swears from specified users
- `!leaderboard` Shows the leaderboard for the server
