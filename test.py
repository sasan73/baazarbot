from baazarbot.crawlers.ecoiran_crawler import EcoiranCrawler
import asyncio

crawler = EcoiranCrawler("https://ecoiran.com")
successful, total = asyncio.run(crawler.extract("https://ecoiran.com/%D8%A8%D8%AE%D8%B4-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF-%DA%A9%D9%84%D8%A7%D9%86-79"))
print("total:", total)
print("successful", successful)