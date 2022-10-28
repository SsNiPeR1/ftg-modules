#    Color Visualizer
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

import logging
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
import requests

from .. import loader, utils, security

logger = logging.getLogger(__name__)



@loader.tds
class ColorMod(loader.Module):
    """Color Visualizer"""
    strings = {"name": "ColorVisualizer"}

    @loader.unrestricted
    async def colorcmd(self, message):
        """Draw a color.\n.color <color hex>"""
        args = utils.get_args(message)
        color = args[0].lstrip('#')
        lv = len(color)
        c = tuple(int(color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        req = requests.get("https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Regular.ttf?raw=true")
        fontfile = BytesIO(req.content)
        font = ImageFont.truetype(fontfile, 48)
        img = Image.new('RGB', (400, 200), (c[0], c[1], c[2]))
        d = ImageDraw.Draw(img)
        if int(color, 16) <= 6710886:
            fc = "white"
        else:
            fc = "black"
        d.text((380, 180), "#" + color, fill=fc, anchor="rs", font=font)
        io = BytesIO()
        img.save(io, "PNG")
        io.seek(0)
        await self._client.send_file(message.peer_id, file=io, caption=f"Color #{color}")
