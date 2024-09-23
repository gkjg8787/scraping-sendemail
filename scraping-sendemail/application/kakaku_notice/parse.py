from datetime import datetime
from bs4 import BeautifulSoup

from domain.model import IKakakuItemFactory, KakakuItem


class KakakuParser:
    results: list[KakakuItem]

    def __init__(self, htmltext, kakakuitemfactory: IKakakuItemFactory):
        soup = BeautifulSoup(htmltext, "html.parser")
        self.results = self.create_kakakuItems(
            soup=soup, kakakuitemfactory=kakakuitemfactory
        )

    def create_kakakuItems(
        self, soup: BeautifulSoup, kakakuitemfactory: IKakakuItemFactory
    ) -> list[KakakuItem]:
        table = soup.find("table")
        keys = [
            "item_id",
            "name",
            "url_id",
            "url",
            "price",
            "trendrate",
            "salename",
            "storename",
            "updated_at",
            "record_low",
            "active_url",
        ]
        results: list[KakakuItem] = []
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if not cols:
                continue
            parse_data = {k: v.text.strip() for k, v in zip(keys, cols)}
            for key in ["item_id", "url_id", "active_url"]:
                parse_data[key] = int(parse_data[key])
            parse_data["updated_at"] = self.convert_updated_at(parse_data["updated_at"])
            parse_data["price"] = self.convert_price(parse_data["price"])
            parse_data["record_low"] = self.convert_price(parse_data["record_low"])
            parse_data["trendrate"] = self.convert_trendrate(parse_data["trendrate"])
            item = kakakuitemfactory.create(**parse_data)
            results.append(item)
        return results

    @classmethod
    def convert_price(cls, value: str) -> int:
        return int(value.replace("円", ""))

    @classmethod
    def convert_trendrate(cls, value: str) -> float:
        return float(value.replace("%", ""))

    @classmethod
    def convert_updated_at(cls, value: str) -> datetime:
        format = "%Y-%m-%d %H:%M:%S"
        return datetime.strptime(value, format)
