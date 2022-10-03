#    Arch Linux Repository Search Tool
#    Copyright (C) 2022 SsNiPeR1

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import logging
import requests
import json

from .. import loader, utils, security

logger = logging.getLogger(__name__)


@loader.tds
class ARSMod(loader.Module):
    """Arch Linux Repository Search Tool"""
    strings = {"name": "ArchRepoSearch"}

    @loader.unrestricted
    async def versioncmd(self, message):
        """Get the version of a package
        .arv <package>"""
        args = utils.get_args(message)
        if await self.allmodules.check_security(message, security.OWNER | security.SUDO):
            try:
                package = args[0]
                repo = args[1]
            except IndexError as e:
                await message.edit(f"<b>Some error occured:</b> <code>{e}</code>")
                return
        
        r = requests.get(f"https://www.archlinux.org/packages/{repo}/{package}/json/").text
        data = json.loads(r)

        await message.edit(data['pkgver'])