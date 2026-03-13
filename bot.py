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

@app.on_message(filters.command("savemsg"))
async def save_source_messages(_, m: Message):
    """
    Save messages from source channel to database
    Usage: /savemsg (send in source channel)
    """
    try:
        chat = m.chat
        
        # Check if this is the source channel
        if chat.id != cfg.SOURCE_CHANNEL:
            await m.reply_text("❌ This command can only be used in the source channel!")
            return
        
        # Clear previous messages
        clear_messages()
        
        processing = await m.reply_text("🔄 **Saving messages from source channel...**")
        
        saved_count = 0
        message_count = 0
        
        # Get last 100 messages (or adjust limit)
        async for message in app.get_chat_history(chat.id, limit=100):
            message_count += 1
            try:
                # Prepare message data
                message_data = {
                    "message_id": message.id,
                    "chat_id": chat.id,
                    "date": message.date.isoformat() if message.date else None,
                }
                
                # Store message content based on type
                if message.text:
                    message_data["type"] = "text"
                    message_data["text"] = message.text
                    if message.entities:
                        message_data["entities"] = [{
                            "type": e.type,
                            "offset": e.offset,
                            "length": e.length,
                            "url": e.url,
                            "user_id": e.user.id if e.user else None,
                            "custom_emoji_id": e.custom_emoji_id
                        } for e in message.entities]
                
                elif message.photo:
                    message_data["type"] = "photo"
                    message_data["file_id"] = message.photo.file_id
                    message_data["caption"] = message.caption
                    if message.caption_entities:
                        message_data["caption_entities"] = [{
                            "type": e.type,
                            "offset": e.offset,
                            "length": e.length,
                            "url": e.url,
                            "user_id": e.user.id if e.user else None,
                            "custom_emoji_id": e.custom_emoji_id
                        } for e in message.caption_entities]
                
                elif message.sticker:
                    message_data["type"] = "sticker"
                    message_data["file_id"] = message.sticker.file_id
                    message_data["emoji"] = message.sticker.emoji
                
                elif message.animation:
                    message_data["type"] = "animation"
                    message_data["file_id"] = message.animation.file_id
                    message_data["caption"] = message.caption
                    if message.caption_entities:
                        message_data["caption_entities"] = [{
                            "type": e.type,
                            "offset": e.offset,
                            "length": e.length,
                            "url": e.url,
                            "user_id": e.user.id if e.user else None,
                            "custom_emoji_id": e.custom_emoji_id
                        } for e in message.caption_entities]
                
                elif message.video:
                    message_data["type"] = "video"
                    message_data["file_id"] = message.video.file_id
                    message_data["caption"] = message.caption
                    if message.caption_entities:
                        message_data["caption_entities"] = [{
                            "type": e.type,
                            "offset": e.offset,
                            "length": e.length,
                            "url": e.url,
                            "user_id": e.user.id if e.user else None,
                            "custom_emoji_id": e.custom_emoji_id
                        } for e in message.caption_entities]
                
                elif message.document:
                    message_data["type"] = "document"
                    message_data["file_id"] = message.document.file_id
                    message_data["file_name"] = message.document.file_name
                    message_data["caption"] = message.caption
                    if message.caption_entities:
                        message_data["caption_entities"] = [{
                            "type": e.type,
                            "offset": e.offset,
                            "length": e.length,
                            "url": e.url,
                            "user_id": e.user.id if e.user else None,
                            "custom_emoji_id": e.custom_emoji_id
                        } for e in message.caption_entities]
                
                # Save to database
                if save_message(message_data):
                    saved_count += 1
                
            except Exception as e:
                print(f"Error saving message {message.id}: {e}")
        
        await processing.edit_text(
            f"✅ **Messages saved successfully!**\n\n"
            f"📊 **Statistics:**\n"
            f"📝 Messages processed: {message_count}\n"
            f"💾 Messages saved: {saved_count}"
        )
        
    except Exception as e:
        await m.reply_text(f"❌ Error: {str(e)}")

#-------------------------------------------------------------------------
@app.on_message(filters.command("s"))
async def send_stored_messages(_, m: Message):
    """
    Sends stored messages from database to current chat
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
        
        # Get stored messages from database
        stored_messages = get_all_messages()
        
        if not stored_messages:
            await m.reply_text("❌ No messages found in database! Use /savemsg in source channel first.")
            await asyncio.sleep(5)
            await m.delete()
            return
        
        # Send processing message
        processing_msg = await m.reply_text(f"🔄 **Sending {len(stored_messages)} stored messages...**")
        
        success_count = 0
        failed_count = 0
        
        # Send each stored message
        for msg_data in stored_messages:
            try:
                await send_stored_message(msg_data, chat.id)
                success_count += 1
                await asyncio.sleep(1)  # Delay to avoid flood
                
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await send_stored_message(msg_data, chat.id)
                    success_count += 1
                except:
                    failed_count += 1
                    
            except Exception as e:
                print(f"Failed to send message: {e}")
                failed_count += 1
        
        # Send final summary
        await processing_msg.edit_text(
            f"✅ **Sending completed!**\n\n"
            f"📊 **Statistics:**\n"
            f"📝 Total messages: {len(stored_messages)}\n"
            f"✅ Successfully sent: {success_count}\n"
            f"❌ Failed: {failed_count}\n"
            f"🎯 Target: {chat.title}"
        )
        
        # Auto delete command after completion
        await asyncio.sleep(10)
        await m.delete()
        
    except Exception as e:
        await m.reply_text(f"❌ Error: {str(e)}")
        print(f"Error in /s command: {e}")
        await asyncio.sleep(5)
        await m.delete()


async def send_stored_message(msg_data: dict, target_chat_id: int):
    """
    Send a stored message to target chat
    """
    msg_type = msg_data.get("type")
    
    # Text message
    if msg_type == "text":
        text = msg_data.get("text")
        entities = msg_data.get("entities")
        
        # Reconstruct entities if they exist
        if entities:
            message_entities = []
            for e in entities:
                if e["type"] == "custom_emoji":
                    message_entities.append(
                        enums.MessageEntity(
                            type=enums.MessageEntityType.CUSTOM_EMOJI,
                            offset=e["offset"],
                            length=e["length"],
                            custom_emoji_id=e["custom_emoji_id"]
                        )
                    )
                else:
                    message_entities.append(
                        enums.MessageEntity(
                            type=e["type"],
                            offset=e["offset"],
                            length=e["length"],
                            url=e.get("url"),
                            user_id=e.get("user_id")
                        )
                    )
            
            await app.send_message(
                target_chat_id,
                text=text,
                entities=message_entities
            )
        else:
            await app.send_message(target_chat_id, text)
    
    # Photo with caption
    elif msg_type == "photo":
        file_id = msg_data.get("file_id")
        caption = msg_data.get("caption")
        caption_entities = msg_data.get("caption_entities")
        
        if caption_entities:
            await app.send_photo(
                target_chat_id,
                file_id,
                caption=caption,
                caption_entities=[enums.MessageEntity(**e) for e in caption_entities]
            )
        else:
            await app.send_photo(target_chat_id, file_id, caption=caption)
    
    # Sticker
    elif msg_type == "sticker":
        file_id = msg_data.get("file_id")
        await app.send_sticker(target_chat_id, file_id)
    
    # Animation/GIF
    elif msg_type == "animation":
        file_id = msg_data.get("file_id")
        caption = msg_data.get("caption")
        caption_entities = msg_data.get("caption_entities")
        
        if caption_entities:
            await app.send_animation(
                target_chat_id,
                file_id,
                caption=caption,
                caption_entities=[enums.MessageEntity(**e) for e in caption_entities]
            )
        else:
            await app.send_animation(target_chat_id, file_id, caption=caption)
    
    # Video
    elif msg_type == "video":
        file_id = msg_data.get("file_id")
        caption = msg_data.get("caption")
        caption_entities = msg_data.get("caption_entities")
        
        if caption_entities:
            await app.send_video(
                target_chat_id,
                file_id,
                caption=caption,
                caption_entities=[enums.MessageEntity(**e) for e in caption_entities]
            )
        else:
            await app.send_video(target_chat_id, file_id, caption=caption)
    
    # Document
    elif msg_type == "document":
        file_id = msg_data.get("file_id")
        caption = msg_data.get("caption")
        caption_entities = msg_data.get("caption_entities")
        
        if caption_entities:
            await app.send_document(
                target_chat_id,
                file_id,
                caption=caption,
                caption_entities=[enums.MessageEntity(**e) for e in caption_entities]
            )
        else:
            await app.send_document(target_chat_id, file_id, caption=caption)

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
