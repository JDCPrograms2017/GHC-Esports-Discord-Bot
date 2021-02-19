import discord
from discord.ext import commands
from discord.utils import get
intents = discord.Intents.default()
intents.members = True

import csv

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
        #dm_message.add_field(name='Deleting messages from this chat', value='To delete messages from this chat that **I\'VE** sent, type !dmclear [number of messages to delete]', inline=False)
        dm_message.add_field(name='Introduction', value='Where to start? While there are commands you can test out here like !ping, I advise you being your journey in the #general chat in our server! Reach out and say hi!', inline=False)
        await channel.send(embed=dm_message)
    
    #NOT FUNCTIONAL  
    #@commands.command()
    #async def dmclear(self, ctx, amount = 5):
    #    dmchannel = ctx.channel.id
    #    async for message in 

    #These are the MAIN commands :)
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Your ping is: {round(self.bot.latency * 1000)}ms. And also... Pong!')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author.display_name}! Good to see you')

    #DISPLAYS SCHEDULES FOR T.N.G BASED ON INCLUDED .CSV FILE
    @commands.command(aliases=['sched', 'skej'])
    async def show_schedule(self, ctx, arg1):
        with open ("UNIFIED_titles_stats_schedule_-_Schedule.csv", newline='') as csvfile:
            rows = csv.reader(csvfile, delimiter=',')
            data = {}
            for row in rows:
                data[row[0]] = row[1:]

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

    #ROLE SPECIFIC - CLEARS DESIRED AMOUNT OF SENT MESSAGES IN A CHANNEL
    @commands.command()
    async def clear(self, ctx, amount = 5):
        check_role = get(ctx.message.guild.roles, name='Bot Moderator')
        if check_role not in ctx.author.roles:
            await ctx.channel.purge(limit=1)
            await ctx.send("You are missing the role: **Bot Moderator** to perform this action.")
        else:
            await ctx.channel.purge(limit = amount + 1)

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