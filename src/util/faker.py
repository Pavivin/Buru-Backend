import random
import uuid
from datetime import datetime
from typing import List

offer_types = ("LOW", "MEDIUM", "HIGH", "HIGHEST", "SUPER")

offer_categories = ("first", "second", "third")


def random_offer_categories() -> str:
    offer_category = offer_categories[random.randint(0, 2)]
    return offer_category


def random_offer_type() -> str:
    offer_type = offer_types[random.randint(0, 4)]
    return f"'{offer_type}'" + "::offertype"


def add_offer(list_id: List[uuid.UUID]) -> str:
    query = ""
    for i, _id in enumerate(list_id):
        query += f"""
            INSERT INTO offer (offer_id, offer_type, title, restrictions, promosite_url, img_url,
                               hash_img, created_at)
                values(
                    '{_id}',
                    {random_offer_type()},
                    '{random_offer_categories()}',
                    'test{i}' ,
                    'test{i}',
                    'test{i}',
                    'test{i}',
                    '{datetime.now().isoformat()}'
                );
            """
    return query


def add_promo(list_id: List[uuid.UUID]) -> str:
    query = ""
    for _id in list_id:
        query += f"""
            INSERT INTO promocode (promo_id, offer_id, status, promo_code, created_at)
                values(
                    '{uuid.uuid4()}',
                    '{_id}',
                    'CREATED'::promostatus,
                    '{uuid.uuid4().hex[:8]}',
                    '{datetime.now().isoformat()}'
                );
            """
    return query


def fake_promo(count: int) -> None:
    query = ""
    list_id = [uuid.uuid4() for _ in range(count)]
    query += add_offer(list_id)
    for _ in range(5):
        query += add_promo(list_id)

    with open("faker.sql", "w+", encoding="UTF-8") as file:
        file.write(query)


fake_promo(1000)
