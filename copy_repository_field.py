#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert UCLA Library CSV files for Ursus, our Blacklight installation."""

import os
import re
import typing
import pprint

import click
from pysolr import Solr  # type: ignore


# Custom Types

DLCSRecord = typing.Dict[str, typing.Any]
UrsusRecord = typing.Dict[str, typing.Any]


@click.command()
@click.argument("solr_url", default="http://localhost:8983/solr/calursus")
def copy_repository_field(solr_url):
    solr_connection = Solr(solr_url, always_commit=True)
    
    n_hits = float('inf')  # but will update from first chunk results   
    start = 0
    chunk_size = 1000
    while start < n_hits:
        print(f"{start+1} to {min(start+chunk_size, n_hits)} of {n_hits}")
        chunk = solr_connection.search(
                "!repository_sim:*",
                fq="repository_tesim:*",
                fl="id,repository_tesim",
                defType="lucene", 
                start=0,
                rows=100,
            )
        solr_connection.add([process_doc(d) for d in chunk.docs], overwrite=False)
        n_hits = chunk.hits
        start += chunk_size

def process_doc(doc):
    doc['repository_sim'] = doc.get('repository_tesim')
    return doc


if __name__ == "__main__":
    copy_repository_field()  # pylint: disable=no-value-for-parameter
