import aiohttp
import os
from pathlib import Path

async def fetch_and_save_image(grno):
    api_url = f"https://student.marwadiuniversity.ac.in:553/handler/getImage.ashx?SID={grno}"
    output_path = f"./images/image_{grno}.png"
    
    Path("./images").mkdir(exist_ok=True)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    with open(output_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            f.write(chunk)
                else:
                    raise Exception(f"HTTP error! status: {response.status}")
    except Exception as error:
        print(f"Error fetching image: {error}")
        raise error
