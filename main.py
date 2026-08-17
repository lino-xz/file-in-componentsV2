import os
import sys
import discord
from discord import ui
from discord.ext import commands

TOKEN = "YOUR_BOT_TOKEN"
PREFIX = "$"
BANNER_FILENAME = "1000371960.jpg"

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)


class SendView(ui.LayoutView):
    def __init__(self, user_filename: str):
        super().__init__(timeout=None)

        container = ui.Container()

        # Banner
        banner = ui.MediaGallery()
        banner.add_item(media=f"attachment://{BANNER_FILENAME}")
        container.add_item(banner)

        container.add_item(ui.Separator())

        # Header
        container.add_item(ui.TextDisplay("## Components V2 Test"))
        container.add_item(ui.Separator())

        # Link buttons
        container.add_item(ui.ActionRow(
            ui.Button(
                label="Server",
                style=discord.ButtonStyle.link,
                url="https://discord.gg/your-invite"
            ),
            ui.Button(
                label="YouTube",
                style=discord.ButtonStyle.link,
                url="https://youtube.com/@your-channel"
            )
        ))

        container.add_item(ui.Separator())

        # Uploaded file
        container.add_item(ui.TextDisplay("### Download File"))
        container.add_item(
            ui.File(media=f"attachment://{user_filename}")
        )

        self.add_item(container)


class Bot(commands.Bot):
    async def on_ready(self):
        print("=" * 50)
        print(f"[+] Logged in as {self.user} | ID: {self.user.id}")
        print("=" * 50)


bot = Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)


@bot.command(name="send")
async def send_command(
    ctx: commands.Context,
    channel: discord.TextChannel
):
    # Check for an uploaded file
    if not ctx.message.attachments:
        await ctx.send("❌ Please attach a file to this command message!")
        return

    # Check for the banner
    if not os.path.isfile(BANNER_FILENAME):
        await ctx.send(
            f"❌ Missing banner image `{BANNER_FILENAME}` in the bot folder!"
        )
        return

    attachment = ctx.message.attachments[0]

    # Prepare the files
    user_file = await attachment.to_file()
    banner_file = discord.File(
        BANNER_FILENAME,
        filename=BANNER_FILENAME
    )

    view = SendView(attachment.filename)

    # Send the Components V2 message
    await channel.send(
        view=view,
        files=[banner_file, user_file]
    )

    await ctx.send(
        f"✅ Component sent to {channel.mention}!",
        delete_after=5
    )


@send_command.error
async def send_command_error(
    ctx: commands.Context,
    error: commands.CommandError
):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "**Usage:** `$send <#channel>`\n"
            "Attach a file to this command message!"
        )


if __name__ == "__main__":
    if not TOKEN or TOKEN == "YOUR_BOT_TOKEN":
        print("[!] Bot token is not configured!")
        sys.exit(1)

    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("[!] Invalid bot token!")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[!] Bot stopped!")
        