from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "22207976"))
    API_HASH = getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = getenv("BOT_TOKEN", "7365852964:AAHUjd52KAVMZgTcX5Imv7NuVjoVsJ7o5Ic")
    FSUB = getenv("FSUB", "SDBotz")
    CHID = int(getenv("CHID", "-1000112234"))
    SUDO = list(map(int, getenv("SUDO", "6872968794").split()))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://Autofilterbot:Autofilterbot@cluster0.1oipdqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    LINK_CHANNEL = getenv("LINK_GROUP", "-1002301713536")  # Add your link group/channel ID here
    SOURCE_CHANNEL = getenv("SOURCE_CHANNEL", "-1003873892040")
cfg = Config()
