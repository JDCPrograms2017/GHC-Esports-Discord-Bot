import discord
from discord.ext import commands
from discord.utils import get
intents = discord.Intents.default()
intents.members = True

import csv

with open ("UNIFIED_titles_stats_schedule_-_Schedule.csv", newline='') as csvfile:
            rows = csv.reader(csvfile, delimiter=',')
            data = {}
            for row in rows:
                data[row[0]] = row[1:]
            
            data_string = ''
            for key in data:
                data_string = data_string + (f'**{key}**, ')
            

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

    #DISPLAYS SCHEDULES FOR T.N.G BASED ON INCLUDED .CSV FILE
    @commands.command(aliases=['sched', 'skej'])
    async def show_schedule(self, ctx, arg1 = None):
        if arg1 is None:
             await ctx.send(f'Missing argument! Please try one of these: {data_string}')
        else:
            embeded_schedule = discord.Embed(
                 title = '*Thursday Night Gaming - All-ages community gaming night - everyone is welcome!*',
                 description = f'**Schedule for {arg1}**',
                 colour = discord.Colour.blue()
            )

            embeded_schedule.set_footer(text='Produced by: GHC Esports Assistant')
            embeded_schedule.set_author(name='GHC Esports Bot')
            embeded_schedule.set_thumbnail(url=data[arg1][4])
            embeded_schedule.add_field(name='Date', value=f'{data[arg1][2]}, {data[arg1][0]} {data[arg1][1]} @ 6 P.M. PST', inline=True)
            embeded_schedule.add_field(name='Details', value=data[arg1][3], inline=True)
            await ctx.send(embed=embeded_schedule)

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

    #WORK IN PROGRESS - Adds and deletes events from Thursday Night Gaming schedule (and will export changes to .csv file and change the old one)
    """@commands.command(aliases=['tng_a', 'tnga'])
    async def tng_add(self, ctx, event_name, month, date, weekday, details, event_image_link = None):
        check_role = get(ctx.message.guild.roles, name='Bot Moderator')
        if check_role not in ctx.author.roles:
          await ctx.channel.purge(limit=1)
          await ctx.send("You are missing the role: **Bot Moderator** to perform this action.")  
        else:
            new_event_string = (f'{month},{date},{weekday},{details},{event_image_link}')
            data[event_name] = new_event_string

    @commands.command()
    async def tng_delete(self, ctx, event_name):
    """

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