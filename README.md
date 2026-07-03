# Discord.py — Components V2 Full Documentation

An in-depth reference guide for designing rich, modern Discord bot UIs using **Components V2** within discord.py.

---

## Table of Contents

1. [What is Components V2?](#what-is-components-v2)
2. [Requirements & Setup](#requirements--setup)
3. [Core Concept — LayoutView](#core-concept--layoutview)
4. [Component Reference](#component-reference)
   - [Container](#container)
   - [TextDisplay](#textdisplay)
   - [Separator](#separator)
   - [Section](#section)
   - [Thumbnail](#thumbnail)
   - [MediaGallery](#mediagallery)
   - [ActionRow](#actionrow)
   - [Button](#button)
   - [Select (Dropdown)](#select-dropdown)
   - [File](#file)
5. [Handling File Attachments](#handling-file-attachments)
6. [Building Layouts](#building-layouts)
7. [Interaction Handling](#interaction-handling)
8. [Full Examples](#full-examples)
   - [Avatar Command](#example-1-avatar-command)
   - [Help Menu with Dropdown](#example-2-help-menu-with-dropdown)
   - [User Info Card](#example-3-user-info-card)
   - [Confirmation Prompt](#example-4-confirmation-prompt)
   - [File Distribution Board](#example-5-file-distribution-board)
9. [Common Patterns & Tips](#common-patterns--tips)
10. [Known Limitations](#known-limitations)

---

## What is Components V2?
**Components V2** represents Discord's advanced message component system. It empowers bots to transmit structured, visually polished messages employing a **layout-based framework** rather than traditional plain embeds.

### Key Differences: Classic Embeds vs. Components V2
| Feature | Classic Embeds | Components V2 |
|---|---|---|
| Layout Control | Highly Limited | Absolute (Containers, Rows) |
| Interactive Elements | Kept outside the embed | Inline inside containers |
| Image Display | Fixed Thumbnail/Image | Dynamic MediaGallery Component |
| Text Formatting | Strict field-based | Flexible TextDisplay markdown |
| Sections | Unsupported | Supported via Section + Thumbnail |

In discord.py, Components V2 implementations utilize discord.ui.LayoutView and its corresponding architectural components inside discord.ui.

---

## Requirements & Setup
Ensure your local framework is fully updated before starting.
```bash
pip install discord.py

```
**Important:** Components V2 demands **discord.py 2.4+**. Ensure you verify your library version.

### Bot Intents Configuration
Your bot initialization requires the following core configurations:
```python
intents = discord.Intents.default()
intents.message_content = True  # Mandatory for standard prefix commands and attachments processing

bot = commands.Bot(command_prefix="!", intents=intents)
```

### Essential Imports
```python
import discord
from discord.ext import commands
from discord import ui
from discord.ui import (
    LayoutView,
    Container,
    Section,
    TextDisplay,
    Separator,
    MediaGallery,
    Thumbnail,
    ActionRow,
    Button,
    Select,
    File,
)
from discord import SelectOption
```

---

## Core Concept — LayoutView
The LayoutView serves as the foundational **root layer** for every Components V2 construction. Consider it the structural canvas holding all primary layout configurations.
```python
class MyView(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=120)  # Lifespan in seconds (None for infinite)
        
        # Build your layout hierarchy here
        container = ui.Container(accent_color=None) # Left border hidden
        container.add_item(ui.TextDisplay("Hello, world!"))
        
        self.add_item(container)  # Mount container onto the LayoutView
```
Deploying the view into a channel:
```python
view = MyView()
await ctx.send(view=view)
```

### LayoutView Parameters
| Parameter | Type | Description |
|---|---|---|
| timeout | float | None | Lifespan before listeners deactivate. Default: 180. Set to None for persistent execution. |

### Structural Utility Methods
```python
self.clear_items()          # Flushes all child components from the view context
self.add_item(component)    # Appends a top-level component layer
await interaction.response.edit_message(view=self)  # Refreshes active UI contents
```

---

## Component Reference
### Container
A **Container** acts as a structural housing box to bind multiple layout elements seamlessly. It stands as the fundamental interface block.
```python
container = ui.Container(
    *children,          # Direct components insertion or populated via .add_item()
    accent_color=None,  # Pass discord.Color / hex int for left border. Set to None to explicitly remove the vertical left border!
    spoiler=False,      # Toggles spoiler blur content protections
    id=None             # Optional unique numerical identifier
)
```

#### Population Strategies:
 * **Method A: Constructor-Defined**
```python
container = ui.Container(
    ui.TextDisplay("Line 1"),
    ui.TextDisplay("Line 2"),
    accent_color=None # Removes left border
)
```
 * **Method B: Sequential Append**
```python
container = ui.Container(accent_color=None)
container.add_item(ui.TextDisplay("Line 1"))
container.add_item(ui.TextDisplay("Line 2"))
```

#### Border Accent Visuals:
```python
# Utilizing explicit accent coloring
container = ui.Container(
    ui.TextDisplay("This features a defined blue vertical border."),
    accent_color=discord.Color.blue()
)

# Stripping down the border completely
clean_container = ui.Container(
    ui.TextDisplay("This box features NO vertical left border outline."),
    accent_color=None
)
```

### TextDisplay
Renders complex **markdown texts** natively inside layout elements, acknowledging standard formatting.
```python
ui.TextDisplay("Your content string here")
```

#### Markdown Formatting Syntaxes:
```python
ui.TextDisplay("# Header 1")
ui.TextDisplay("## Header 2")
ui.TextDisplay("### Header 3")
ui.TextDisplay("**Bolded Text** and *Italics* alongside __Underlines__")
ui.TextDisplay("> Blockquote text block entries")
ui.TextDisplay("`inline formatting syntax`")
ui.TextDisplay("-# Tiny subtext notation layouts")
```

#### Variable-Driven Expressions:
```python
ui.TextDisplay(f"**Target Member:** {member.name}")
ui.TextDisplay(f"**Ident ID:** `{member.id}`")
ui.TextDisplay(f"**Join Timestamp:** <t:{int(member.joined_at.timestamp())}:R>")
```

### Separator
Draws a clean **horizontal separation partition line** between structural layouts for improved visual ergonomics.
```python
ui.Separator(
    spacing=ui.SeparatorSpacing.small,  # Options include: .small, .large
    visible=True                         # Set False for invisible spacing gaps
)
```

```python
container = ui.Container(
    ui.TextDisplay("Block Alpha"),
    ui.Separator(),                          # Active division line
    ui.TextDisplay("Block Beta"),
    ui.Separator(visible=False),             # Blank structural gap spacing
    ui.TextDisplay("Block Gamma"),
    accent_color=None
)
```

### Section
A **Section** arranges structural content horizontally, enabling regular texts on the left-hand partition and accessories fixed to the right-hand side.
```python
ui.Section(
    *text_components,   # TextDisplay items allocated to left frame
    accessory=...,      # An accessory component (Button, Thumbnail) locked to the right side
    id=None
)
```

```python
section = ui.Section(
    ui.TextDisplay("### Community Announcement Page"),
    ui.TextDisplay("Explore internal infrastructure guides updates."),
    accessory=ui.Thumbnail(
        media=discord.UnfurledMediaItem(url="[https://example.com/logo.png](https://example.com/logo.png)"),
        description="Guild Mark Logo"
    )
)
```

### Thumbnail
A specialized **compact asset image** mapped as an accessory exclusively inside a parent Section.
```python
ui.Thumbnail(
    media=discord.UnfurledMediaItem(url="https://..."),
    description="Alternative text fields",   # Accessibility alt text
    spoiler=False
)
```

```python
ui.Thumbnail(
    media=discord.UnfurledMediaItem(url=member.display_avatar.url),
    description=f"User avatar portrait for {member.name}"
)
```

**Constraint:** A Thumbnail element cannot exist independently; it must be mapped inside the accessory field of a Section.

### MediaGallery
Assembles and structures **multiple image blocks** in an orderly presentation configuration within containers.
```python
gallery = ui.MediaGallery()
gallery.add_item(
    media="[https://example.com/photo.png](https://example.com/photo.png)",   
    description="Alt markup string description",                  
    spoiler=False                            
)
```

#### Uploading Local Asset Attaches:
```python
gallery = ui.MediaGallery()
gallery.add_item(media="attachment://profile.png")
```

Execution dispatch call:
```python
await ctx.send(
    view=view,
    files=[discord.File(image_buffer, filename="profile.png")]
)
```

**Capacity:** A singular MediaGallery can bundle up to **10 images** collectively.
### ActionRow
A dedicated **horizontal interface container row** designated for user interaction controls like Buttons and Select Dropdowns.
```python
row = ui.ActionRow(
    ui.Button(label="Proceed", style=discord.ButtonStyle.primary),
    ui.Button(label="Cancel", style=discord.ButtonStyle.secondary),
)
```

**Limitation:** An individual ActionRow accepts a maximum capacity of **5 Buttons** OR **1 Select dropdown instance**. It cannot bundle both types concurrently.

### Button
Clickable action nodes mapped inside active ActionRow elements or as accessories inside ui.Section.
```python
ui.Button(
    label="Interactive Trigger",            
    style=discord.ButtonStyle.primary,      
    custom_id="unique_callback_id",         # Callback identifier matching
    url="https://...",                      # For external link redirection (Link style only)
    emoji="🛡️",                             
    disabled=False,                         
    row=None
)
```

#### Interactive Button Styles:
| Style Variant | Visual Tint | Primary Intent |
|---|---|---|
| discord.ButtonStyle.primary | Blue | Standard prominent workflows |
| discord.ButtonStyle.secondary | Grey | Secondary neutral utilities |
| discord.ButtonStyle.success | Green | Successful confirmation steps |
| discord.ButtonStyle.danger | Red | Destructive workflows/Deletions |
| discord.ButtonStyle.link | Grey + Arrow | External network navigation redirection |

#### Setting Interactive Callbacks:
```python
btn = ui.Button(label="Accept Terms", style=discord.ButtonStyle.success, custom_id="accept_id")

async def accept_callback(interaction: discord.Interaction):
    await interaction.response.send_message("Terms validated successfully.", ephemeral=True)

btn.callback = accept_callback
```

### Select (Dropdown)
Interactive menus providing structured list item selection arrays.
```python
ui.Select(
    placeholder="Identify destination hub...",
    min_values=1,
    max_values=1,
    options=[
        discord.SelectOption(label="Tier A", value="t1", description="First class access", emoji="🥇"),
        discord.SelectOption(label="Tier B", value="t2", description="Standard class access", emoji="🥈"),
    ],
    custom_id="select_tier_dropdown",
    disabled=False
)
```

#### Select Options Callback Executions:
```python
self.dropdown = ui.Select(
    placeholder="Choose your path...",
    options=[
        discord.SelectOption(label="Admin Settings", value="adm"),
        discord.SelectOption(label="User Settings", value="usr"),
    ]
)
self.dropdown.callback = self.on_dropdown_select

async def on_dropdown_select(self, interaction: discord.Interaction):
    selected_value = self.dropdown.values[0]
    await interaction.response.edit_message(content=f"Redirecting to: {selected_value}")
```

### File
Renders a raw attachment downloable box directly inside your structured UI container layer.
```python
ui.File(media="attachment://filename.ext")
```

Unlike text links, this reserves an absolute, dedicated download frame native to Discord's interface.

---

## Handling File Attachments
Components V2 allows you to bind downloadable attachments directly inside container layers through the attachment:// URI namespace.

### Implementation Rules:
 1. **The Transport Array (files=[...])**: You must provide the raw upload payload using standard discord.File objects attached directly to the message context wrapper (channel.send or ctx.send).
 2. **The Layout Link (media="attachment://...")**: Inside the ui.File or ui.MediaGallery construction, map the media value to point matching the exact string filename of your transport array item.

---

## Building Layouts
### Architecture Mapping Overview
```
LayoutView
└── Container (accent_color=None removes left border decoration)
    ├── TextDisplay
    ├── Separator
    ├── Section
    │   ├── TextDisplay (Left positioning alignment)
    │   └── Thumbnail / Button (Right partition accessory layout)
    ├── MediaGallery
    │   └── Image Collections
    ├── Separator
    ├── File Component (Download card anchor)
    └── ActionRow
        ├── Button Instance
        └── Button Instance
```

### Component Nesting Constraints
| Parent Element Layer | Permitted Internal Child Components |
|---|---|
| LayoutView | Container instances exclusively (Top structural baseline) |
| Container | TextDisplay, Separator, Section, MediaGallery, File, ActionRow |
| Section | TextDisplay components (Left) + Accessory component (Right Side) |
| ActionRow | Up to **5 Buttons** OR Exactly **1 Select Dropdown** control |
| MediaGallery | Managed imagery child blocks via .add_item() methods |

**Important Architecture Guardrail:** Containers **cannot** be nested inside other Containers.

---

## Interaction Handling
### Restricting Actions to Command Instigators
Incorporate the interaction_check routine to prevent non-author interaction:
```python
class RestrictedView(ui.LayoutView):
    def __init__(self, author: discord.Member):
        super().__init__(timeout=60)
        self.author = author

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "Access Denied: This dashboard belongs to another user.", ephemeral=True
            )
            return False
        return True
```

### Dynamic Component Redraw Layout Tasks
```python
async def on_refresh_trigger(self, interaction: discord.Interaction):
    # Clear preexisting state
    self.clear_items()
    
    # Rebuild structural elements cleanly from the base up
    updated_container = ui.Container(
        ui.TextDisplay("## State Updated Successfully!"),
        ui.TextDisplay("System properties have altered configuration states."),
        accent_color=None # Keeps the profile box layout clean with zero left borders
    )
    self.add_item(updated_container)
    
    # Commit variations to live visual message components
    await interaction.response.edit_message(view=self)
```

---

## Full Examples
### Example 1: Avatar Command
```python
import discord
from discord.ext import commands
from discord import ui
from typing import Optional
import requests
from io import BytesIO


class AvatarManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avatar", aliases=["pfp"])
    async def avatar_command(self, ctx, member: Optional[discord.Member] = None):
        member = member or ctx.author
        avatar = member.display_avatar

        is_animated = avatar.is_animated()
        fmt = "gif" if is_animated else "png"
        filename = f"avatar.{fmt}"

        response = requests.get(avatar.replace(size=1024, format=fmt).url)
        avatar_data = BytesIO(response.content)

        class AvatarView(ui.LayoutView):
            def __init__(self):
                super().__init__()

                png_url  = member.display_avatar.replace(size=1024, format="png").url
                jpg_url  = member.display_avatar.replace(size=1024, format="jpg").url

                gallery = ui.MediaGallery()
                gallery.add_item(media=f"attachment://{filename}")

                btn_png  = ui.Button(label="PNG Asset",  style=discord.ButtonStyle.link, url=png_url)
                btn_jpg  = ui.Button(label="JPG Asset",  style=discord.ButtonStyle.link, url=jpg_url)
                button_row = ui.ActionRow(btn_png, btn_jpg)

                container = ui.Container(
                    ui.TextDisplay(f"# Profile: {member.name}"),
                    ui.Separator(),
                    ui.TextDisplay(f"**System Identification:** `{member.id}`"),
                    gallery,
                    ui.Separator(),
                    button_row,
                    accent_color=None # Strip out vertical lines to ensure a clean photo look
                )
                self.add_item(container)

        await ctx.send(
            view=AvatarView(),
            files=[discord.File(avatar_data, filename=filename)]
        )

async def setup(bot):
    await bot.add_cog(AvatarManager(bot))
```

### Example 2: Help Menu with Dropdown
```python
import discord
from discord.ext import commands
from discord import ui, SelectOption

MODULES = {
    "Admin": ["`ban`", "`kick`", "`clear`"],
    "Public": ["`ping`", "`info`", "`help`"]
}

class InteractiveHelpView(ui.LayoutView):
    def __init__(self, bot: commands.Bot, author: discord.Member):
        super().__init__(timeout=120)
        self.bot = bot
        self.author = author
        self._render_home_layer()

    def _render_home_layer(self):
        self.clear_items()

        self.dropdown = ui.Select(
            placeholder="Browse system tools modules...",
            options=[SelectOption(label=k, value=k) for k in MODULES.keys()]
        )
        self.dropdown.callback = self.on_selection_callback

        section = ui.Section(
            ui.TextDisplay("### 🛠️ Help Desk Matrix"),
            ui.TextDisplay("Toggle dropdown menus to access specific module listings."),
            accessory=ui.Thumbnail(
                media=discord.UnfurledMediaItem(url=self.bot.user.display_avatar.url),
                description="Core Client Visual"
            )
        )

        container = ui.Container(
            section,
            ui.Separator(),
            ui.ActionRow(self.dropdown),
            accent_color=None # Zero vertical borders for cleaner menu integrations
        )
        self.add_item(container)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author.id

    async def on_selection_callback(self, interaction: discord.Interaction):
        selected_mod = self.dropdown.values[0]
        self.clear_items()

        # Re-initialize control state assets
        self.dropdown = ui.Select(
            placeholder="Select another category...",
            options=[SelectOption(label=k, value=k, default=(k == selected_mod)) for k in MODULES.keys()]
        )
        self.dropdown.callback = self.on_selection_callback

        container = ui.Container(
            ui.TextDisplay(f"### 📂 Module: {selected_mod}"),
            ui.TextDisplay(" ".join(MODULES[selected_mod])),
            ui.Separator(),
            ui.ActionRow(self.dropdown),
            accent_color=None
        )
        self.add_item(container)
        await interaction.response.edit_message(view=self)

class HelpCore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_call(self, ctx):
        await ctx.send(view=InteractiveHelpView(self.bot, ctx.author))

async def setup(bot):
    await bot.add_cog(HelpCore(bot))
```

### Example 3: User Info Card
```python
import discord
from discord.ext import commands
from discord import ui
from typing import Optional

class UserIdentityCard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="userinfo")
    async def user_info_lookup(self, ctx, member: Optional[discord.Member] = None):
        member = member or ctx.author
        
        class IdentityCardView(ui.LayoutView):
            def __init__(self):
                super().__init__()
                
                section = ui.Section(
                    ui.TextDisplay(f"# Summary Card: {member.display_name}"),
                    ui.TextDisplay(f"**Account Handle:** {member.name}"),
                    accessory=ui.Thumbnail(
                        media=discord.UnfurledMediaItem(url=member.display_avatar.url),
                        description="Target Portrait"
                    )
                )
                
                # Dynamically utilize color borders or cleanly strip it depending on preference
                container = ui.Container(
                    section,
                    ui.Separator(),
                    ui.TextDisplay(f"**Join Timestamp:** <t:{int(member.joined_at.timestamp())}:D>"),
                    accent_color=member.color if member.color.value else None # Reverts to none (no border) if user has default color rules
                )
                self.add_item(container)
                
        await ctx.send(view=IdentityCardView())

async def setup(bot):
    await bot.add_cog(UserIdentityCard(bot))
```

### Example 4: Confirmation Prompt
```python
import discord
from discord.ext import commands
from discord import ui

class OperationalPromptView(ui.LayoutView):
    def __init__(self, author: discord.Member, description_string: str):
        super().__init__(timeout=30)
        self.author = author
        self.desc = description_string
        self._compile_prompt()

    def _compile_prompt(self):
        self.clear_items()
        
        yes_btn = ui.Button(label="Confirm Operation", style=discord.ButtonStyle.success)
        no_btn  = ui.Button(label="Abort Operation", style=discord.ButtonStyle.danger)
        
        yes_btn.callback = self.confirm_execution
        no_btn.callback  = self.abort_execution
        
        container = ui.Container(
            ui.TextDisplay("## ⚠️ System Authorization Gateway Request"),
            ui.Separator(),
            ui.TextDisplay(f"Pending Operation: **{self.desc}**"),
            ui.Separator(),
            ui.ActionRow(yes_btn, no_btn),
            accent_color=discord.Color.gold() # Warning indicator color assignment
        )
        self.add_item(container)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author.id

    async def confirm_execution(self, interaction: discord.Interaction):
        self.clear_items()
        resolved_container = ui.Container(
            ui.TextDisplay("## ✅ System Notice: Executed successfully"),
            accent_color=None # Clears side border layout presentation cleanly
        )
        self.add_item(resolved_container)
        await interaction.response.edit_message(view=self)

    async def abort_execution(self, interaction: discord.Interaction):
        self.clear_items()
        resolved_container = ui.Container(
            ui.TextDisplay("## ❌ System Notice: Operation Aborted"),
            accent_color=None
        )
        self.add_item(resolved_container)
        await interaction.response.edit_message(view=self)
```

### Example 5: File Distribution Board
```python
import os
import discord
from discord.ext import commands
from discord import ui

BANNER_FILENAME = "1000371960.jpg"

class SendView(ui.LayoutView):
    def __init__(self, author: discord.Member, user_filename: str) -> None:
        super().__init__(timeout=120)
        self.author = author

        container = ui.Container(accent_color=None)
        
        # Banner local attachment image placement
        banner_gallery = ui.MediaGallery()
        banner_gallery.add_item(media=f"attachment://{BANNER_FILENAME}")
        container.add_item(banner_gallery)
        
        container.add_item(ui.Separator())
        container.add_item(ui.TextDisplay("## Components V2 Test"))
        container.add_item(ui.Separator())
        
        # Split section alignments
        youtube_button = ui.Button(label="Link", style=discord.ButtonStyle.link, url="[https://youtube.com](https://youtube.com)")
        youtube_section = ui.Section(ui.TextDisplay("[YouTube](https://youtube.com)"), accessory=youtube_button)
        container.add_item(youtube_section)
        
        container.add_item(ui.Separator())
        container.add_item(ui.TextDisplay("Tải File"))
        
        # Dynamic uploaded attachment slot anchor mapping
        file_component = ui.File(media=f"attachment://{user_filename}")
        container.add_item(file_component)
        
        self.add_item(container)

@commands.command(name="send")
async def send_command(ctx: commands.Context, channel: discord.TextChannel) -> None:
    if not ctx.message.attachments:
        await ctx.send("❌ Please attach a file to this command message!")
        return

    user_attachment = ctx.message.attachments[0]
    user_file = await user_attachment.to_file()
    banner_file = discord.File(BANNER_FILENAME, filename=BANNER_FILENAME)
    
    view = SendView(author=ctx.author, user_filename=user_attachment.filename)
    await channel.send(view=view, files=[banner_file, user_file])
```

---

## Common Patterns & Tips
### Clearing Left Side Border Outlines Explicitly
To omit the vertical accent border frame element natively present inside ui.Container layouts, explicitly define accent_color=None during initialization inside your execution calls.

### Dropdown Refresh Persistent Callbacks
When rebuilding active components layout blocks via state mutations or selection triggers, verify that you explicitly assign the .callback hook logic property to freshly instantiated dropdown arrays before committing edits.

### Disabling Controls After Interaction
```python
async def on_button_click(self, interaction: discord.Interaction):
    self.clear_items()
    halt_btn = ui.Button(label="Session Resolved", style=discord.ButtonStyle.secondary, disabled=True)
    container = ui.Container(
        ui.TextDisplay("Task complete."),
        ui.ActionRow(halt_btn),
        accent_color=None
    )
    self.add_item(container)
    await interaction.response.edit_message(view=self)
```

---

## Known Limitations
| System Rules Framework | Architecture Restrictions |
|---|---|
| **Zero Container Nesting Operations** | You cannot place any Container within another Container object block. |
| **Section Confined Accessories** | Section layouts require a defined interactive/visual element passed to the accessory slot parameter. |
| **ActionRow Allocation Ceilings** | Enforces caps of 5 interactive Button configurations OR 1 independent Dropdown menu set exclusively. |
| **MediaGallery Volumes Constraints** | Galleries can house up to a maximum volume of 10 image indexes. |
| **No Mix-and-Match Processing** | Components V2 layouts cannot be combined or dispatched together with classic Embed layers inside the same payload message execution context. |

**Tip:** Always test your layouts in a development server first. Discord sometimes updates component rendering behavior, and layouts that look fine in one Discord client version may appear slightly different in another.

---

# Author
Lino
