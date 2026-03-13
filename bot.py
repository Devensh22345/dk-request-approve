from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters, Client, errors, enums
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg 
import random, asyncio

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

txt1 = ['**𝐇𝐞𝐥𝐥𝐨 𝐈 𝐚𝐦 𝐚 𝐀𝐧𝐢𝐦𝐞 𝐏𝐫𝐨𝐯𝐢𝐝𝐞𝐫 𝐁𝐨𝐭 𝐛𝐲 [@DK_ANIMES]**']
txt2 = [
    '<b><blockquote> 𝐂𝐥𝐢𝐜𝐤 𝐇𝐞𝐫𝐞 𝐭𝐨 𝐆𝐞𝐭 𝐀𝐧𝐢𝐦𝐞 𝐢𝐧 𝐇𝐢𝐧𝐝𝐢 \n𝐉𝐮𝐬𝐭 𝐂𝐥𝐢𝐜𝐤 𝐨𝐧 👇👇 </blockquote>\n /START</b>'
]

@app.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approve(_, m: Message):
    try:
        op = m.chat
        kk = m.from_user
        await app.approve_chat_join_request(op.id, kk.id)  # Automatically approve the request
        print(f"Approved join request from {kk.id} in {op.id}")

        add_group(op.id)
        add_user(kk.id)

        img = "https://envs.sh/elk.jpg"

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("𝐂𝐥𝐢𝐜𝐤 𝐡𝐞𝐫𝐞 𝐓𝐨 𝐖𝐚𝐭𝐜𝐡/𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐢𝐧 𝐇𝐢𝐧𝐝𝐢 👀", url="https://t.me/leeeeeeeeeeeeeeeeeechbot?start=hi")],
                [InlineKeyboardButton("𝐍𝐞𝐰 𝐚𝐧𝐢𝐦𝐞 𝐢𝐧 𝐇𝐢𝐧𝐝𝐢", url="https://t.me/leeeeeeeeeeeeeeeeeechbot?start=hi")],
            ]
        )

        await app.send_message(kk.id, random.choice(txt1))
        await app.send_message(kk.id, random.choice(txt2))
        await app.send_photo(
            kk.id,
            img,
            caption="<b><blockquote>𝐂𝐥𝐢𝐜𝐤 𝐨𝐧 𝐁𝐞𝐥𝐨𝐰 𝐁𝐮𝐭𝐭𝐨𝐧 𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐘𝐨𝐮𝐫 𝐄𝐩𝐢𝐬𝐨𝐝𝐞 👇👇👇👇</blockquote></b>",
            reply_markup=keyboard
        )

    except errors.PeerIdInvalid:
        print("User hasn't started the bot yet.")
    except Exception as err:
        print(f"Error: {err}")


@app.on_message(filters.command("start"))
async def start(_, m: Message):
    try:
        user = m.from_user

        if m.chat.type == enums.ChatType.PRIVATE:
            add_user(user.id)
            await m.reply_photo(
                "https://envs.sh/elk.jpg",
                caption=f"<b><blockquote>𝐂𝐥𝐢𝐜𝐤 𝐨𝐧 𝐓𝐡𝐞 𝐚𝐧𝐢𝐦𝐞 𝐍𝐚𝐦𝐞 \n𝐓𝐨 𝐃𝐢𝐫𝐞𝐜𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐘𝐨𝐮𝐫 𝐀𝐧𝐢𝐦𝐞.🔥🔥</blockquote></b>",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("💁‍♂️ Start me private 💁‍♂️", url="https://t.me/leeeeeeeeeeeeeeeeeechbot?start=hi")]]
                )
            )

        elif m.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            add_group(m.chat.id)
            await m.reply_text(f"**🦊 Hello {user.first_name}!\nWrite me in private for more details**")

        print(f"{user.first_name} started the bot!")

    except Exception as err:
        print(f"Error: {err}")


@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}` """)


@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success, failed, deactivated, blocked = 0, 0, 0, 0

    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            await m.reply_to_message.copy(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(e)
            failed += 1

    await lel.edit(f"✅Successfully sent to `{success}` users.\n❌ Failed to `{failed}` users.\n👾 `{blocked}` Blocked users.\n👻 `{deactivated}` Deactivated users.")


@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success, failed, deactivated, blocked = 0, 0, 0, 0

    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            await m.reply_to_message.forward(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(e)
            failed += 1

    await lel.edit(f"✅Successfully forwarded to `{success}` users.\n❌ Failed to `{failed}` users.\n👾 `{blocked}` Blocked users.\n👻 `{deactivated}` Deactivated users.")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------send msg ---------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.on_message(filters.command("s"))
async def copy_channel_messages(_, m: Message):
    """
    Copies all messages from source channel to current chat
    Usage: /s (send in target group/channel where bot is admin)
    """
    try:
        # Check if bot is admin in the current chat
        chat = m.chat
        bot_member = await app.get_chat_member(chat.id, "me")
        
        if bot_member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            await m.reply_text("❌ I need to be an admin in this chat to send messages!")
            await asyncio.sleep(5)
            await m.delete()
            return
        
        # Check if source channel is configured
        if not hasattr(cfg, 'SOURCE_CHANNEL') or not cfg.SOURCE_CHANNEL:
            await m.reply_text("❌ SOURCE_CHANNEL is not configured in configs.py!")
            await asyncio.sleep(5)
            await m.delete()
            return
        
        # Send processing message
        processing_msg = await m.reply_text("🔄 **Copying messages from source channel...**")
        
        try:
            # Get source channel info
            source_chat = await app.get_chat(cfg.SOURCE_CHANNEL)
            
            # Count messages
            message_count = 0
            success_count = 0
            failed_count = 0
            
            # Get all messages from source channel
            async for message in app.get_chat_history(source_chat.id, limit=1000):  # Adjust limit as needed
                message_count += 1
                try:
                    # Copy message without forward tag
                    await copy_message_without_forward(message, chat.id)
                    success_count += 1
                    
                    # Small delay to avoid flood limits
                    await asyncio.sleep(0.5)
                    
                except FloodWait as e:
                    # Handle flood wait
                    await asyncio.sleep(e.value)
                    # Retry the message
                    try:
                        await copy_message_without_forward(message, chat.id)
                        success_count += 1
                    except:
                        failed_count += 1
                        
                except Exception as e:
                    print(f"Failed to copy message {message.id}: {e}")
                    failed_count += 1
            
            # Send final summary
            await processing_msg.edit_text(
                f"✅ **Copying completed!**\n\n"
                f"📊 **Statistics:**\n"
                f"📝 Total messages: {message_count}\n"
                f"✅ Successfully copied: {success_count}\n"
                f"❌ Failed: {failed_count}\n"
                f"📢 Source: {source_chat.title}\n"
                f"🎯 Target: {chat.title}"
            )
            
        except errors.ChannelInvalid:
            await processing_msg.edit_text("❌ Invalid source channel! Make sure bot is a member of the source channel.")
        except errors.ChatAdminRequired:
            await processing_msg.edit_text("❌ Bot needs to be admin in source channel to read messages!")
        except Exception as e:
            await processing_msg.edit_text(f"❌ Error accessing source channel: {str(e)}")
        
        # Auto delete command after completion
        await asyncio.sleep(10)
        await m.delete()
        
    except Exception as e:
        await m.reply_text(f"❌ Error: {str(e)}")
        print(f"Error in /s command: {e}")
        await asyncio.sleep(5)
        await m.delete()


async def copy_message_without_forward(message: Message, target_chat_id: int):
    """
    Helper function to copy message without forward tag
    Supports: text, media, stickers, premium emojis
    """
    try:
        # Text message with entities (including premium emojis)
        if message.text or message.caption:
            text = message.text or message.caption
            entities = message.entities or message.caption_entities
            
            if message.media:
                # Media with caption
                await message.copy(
                    target_chat_id,
                    caption=text,
                    caption_entities=entities,
                    parse_mode=enums.ParseMode.HTML
                )
            else:
                # Plain text message
                await app.send_message(
                    target_chat_id,
                    text=text,
                    entities=entities,
                    parse_mode=enums.ParseMode.HTML
                )
        
        # Sticker
        elif message.sticker:
            await app.send_sticker(
                target_chat_id,
                message.sticker.file_id
            )
        
        # Animation (GIF)
        elif message.animation:
            await app.send_animation(
                target_chat_id,
                message.animation.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities
            )
        
        # Video
        elif message.video:
            await app.send_video(
                target_chat_id,
                message.video.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                duration=message.video.duration,
                width=message.video.width,
                height=message.video.height,
                thumb=message.video.thumbs[0].file_id if message.video.thumbs else None
            )
        
        # Photo
        elif message.photo:
            await app.send_photo(
                target_chat_id,
                message.photo.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities
            )
        
        # Document
        elif message.document:
            await app.send_document(
                target_chat_id,
                message.document.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities
            )
        
        # Audio
        elif message.audio:
            await app.send_audio(
                target_chat_id,
                message.audio.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                duration=message.audio.duration,
                performer=message.audio.performer,
                title=message.audio.title
            )
        
        # Voice
        elif message.voice:
            await app.send_voice(
                target_chat_id,
                message.voice.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                duration=message.voice.duration
            )
        
        # Video Note
        elif message.video_note:
            await app.send_video_note(
                target_chat_id,
                message.video_note.file_id,
                duration=message.video_note.duration,
                length=message.video_note.length
            )
        
        # Poll
        elif message.poll:
            await app.send_poll(
                target_chat_id,
                question=message.poll.question,
                options=[opt.text for opt in message.poll.options],
                is_anonymous=message.poll.is_anonymous,
                type=message.poll.type,
                allows_multiple_answers=message.poll.allows_multiple_answers,
                correct_option_id=message.poll.correct_option_id,
                explanation=message.poll.explanation,
                explanation_entities=message.poll.explanation_entities,
                open_period=message.poll.open_period,
                close_date=message.poll.close_date
            )
        
        # Contact
        elif message.contact:
            await app.send_contact(
                target_chat_id,
                phone_number=message.contact.phone_number,
                first_name=message.contact.first_name,
                last_name=message.contact.last_name,
                vcard=message.contact.vcard
            )
        
        # Location
        elif message.location:
            await app.send_location(
                target_chat_id,
                latitude=message.location.latitude,
                longitude=message.location.longitude,
                horizontal_accuracy=message.location.horizontal_accuracy,
                live_period=message.location.live_period,
                heading=message.location.heading,
                proximity_alert_radius=message.location.proximity_alert_radius
            )
        
        # Venue
        elif message.venue:
            await app.send_venue(
                target_chat_id,
                latitude=message.venue.location.latitude,
                longitude=message.venue.location.longitude,
                title=message.venue.title,
                address=message.venue.address,
                foursquare_id=message.venue.foursquare_id,
                foursquare_type=message.venue.foursquare_type
            )
        
        # Game
        elif message.game:
            await app.send_game(
                target_chat_id,
                game_short_name=message.game.short_name
            )
        
        # Default: try to copy using generic method
        else:
            await message.copy(target_chat_id)
            
    except Exception as e:
        print(f"Error in copy_message_without_forward: {e}")
        raise e


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------create link ---------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.on_message(filters.command("p"))
async def create_invite_link(_, m: Message):
    """
    Creates invite links for channels/groups and sends them to the link channel
    Usage: /p (send this command in the channel/group where bot is admin)
    """
    try:
        # Check if bot is admin in the chat
        chat = m.chat
        bot_member = await app.get_chat_member(chat.id, "me")
        
        if bot_member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            await m.reply_text("❌ I need to be an admin in this chat to create invite links!")
            # Auto delete command after 5 seconds
            await asyncio.sleep(1)
            await m.delete()
            return
        
        # Check if link channel is configured
        if not hasattr(cfg, 'LINK_CHANNEL') or not cfg.LINK_CHANNEL:
            await m.reply_text("❌ LINK_CHANNEL is not configured in configs.py!")
            # Auto delete command after 5 seconds
            await asyncio.sleep(1)
            await m.delete()
            return
        
        # Get user info safely
        creator_name = "Unknown"
        creator_mention = "Unknown User"
        
        if m.from_user:
            creator_name = m.from_user.first_name
            creator_mention = m.from_user.mention
        elif m.sender_chat:
            # If sent from a channel/anonymously
            creator_name = m.sender_chat.title
            creator_mention = f"@{m.sender_chat.username}" if m.sender_chat.username else m.sender_chat.title
        
        # Create invite link based on chat type
        if chat.type in [enums.ChatType.CHANNEL]:
            # For channels - create join request link
            try:
                # First, ensure bot has permission to invite users
                invite_link = await app.create_chat_invite_link(
                    chat.id,
                    creates_join_request=True,
                    name=f"Link created by {creator_name}"
                )
                link_type = "Channel (Join Request)"
                link = invite_link.invite_link
            except Exception as e:
                await m.reply_text(f"❌ Failed to create channel invite link: {str(e)}")
                # Auto delete command after 5 seconds
                await asyncio.sleep(1)
                await m.delete()
                return
                
        elif chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            # For groups - create normal invite link
            try:
                invite_link = await app.create_chat_invite_link(
                    chat.id,
                    name=f"Link created by {creator_name}"
                )
                link_type = "Group"
                link = invite_link.invite_link
            except Exception as e:
                await m.reply_text(f"❌ Failed to create group invite link: {str(e)}")
                # Auto delete command after 5 seconds
                await asyncio.sleep(1)
                await m.delete()
                return
        else:
            await m.reply_text("❌ This command can only be used in groups or channels!")
            # Auto delete command after 5 seconds
            await asyncio.sleep(1)
            await m.delete()
            return
        
        # Get chat information
        chat_info = await app.get_chat(chat.id)
        chat_title = chat_info.title
        chat_username = f"@{chat_info.username}" if chat_info.username else "No username"
        
        # Prepare message for link channel
        link_message = f"""
**𝗬𝗢𝗨𝗥 𝗥𝗘𝗤𝗨𝗘𝗦𝗧𝗘𝗗 𝗔𝗡𝗜𝗠𝗘:** 
**{chat_title}**

**𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗 𝗟𝗜𝗡𝗞:** 
**{link}**
**{link}**
        """
        
        # Send to link channel
        try:
            await app.send_message(
                cfg.LINK_CHANNEL,
                link_message,
                disable_web_page_preview=True
            )
            
        
            
            # Send confirmation to the user
            reply_msg = await m.reply_text(
                f"✅ **Invite link created and sent to link channel!**\n\n"
                f"📢 **Chat:** {chat_title}\n"
                f"🔗 **Link:** {link}",
                disable_web_page_preview=True
            )
            
            # Auto delete command and reply after 10 seconds
            await asyncio.sleep(1)
            await m.delete()  # Delete the command message
            await reply_msg.delete()  # Delete the reply message
            
        except Exception as e:
            await m.reply_text(f"❌ Failed to send to link channel: {str(e)}")
            # Auto delete command after 5 seconds
            await asyncio.sleep(5)
            await m.delete()
            
    except errors.ChatAdminRequired:
        await m.reply_text("❌ I need to be an admin in this chat to create invite links!")
        # Auto delete command after 5 seconds
        await asyncio.sleep(5)
        await m.delete()
    except Exception as e:
        error_msg = await m.reply_text(f"❌ Error: {str(e)}")
        print(f"Error in /p command: {e}")
        # Auto delete command and error message after 5 seconds
        await asyncio.sleep(5)
        await m.delete()
        await error_msg.delete()


print("I'm Alive Now!")
app.run()
