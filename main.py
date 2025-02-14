try:
    from config import *
except:
    print("Unable to find config.py")
    exit()

from config import prefix, token, server_id, admin_id, api_key, api_url, bot_id, self_bot
import discord
import requests
from pystyle import Colors, Colorate


intents = discord.Intents.default()
intents.message_content = True  # Read mensages

if self_bot:
    bot = discord.Client(intents=intents)  # Self-bot
else:
    bot = discord.Client(intents=discord.Intents.all(),  
                         help_command=None ) # Discord Bot

# UI components for regular bot
if not self_bot:
    from discord.ui import Button, View, Modal, TextInput



logo = rf"""
  ___         _                     
 | _ \__ _ __| |____ _ __ _ ___     
 |  _/ _` / _| / / _` / _` / -_)    $ Made by Marcos0747
 |_| \__,_\__|_\_\__,_\__, \___|    $ Tracking!!
                      |___/         
"""

def banner():
    print(Colorate.Horizontal(Colors.cyan_to_blue, logo, 1))

    # Check API Status
    headers = {
        'Content-Type': 'application/json',
        'aftership-api-key': api_key
    }
    try:
        response = requests.get(f'{api_url}/couriers', 
                                headers=headers, 
                                timeout=5)
        
        api_status = "✅ Working" if response.status_code == 200 else "❌ Not working"
    except requests.exceptions.RequestException:
        api_status = "❌ Not working"
    
    print(Colorate.Horizontal(Colors.cyan_to_blue,f"API Status: {api_status}"))

# ========== INTERACTIVE COMPONENTS (regular bot only) ==========
if not self_bot:
    class TrackModal(Modal):
        def __init__(self):
            super().__init__(title="Track Package")
            self.tracking_number = TextInput(label="Tracking Number", placeholder="Enter tracking number...")
            self.add_item(self.tracking_number)

        async def on_submit(self, interaction: discord.Interaction):
            await process_tracking(interaction.channel, self.tracking_number.value)

    async def process_tracking(channel, tracking_number):
        msg = await channel.send(f'⚙️ **Tracking:** `{tracking_number}`...')
        try:
            response = requests.get(
                f'{api_url}/trackings/{tracking_number}',
                headers={'aftership-api-key': api_key}  # Header should be this 
            )

            if response.status_code == 200:
                status = response.json()['data']['tracking']['tag']
                await msg.edit(content=f'📦 **Status:** {status}')
            else:
                await msg.edit(content='❌ **Tracking failed**')
        except Exception as e:
            await msg.edit(content=f'🔥 **Error: {str(e)}**')

    def create_help_view():
        view = View()
        # Invite button
        view.add_item(Button(label="Invite", url=f"https://discord.com/oauth2/authorize?client_id={bot_id}"))
        # Tracking button with modal
        track_btn = Button(label="Track Package", style=discord.ButtonStyle.primary)
        
        async def track_callback(interaction):
            await interaction.response.send_modal(TrackModal())
        
        track_btn.callback = track_callback
        view.add_item(track_btn)
        return view

# ========== COMMON FUNCTIONALITY ==========

@bot.event
async def on_ready():
    banner()
    print("\n" + Colorate.Horizontal(Colors.cyan_to_blue, f'{bot.user} connected!'))
    await bot.change_presence(activity=discord.Game(name=f"{prefix}help"))

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user or message.guild.id != server_id or message.author.id != admin_id:
        return

    # ========== REGULAR BOT MODE ==========
    if not self_bot:
        # Help command 
        if message.content.lower().startswith(prefix + "help"):
            embed = discord.Embed(title="Help",
                                   description="List of available commands:",
                                   color=0x00ff00)
            
            embed.add_field(name=f"`🧰` {prefix}help", 
                            value="**Shows this help message.**", 
                            inline=False)
            
            embed.add_field(name=f"`📦` {prefix}track <tracking_number>", 
                            value="**Track a package using its tracking number.**", 
                            inline=False)
            
            await message.reply(
                embed=embed,
                view=create_help_view()
            )

        # Track command
        if message.content.lower().startswith(prefix + "track"):
            args = message.content.split()
            if len(args) < 2:
                await message.reply(f"**Usage:** `{prefix}track <tracking_number>`")
                return
                
            await process_tracking(message.channel, args[1])

    # ========== SELF-BOT MODE ==========
    else:
        # Help command
        if message.content.lower().startswith(prefix + "help"):
            help_text = (
                "**Available Commands**\n\n"
                f"`{prefix}help` - Show this help\n"
                f"`{prefix}track <number>` - Direct tracking\n"
                f"`{prefix}secret` - Special command"
            )
            await message.reply(help_text)

        # Fast track command
        if message.content.lower().startswith(prefix + "track"):
            args = message.content.split()
            if len(args) < 2:
                await message.reply(f"**Usage:** `{prefix}track <number>`")
                return
                
            tracking_number = args[1]
            msg = await message.reply(f"🔍 **Searching** **{tracking_number}**...")
            
        try:
            response = requests.get(
                f'{api_url}/trackings/{tracking_number}',
                headers={'as-api-key': api_key},
                timeout=10  
            )
            response.raise_for_status()  # Error if HTTP != 200

            status = response.json()['data']['tracking']['tag']
            await msg.edit(content=f'📦 **Status:** {status}')

        except requests.exceptions.HTTPError:
            await msg.edit(content='❌ **Código de seguimiento no encontrado**')
        except requests.exceptions.Timeout:
            await msg.edit(content='⌛ **Tiempo de espera agotado**')
        except Exception as e:
            await msg.edit(content=f'🔥 **Error: {str(e)}**')

        # Self-bot exclusive command
        if message.content.lower().startswith(prefix + "secret"):
            await message.reply("🕶️ Secret feature activated!") # This is useful but...

bot.run(token)