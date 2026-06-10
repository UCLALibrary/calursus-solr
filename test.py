import os
from random import shuffle
from unittest import TestCase

import requests

SOLR_URL = os.getenv("SOLR_TEST_URL", "http://localhost:8985/solr/ursus")


class TestSort(TestCase):
    def setUp(self):
        requests.post(
            f"{SOLR_URL}/update?commit=true",
            json={"delete": {"query": "*:*"}},
            headers={"Content-Type": "application/json"},
        )

    def tearDown(self):
        requests.post(
            f"{SOLR_URL}/update?commit=true",
            json={"delete": {"query": "*:*"}},
            headers={"Content-Type": "application/json"},
        )

    def test_sorts_non_latin(self):
        docs = [
            {"id": "1", "title_tsort": "x"},
            {"id": "2", "title_tsort": "y"},
            {"id": "3", "title_tsort": "z"},
            {"id": "4", "title_tsort": "あ(a)"},
            {"id": "5", "title_tsort": "い(i)"},
            {"id": "6", "title_tsort": "う(u)"},
        ]
        shuffle(docs)

        # Index documents
        requests.post(
            f"{SOLR_URL}/update?commit=true",
            json=docs,
            headers={"Content-Type": "application/json"},
        )

        # Query documents, A–Z
        response_asc = requests.get(
            f"{SOLR_URL}/select",
            params={"q": "*:*", "sort": "title_tsort asc"},
        )

        order_asc = [doc["id"] for doc in response_asc.json()["response"]["docs"]]
        self.assertEqual(order_asc, ["1", "2", "3", "4", "5", "6"])

        # Query documents, Z–A
        response_desc = requests.get(
            f"{SOLR_URL}/select",
            params={"q": "*:*", "sort": "title_tsort desc"},
        )
        order_asc = [doc["id"] for doc in response_desc.json()["response"]["docs"]]
        assert order_asc == ["6", "5", "4", "3", "2", "1"]

    def test_sorts_numeric(self):
        docs = [
            {"id": "1", "title_tsort": "thing 1"},
            {"id": "2", "title_tsort": "thing 9"},
            {"id": "3", "title_tsort": "thing 10"},
        ]
        shuffle(docs)

        # Index documents
        requests.post(
            f"{SOLR_URL}/update?commit=true",
            json=docs,
            headers={"Content-Type": "application/json"},
        )

        # Query documents, A–Z
        response_asc = requests.get(
            f"{SOLR_URL}/select",
            params={"q": "*:*", "sort": "title_tsort asc"},
        )

        order_asc = [doc["id"] for doc in response_asc.json()["response"]["docs"]]
        self.assertEqual(order_asc, ["1", "2", "3"])

        # Query documents, Z–A
        response_desc = requests.get(
            f"{SOLR_URL}/select",
            params={"q": "*:*", "sort": "title_tsort desc"},
        )
        order_asc = [doc["id"] for doc in response_desc.json()["response"]["docs"]]
        assert order_asc == ["3", "2", "1"]
