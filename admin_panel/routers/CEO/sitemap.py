from globals import *
from fastapi import FastAPI, Request
from fastapi.responses import Response
from datetime import datetime, timedelta
from ..auctionCRUD.short_get_all import *

async def sitemap():
    # Получаем текущую дату
    today = datetime.utcnow().date()
    
    # Пример функции для расчета динамических дат
    def format_date(date):
        return date.strftime("%Y-%m-%d")
    
    auctions = await short_get_all()
    urls = [
        {"loc": "https://torgi.monety.shop/", "lastmod": format_date(today), "changefreq": "daily", "priority": 1.0},
        {"loc": "https://example.com/about", "lastmod": format_date(today - timedelta(days=5)), "changefreq": "monthly", "priority": 0.8},
    ]
    
    for a in auctions:
        urls.append({
            "loc": f"https://torgi.monety.shop/alt_auction?a_id={a['a_id']}",
            "lastmod": format_date(today - timedelta(days=10)),  # Пример: дата обновления аукциона 10 дней назад
            "changefreq": "weekly",
            "priority": 0.9
        })
    
    # Генерация XML
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        sitemap_xml += f"  <url>\n"
        sitemap_xml += f"    <loc>{url['loc']}</loc>\n"
        sitemap_xml += f"    <lastmod>{url['lastmod']}</lastmod>\n"
        sitemap_xml += f"    <changefreq>{url['changefreq']}</changefreq>\n"
        sitemap_xml += f"    <priority>{url['priority']}</priority>\n"
        sitemap_xml += f"  </url>\n"

    sitemap_xml += '</urlset>'

    return Response(content=sitemap_xml, media_type="application/xml")
