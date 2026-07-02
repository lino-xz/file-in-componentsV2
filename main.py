import os
import discord
from discord import ui
from discord.ext import commands

BOT_TOKEN: str = "YOUR-BOT-TOKEN"
COMMAND_PREFIX: str = "!"
BANNER_FILENAME = "1000371960.jpg"

gateway_intents = discord.Intents.all()
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=gateway_intents, help_command=None)


class SendView(ui.LayoutView):
    def __init__(self, author: discord.Member, user_filename: str) -> None:
        super().__init__(timeout=120)
        self.author = author

        container = ui.Container(accent_color=None)  # Tạo Container + xoá viền bên trái
        
        # Ảnh Banner
        banner_gallery = ui.MediaGallery()
        banner_gallery.add_item(media=f"attachment://{BANNER_FILENAME}")
        container.add_item(banner_gallery)  # Nạp ảnh vào Container
        
        container.add_item(ui.Separator())  # Chèn đường kẻ ngang
        
        # Tiêu đề
        container.add_item(ui.TextDisplay("## Components V2 Test"))
        container.add_item(ui.Separator())  # Chèn đường kẻ ngang
        
        # YouTube button
        youtube_button = ui.Button(label="Link", style=discord.ButtonStyle.link, url="https://youtube.com/@your-channel")
        youtube_section = ui.Section(ui.TextDisplay("[YouTube](https://youtube.com/@your-channel)"), accessory=youtube_button)
        container.add_item(youtube_section)
        
        # Server button
        server_button = ui.Button(label="Link", style=discord.ButtonStyle.link, url="https://discord.gg/your-invite")
        server_section = ui.Section(ui.TextDisplay("[Server Support](https://discord.gg/your-invite)"), accessory=server_button)
        container.add_item(server_section)
        
        container.add_item(ui.Separator())  # Chèn đường kẻ ngang
        container.add_item(ui.TextDisplay("Tải File"))
        
        # 5. File đính kèm của người dùng
        file_component = ui.File(media=f"attachment://{user_filename}")
        container.add_item(file_component)
        
        self.add_item(container)
        

@bot.command(name="send")
async def send_command(ctx: commands.Context, channel: discord.TextChannel) -> None:
    # Kiểm tra file đính kèm
    if not ctx.message.attachments:
        await ctx.send("❌ Please attach a file to this command message!")
        return
        
    # Kiểm tra file ảnh banner
    if not os.path.exists(BANNER_FILENAME):
        await ctx.send(f"❌ Missing banner image file `{BANNER_FILENAME}` in bot folder!")
        return

    # Lấy file từ tin nhắn của user
    user_attachment = ctx.message.attachments[0]
    user_file = await user_attachment.to_file()
    
    # Lấy file ảnh banner
    banner_file = discord.File(BANNER_FILENAME, filename=BANNER_FILENAME)
    
    # Tạo View với tên file của user
    view = SendView(author=ctx.author, user_filename=user_attachment.filename)
    
    # Gửi sang kênh đã tag
    await channel.send(view=view, files=[banner_file, user_file])
    
    await ctx.send(f"✅ Component sent to {channel.mention}!", delete_after=5)
    # await ctx.message.delete()
    

@send_command.error
async def send_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("**Instructions:** `!send <#channel>` (and remember to attach the file to this message!)")
        

bot.run(BOT_TOKEN)
