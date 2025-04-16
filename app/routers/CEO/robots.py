from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

async def robots(request: Request):
    robots_txt = """
    User-agent: *
    Disallow: /hello/
    Disallow: /login/
    Disallow: /create_auction/
    Allow: /
    
    Sitemap: https://torgi.monety.shop/sitemap.xml
    """
    return PlainTextResponse(robots_txt.strip())
