from telethon.tl.functions.channels import LeaveChannelRequest
from uniborg.util import admin_cmd
import time

@borg.on(admin_cmd("q", outgoing=True))

async def q(e):

    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("Goodbye.")

        time.sleep(3)

        if '-' in str(e.chat_id):
            await borg(LeaveChannelRequest(e.chat_id))
        else:
            await e.edit('That\'s not a chat!')
