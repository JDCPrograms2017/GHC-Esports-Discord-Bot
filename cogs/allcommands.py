import discord
from discord.ext import commands
from discord.utils import get
intents = discord.Intents.default()
intents.members = True

import sqlite3         

class AllCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    #Individual member DM commands & listeners
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await member.create_dm()
        
        dm_message = discord.Embed(
            title = 'Welcome to GHC Esports!',
            description = 'Thank you so very much for joining our GHC Esports Discord server! You will find that we are a fun and supportive community in all of your endeavors (But mostly gaming with us :))!',
            colour = discord.Colour.blue()
        )

        dm_message.set_footer(text='Produced by: GHC Esports Assistant')
        dm_message.set_thumbnail(url='https://pbs.twimg.com/profile_images/1248003912059088898/JG3hxY8r.jpg')
        dm_message.add_field(name='Introduction', value='Where to start? While there are commands you can test out here like !ping, I advise you begin your journey in the #general chat in our server! Reach out and say hi!', inline=False)
        dm_message.add_field(name='About me (GHC Esports Assistant)', value='I am still very new and very in-dev, but you can check out my functionality by typing !list_commands in any text-channel on our server! :)', inline=False)
        dm_message.add_field(name='NOTE', value='As far as the devs know... you cannot delete chat history with this bot, lol.', inline=False)
        await channel.send(embed=dm_message)
    

    #These are the MAIN commands :)
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Your ping is: {round(self.bot.latency * 1000)}ms. And also... Pong!')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author.display_name}! Good to see you')

    @commands.command()
    async def vouch(self, ctx, *, vouchee = None):
        if vouchee is None:
            await ctx.send(f'Yooo {ctx.author.display_name}, vouch for someone bruv!')
        else:
            await ctx.send(f'Yea, sure. I vouch for {vouchee}')

    #DISPLAYS SCHEDULES FOR T.N.G BASED ON INCLUDED .CSV FILE BUT CURRENTLY TRANSITIONING TO SQLITE
    @commands.command(aliases=['sched', 'skej'])
    async def show_schedule(self, ctx, *, arg1 = None):
        db = sqlite3.connect('TNG_Events.db')
        cursor = db.cursor()
        cursor.execute("SELECT EVENT_NAME FROM TNG_Events ORDER BY MONTHNUMB, DAY ASC")
        events = ""
        events_arr = []
        for event in cursor.fetchall():
            events = events + ("%s, " % (event))
            events_arr.append(("%s" % (event)))

        if arg1 is None:
            await ctx.send(f'Missing ***or invalid*** argument! Please try one of these: {events}')
        elif arg1 in events_arr:
            embeded_schedule = discord.Embed(
                 title = '*Thursday Night Gaming - All-ages community gaming night - Everyone is welcome!*',
                 description = f'**Schedule for {arg1}**',
                 colour = discord.Colour.blue()
            )
            #FOOTER
            embeded_schedule.set_footer(text='Produced by: GHC Esports Assistant')
            #AUTHOR
            embeded_schedule.set_author(name='GHC Esports Bot')
            #THUMBNAIL
            cursor.execute(f"SELECT THUMBNAIL_LINK FROM TNG_Events WHERE EVENT_NAME = '{arg1}' ORDER BY MONTHNUMB, DAY ASC")
            thumbnail = ("%s" % (cursor.fetchone()))
            embeded_schedule.set_thumbnail(url=thumbnail)
            #DATE
            cursor.execute(f"SELECT WEEKDAY FROM TNG_Events WHERE EVENT_NAME = '{arg1}' ORDER BY MONTHNUMB, DAY ASC")
            weekday = ("%s" % (cursor.fetchone()))
            cursor.execute(f"SELECT MONTH FROM TNG_Events WHERE EVENT_NAME = '{arg1}' ORDER BY MONTHNUMB, DAY ASC")
            month = ("%s" % (cursor.fetchone()))
            cursor.execute(f"SELECT DAY FROM TNG_Events WHERE EVENT_NAME = '{arg1}' ORDER BY MONTHNUMB, DAY ASC")
            day = ("%d" % (cursor.fetchone()))
            embeded_schedule.add_field(name='Date', value=f'{weekday}, {month} {day} @ 6 P.M. PST', inline=True)
            #COMMENTS/DETAILS
            cursor.execute(f"SELECT COMMENTS FROM TNG_Events WHERE EVENT_NAME = '{arg1}' ORDER BY MONTHNUMB, DAY ASC")
            comments = ("%s" % (cursor.fetchone()))
            embeded_schedule.add_field(name='Details', value=comments, inline=True)
            #SEND SCHEDULE
            await ctx.send(embed=embeded_schedule)
        else:
            await ctx.send(f'Missing ***or invalid*** argument! Please try one of these: {events}')
        
        #NEVER FORGET TO CLOSE CURSOR & DATABASE! YOU RISK MEMORY LEAKS!
        cursor.close()
        db.close()

    #ROLE SPECIFIC COMMANDS 
    #----------------------
    #CLEARS DESIRED AMOUNT OF SENT MESSAGES IN A CHANNEL
    @commands.command()
    async def clear(self, ctx, amount = 5):
        check_role = get(ctx.message.guild.roles, name='Bot Moderator')
        if check_role not in ctx.author.roles:
            await ctx.channel.purge(limit=1)
            await ctx.send("You are missing the role: **Bot Moderator** to perform this action.")
        else:
            await ctx.channel.purge(limit = amount + 1)

    @commands.command()
    async def kick(self, ctx, member: discord.Member = None, *, why = 'no specified reason, lol'):
        check_role = get(ctx.message.guild.roles, name='Bot Moderator')
        if check_role not in ctx.author.roles:
            await ctx.channel.purge(limit=1)
            await ctx.send("You are missing the role: **Bot Moderator** to perform this action.")
        else: 
            if member is None:
                await ctx.channel.purge(limit=1)
                await ctx.send('**Please specify user to kick**')
            else:
                await ctx.channel.purge(limit=1)
                await ctx.guild.kick(member, reason = why)
                await ctx.send(f'{member} has been kicked by {ctx.author.display_name} for **{why}**')

    #LISTS AVAILABLE COMMANDS
    @commands.command()
    async def list_commands(self, ctx):
        help_embed = discord.Embed(
            title = 'Commands',
            description = 'Here\'s a list of currently available commands!',
            colour = discord.Colour.blue()
        )

        help_embed.set_footer(text='Produced by: GHC Esports Assistant')
        help_embed.set_author(name='GHC Esports Bot')
        help_embed.set_thumbnail(url='http://4.bp.blogspot.com/-yL1-QHwlqhI/VlSW7jnFTXI/AAAAAAAAA9o/uD0yGmZz9uE/s1600/commandblock.jpg')
        help_embed.add_field(name='*PREFIX*', value='!', inline=False)
        help_embed.add_field(name='hello', value='A basic hello!', inline=False)
        help_embed.add_field(name='ping', value='You can check your ping with this! (We don\'t know what server it pings though...)', inline=False)
        help_embed.add_field(name='show_schedule [arg]', value='Shows our Thursday Night Gaming-specific schedule for the next upcoming event!', inline=False)
        help_embed.add_field(name='show_schedule **ALIASES**', value='skej [arg], sched [arg]', inline=False)


        await ctx.send(embed=help_embed)





def setup(bot):
    bot.add_cog(AllCommands(bot))