import scrapy


class PokemonSpiderSpider(scrapy.Spider):
    name = "pokemon_spider"
    allowed_domains = ["pokemondb.net"]
    start_urls = ['https://pokemondb.net/pokedex/all']

    def parse(self, response):
        table = response.xpath('//table[@id="pokedex"]')[0]
        rows = table.xpath('.//tr')[1:]
        for row in rows:
            name = row.xpath('.//td[2]/a/text()').get()
            type_1 = row.xpath('.//td[3]/a[1]/text()').get()
            type_2 = row.xpath('.//td[3]/a[2]/text()').get()
            total = row.xpath('.//td[4]/text()').get()
            hp = row.xpath('.//td[5]/text()').get()
            attack = row.xpath('.//td[6]/text()').get()
            defense = row.xpath('.//td[7]/text()').get()
            sp_atk = row.xpath('.//td[8]/text()').get()
            sp_def = row.xpath('.//td[9]/text()').get()
            speed = row.xpath('.//td[10]/text()').get()

            yield {
                'Name': name,
                'Type 1': type_1,
                'Type 2': type_2,
                'Total': total,
                'HP': hp,
                'Attack': attack,
                'Defense': defense,
                'Sp. Atk': sp_atk,
                'Sp. Def': sp_def,
                'Speed': speed
            }
