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


def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


@loader.tds
class ColorMod(loader.Module):
    """Color Visualizer"""
    strings = {"name": "ColorVisualizer"}

    def download_file(url):
        local_filename = url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename

    @loader.unrestricted
    async def colorcmd(self, message):
        """Draw a color.\n.color <color hex>"""
        args = utils.get_args(message)
        color = args[0].lstrip('#')
        lv = len(color)
        c = tuple(int(color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        if not os.path.exists("Inconsolata.ttf"):
            download_file("https://raw.githubusercontent.com/SsNiPeR1/ftg-modules/main/Inconsolata.ttf")
        fontfile = ImageFont.truetype("Inconsolata.ttf", 48)
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
        await message.edit(file=io)
