import discord
import platform
import time
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands import CheckFailure, check
import asyncio
import aiosqlite
from datetime import datetime
OWNER_ID = 267410788996743168

class devtools(commands.Cog):
    """
    Dev commands. thats really it
    """
    def __init__(self,bot):
        self.bot = bot
    
    async def cog_check(self,ctx):
        return ctx.author.id == OWNER_ID
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            logchannel = await self.bot.fetch_channel(798016167163723776)
            guildstatvc = await self.bot.fetch_channel(798014995496960000)
            playerstatvc = await self.bot.fetch_channel(809977048868585513)
            await guildstatvc.edit(name=f"Guilds: {len(self.bot.guilds)}")
            userstatvc = await self.bot.fetch_channel(798018451330433044)
            await userstatvc.edit(name=f"Users: {len(self.bot.users)}")
            c = await self.bot.db.execute("SELECT COUNT(*) FROM e_users")
            total_db_users = await c.fetchone()
            await playerstatvc.edit(name=f"Players (in DB): {total_db_users[0]}")
            
            
            ts = self.bot.utc_calc(str(guild.created_at))
            msg = f"""New guild pog: ```prolog
Guild:           {guild.name}
ID:              {guild.id}
Owner:           {str(guild.owner)}
Region:          {guild.region}
Members:         {guild.member_count}
Boosters:        {len(guild.premium_subscribers)}
Boost level:     {guild.premium_tier}
Channels:        {len(guild.channels)}
Roles:           {len(guild.roles)}
Filesize limit:  {guild.filesize_limit}
Desc:            {(guild.description or 'None')}
Created:         {ts[0]} days, {ts[1]} hours, {ts[2]} minutes, {ts[3]} seconds ago
Emoji limit:     {guild.emoji_limit}```
            """
            await logchannel.send(msg)
        except Exception as e:
            dev = await self.bot.fetch_user(267410788996743168)
            await dev.send(e)
        
    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
        try:
            logchannel = await self.bot.fetch_channel(798016167163723776)
            guildstatvc = await self.bot.fetch_channel(798014995496960000)
            playerstatvc = await self.bot.fetch_channel(809977048868585513)
            await guildstatvc.edit(name=f"Guilds: {len(self.bot.guilds)}")
            userstatvc = await self.bot.fetch_channel(798018451330433044)
            await userstatvc.edit(name=f"Users: {len(self.bot.users)}")
            c = await self.bot.db.execute("SELECT COUNT(*) FROM e_users")
            total_db_users = await c.fetchone()
            await playerstatvc.edit(name=f"Players (in DB): {total_db_users[0]}")
            
            ts = self.bot.utc_calc(str(guild.created_at))
            msg = f"""Fuck, we lost a guild: ```prolog
Guild:           {guild.name}
ID:              {guild.id}
Owner:           {str(guild.owner)}
Region:          {guild.region}
Members:         {guild.member_count}
Boosters:        {len(guild.premium_subscribers)}
Boost level:     {guild.premium_tier}
Channels:        {len(guild.channels)}
Roles:           {len(guild.roles)}
Filesize limit:  {guild.filesize_limit}
Desc:            {(guild.description or 'None')}
Created:         {ts[0]} days, {ts[1]} hours, {ts[2]} minutes, {ts[3]} seconds ago
Emoji limit:     {guild.emoji_limit}```
            """
            await logchannel.send(msg)
        except Exception as e:
            dev = await self.bot.fetch_user(267410788996743168)
            await dev.send(e)
        
    @tasks.loop(minutes=10)
    async def database_backup_task(self):
        try:
            await self.bot.db.commit()
            self.bot.backup_db = await aiosqlite.connect('ecox_backup.db')
            await self.bot.db.backup(self.bot.backup_db)
            await self.bot.backup_db.commit()
            await self.bot.backup_db.close()
            return
        except Exception as e:
            print(f"An error occured while backing up the database:\n`{e}`")
            return
    
    @commands.group(invoke_without_command=True,hidden=True)
    async def dev(self, ctx):
        #bot dev commands
        await ctx.send("`You're missing one of the below arguements:` ```md\n- reload\n- loadall\n- status <reason>\n- ban <user> <reason>\n```")

    @dev.command(aliases=["r","reloadall"])
    async def reload(self, ctx):
        output = ""
        amount_reloaded = 0
        async with ctx.channel.typing():
            for e in self.bot.initial_extensions:
                try:
                    self.bot.reload_extension(e)
                    amount_reloaded += 1
                except Exception as e:
                    e = str(e)
                    output = output + e + "\n"
            await asyncio.sleep(1)
            if output == "":
                await ctx.send(content=f"`{len(self.bot.initial_extensions)} cogs succesfully reloaded.`") # no output = no error
            else:
                await ctx.send(content=f"`{amount_reloaded} cogs were reloaded, except:` ```\n{output}```") # output
    
    @dev.command(aliases=["us"])
    async def updatestats(self, ctx):
        async with ctx.channel.typing():
            logchannel = await self.bot.fetch_channel(798016167163723776)
            guildstatvc = await self.bot.fetch_channel(798014995496960000)
            playerstatvc = await self.bot.fetch_channel(809977048868585513)
            await guildstatvc.edit(name=f"Guilds: {len(self.bot.guilds)}")
            userstatvc = await self.bot.fetch_channel(798018451330433044)
            await userstatvc.edit(name=f"Users: {len(self.bot.users)}")
            c = await self.bot.db.execute("SELECT COUNT(*) FROM e_users")
            total_db_users = await c.fetchone()
            await playerstatvc.edit(name=f"Players (in DB): {total_db_users[0]}")
        await ctx.send("Updated support server stats.")

    @dev.command(aliases=["load","l"])
    async def loadall(self, ctx):
        output = ""
        amount_loaded = 0
        async with ctx.channel.typing():
            for e in self.bot.initial_extensions:
                try:
                    self.bot.load_extension(e)
                    amount_loaded += 1
                except Exception as e:
                    e = str(e)
                    output = output + e + "\n"
            await asyncio.sleep(1)
            if output == "":
                await ctx.send(content=f"`{len(self.bot.initial_extensions)} cogs succesfully loaded.`") # no output = no error
            else:
                await ctx.send(content=f"`{amount_loaded} cogs were loaded, except:` ```\n{output}```") # output

    @dev.command()
    async def status(self, ctx, *, text):
        # Setting `Playing ` status
        if text is None:
            await ctx.send(f"{ctx.guild.me.status}")
        if len(text) > 60:
            await ctx.send("`Too long you pepega`")
            return
        try:
            await self.bot.change_presence(activity=discord.Game(name=text))
            await ctx.message.add_reaction("\U00002705")
        except Exception as e:
            await ctx.message.add_reaction("\U0000274c")
            await ctx.send(f"`{e}`")

    @dev.command()
    async def stop(self, ctx):
        askmessage = await ctx.send("`you sure?`")
        def check(m):
            newcontent = m.content.lower()
            return newcontent == 'yea' and m.channel == ctx.channel and m.author.id == OWNER_ID
        try:
            await self.bot.wait_for('message', timeout=5, check=check)
        except asyncio.TimeoutError:
            await askmessage.edit(content="`Timed out. haha why didnt you respond you idiot`")
        else:
            await ctx.send("`bye`")
            print(f"Bot is being stopped by {ctx.message.author} ({ctx.message.id})")
            await self.bot.db.commit()
            await self.bot.db.close()
            await self.bot.logout()
        
    @dev.group(invoke_without_command=True)
    async def sql(self, ctx):
        await ctx.send("`Youre missing one of the below params:` ```md\n- fetchone\n- fetchall\n- run\n```") 
            
    @sql.command()
    async def fetchone(self, ctx, *, statement):
        try:
            c = await self.bot.db.execute(statement)
            data = await c.fetchone()
            await self.bot.db.commit()
            await ctx.send(data)
        except Exception as e:
            await ctx.send(f"```sql\n{e}\n```")
            
    @sql.command()
    async def fetchall(self, ctx, *, statement):
        try:
            c = await self.bot.db.execute(statement)
            data = await c.fetchall()
            await self.bot.db.commit()
            await ctx.send(data)
        except Exception as e:
            await ctx.send(f"```sql\n{e}\n```")
    @sql.command()
    async def run(self, ctx, *, statement):
        try:
            c = await self.bot.db.execute(statement)
            await self.bot.db.commit()
            await ctx.message.add_reaction(emoji="\U00002705")
        except Exception as e:
            await ctx.send(f"```sql\n{e}\n```")
            
    @dev.group(invoke_without_command=True)
    async def eco(self, ctx):
        pass
    
    @eco.command()
    async def reset(self, ctx, user: discord.User = None):
        if user is None:
            await ctx.send("Provide an user")
            return
        player = await self.bot.get_player(user.id)
        if player is None:
            await ctx.send("They're not even in the database...")
            return
        
        await self.bot.db.execute("UPDATE e_users SET bal = 100 WHERE id = ?",(user.id,))
        await ctx.send("Reset.")
        
    @eco.command()
    async def give(self, ctx, user: discord.User, amount):
        amount = float(amount)
        player = await self.bot.get_player(user.id)
        if player is None:
            await ctx.send("They're not even in the database...")
            return
        
        await self.bot.db.execute("UPDATE e_users SET bal = (bal + ?) WHERE id = ?",(amount, user.id,))
        await ctx.send(f"Success.\nNew balance: ${(player[3] + amount)}")
    
    @eco.command(name="set")
    async def setamount(self, ctx, user: discord.User = None, amount: float = None):
        if user is None:
            await ctx.send("Provide an user.")
            return
        if amount is None:
            await ctx.send("Provide an amount.")
        player = await self.bot.get_player(user.id)
        if player is None:
            await ctx.send("They're not even in the database...")
            return
        
        await self.bot.db.execute("UPDATE e_users SET bal = ? WHERE id = ?",(amount, user.id,))
        await ctx.send("Success.")
        
    @dev.command(aliases=["bu"])
    async def backup(self, ctx):
        try:
            await self.bot.db.commit()
            self.bot.backup_db = await aiosqlite.connect('ecox_backup.db')
            await self.bot.db.backup(self.bot.backup_db)
            await self.bot.backup_db.commit()
            await self.bot.backup_db.close()
            await ctx.send("done, lol")
            return
        except Exception as e:
            await ctx.send(f"An error occured while backing up the database:\n`{e}`")
            return
        
    @dev.command(hidden=True,name="stream")
    async def streamingstatus(self, ctx, *, name):
        if ctx.author.id != 267410788996743168:
            return
        await self.bot.change_presence(activity=discord.Streaming(name=name,url="https://twitch.tv/monstercat/"))
        await ctx.send("aight, done")
        
    @dev.command()
    async def m(self, ctx):
        if self.bot.maintenance:
            self.bot.maintenance = False
            return await ctx.send("Maintenence is now off.")
        else:
            self.bot.maintenance = True
            return await ctx.send("Maintenence is now on.")
def setup(bot):
    bot.add_cog(devtools(bot))