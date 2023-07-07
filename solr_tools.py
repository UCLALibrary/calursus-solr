#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert UCLA Library CSV files for Ursus, our Blacklight installation."""

import os
import re
import time
import typing

import click
from retry.api import retry_call
import rich.progress
from pysolr import Solr  # type: ignore


# Custom Types

DLCSRecord = typing.Dict[str, typing.Any]
UrsusRecord = typing.Dict[str, typing.Any]


@click.group()
def solr_tools():
    pass


@solr_tools.command()
@click.argument("source_url", default="http://localhost:8983/solr/californica")
@click.argument("destination_url", default="http://localhost:8983/solr/ursus")
def clone(source_url, destination_url):
    with rich.progress.Progress() as progress:
        task = progress.add_task("Copying...", total=None)

        source_solr = Solr(source_url, timeout=10, always_commit=True)
        destination_solr = Solr(destination_url, always_commit=True)

        n_hits = float("inf")  # but will updasste from first chunk results
        start = 0
        chunk_size = 250
        while start < n_hits:
            chunk = source_solr.search(
                "*:*",
                defType="lucene",
                start=start,
                rows=chunk_size,
            )

            processed_chunk = [process_doc(d) for d in chunk.docs]

            retry_call(
                destination_solr.add,
                fargs=[processed_chunk],
                fkwargs={"overwrite": True},
                # tries=3,
                delay=1,
                backoff=6,
                max_delay=15 * 60,  # 15 min
            )

            n_hits = chunk.hits
            start += chunk_size
            progress.update(task, total=n_hits, completed=start + len(chunk.docs))
            time.sleep(1)


def process_doc(doc):
    for key in ["_version_", "score", "hashed_id_ssi", "suggest"]:
        doc.pop(key, None)

    # Facet fields aren't stored, so populate them from the stored equivalents
    doc.update(
        {
            f"{field}_sim": doc.get(f"{field}_tesim")
            for field in [
                "architect",
                "associated_name",
                "author",
                "caligrapher",
                "collection",
                "commentator",
                "composer",
                "creator",
                "dimensions",
                "director",
                "dlcs_collection_name",
                "editor",
                "engraver",
                "extent",
                "features",
                "form",
                "genre",
                "human_readable_language",
                "human_readable_resource_type",
                "human_readable_type",
                "illuminator",
                "illustrator",
                "keywords",
                "local_identifier",
                "location",
                "lyricist",
                "medium",
                "named_subject",
                "names",
                "normalized_date",
                "photographer",
                "place_of_origin",
                "printmaker",
                "rubricator",
                "scribe",
                "script",
                "series",
                "subject_cultural_object",
                "subject_domain_topic",
                "subject_geographic",
                "subject_temporal",
                "subject_topic",
                "subject",
                "support",
                "translator",
                "uniform_title",
                "writing_system",
            ]
        }
    )
    # If any facet fields don't fit the *_sim: *_tesim pattern, add them explicitly
    doc.update(
        {
            "dlcs_collection_name_sim": doc.get("dlcs_collection_name_ssm"),
            "generic_type_sim": doc.get("resource_type_tesim"),
            "local_identifier_sim": doc.get("local_identifier_ssm"),
            "local_identifier_ssim": doc.get("local_identifier_ssm"),
        }
    )
    title = doc.get("title_tesim")
    if type(title) is list and len(title) > 0 and type(title[0]) is str:
        doc["title_alpha_numeric_ssort"] = title[0]

    return doc


if __name__ == "__main__":
    solr_tools()  # pylint: disable=no-value-for-parameter
