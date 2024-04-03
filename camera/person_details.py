from urllib.request import urlopen

from PIL.Image import open
from aiohttp import ClientSession


async def main(persons_url):
    summary = []
    async with ClientSession() as session:
        async with session.get(persons_url) as response:
            data = await response.json()
            for result in data['results']:
                result['original_image'] = [open(urlopen(result['original_image']))]
                summary.append(result)
    return summary
