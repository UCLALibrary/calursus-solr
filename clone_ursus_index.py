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
@click.argument("source_url", default="http://localhost:8983/solr/californica")
@click.argument("destination_url", default="http://localhost:8983/solr/ursus")
def clone_solr_core(source_url, destination_url):
    source_solr = Solr(source_url, always_commit=True)
    destination_solr = Solr(destination_url, always_commit=True)

    
    chunk = source_solr.search(
            "has_model_ssim:Collection",
            defType="lucene", 
            start=0,
            rows=100,
        )
    destination_solr.add([process_doc(d,source_solr,destination_solr) for d in chunk.docs], overwrite=True)

def process_doc(doc,source_solr,destination_solr):
    for key in ['_version_', 'score', 'hashed_id_ssi']:
        doc.pop(key, None)
    
    # Facet fields aren't stored, so populate them from the stored equivalents
    doc.update({f"{field}_sim": doc.get(f"{field}_tesim") 
                for field in [
                    'associated_name',
                    'uniform_title',
                    'architect',
                    'author',
                    'rubricator',
                    'translator',
                    'illustrator',
                    'caligrapher',
                    'engraver',
                    'printmaker',
                    'editor',
                    'creator',
                    'keywords',
                    'form',
                    'names',
                    'commentator',
                    'composer',
                    'dimensions',
                    'dlcs_collection_name',
                    'extent',
                    'features',
                    'genre',
                    'human_readable_language',
                    'human_readable_resource_type',
                    'illuminator',
                    'local_identifier',
                    'location',
                    'lyricist',
                    'medium',
                    'named_subject',
                    'normalized_date',
                    'photographer',
                    'place_of_origin',
                    'scribe',
                    'script',
                    'subject',
                    'support',
                    'writing_system',
                ]
    # # If any facet fields don't fit the *_sim: *_tesim pattern, add them explicitly
    # doc.update({
    #     "features_sim": doc.get('features_tesim'),
    # })
    })
    if doc.get("has_model_ssim")[0] == 'Collection':    
        n_hits = float('inf')  # but will update from first chunk results   
        start = 0
        chunk_size = 1000
        while start < n_hits:
            print(f"{start+1} to {min(start+chunk_size, n_hits)} of {n_hits}")
            chunk = source_solr.search(
                "(has_model_ssim:Work) AND (member_of_collection_ids_ssim:" + doc.get("id") + ")",
                defType="lucene", 
                start=start,
                rows=chunk_size,
            )
            n_hits = chunk.hits
            destination_solr.add([process_doc(d,source_solr,destination_solr) for d in chunk.docs], overwrite=True)
            start += chunk_size

    return doc

# def load_csv(filename: str, solr_url: typing.Optional[str]):
#     """Load data from a csv.

#     Args:
#         filename: A CSV file.
#         solr_url: URL of a solr instance.
#     """

#     solr_client = Solr(solr_url, always_commit=True) if solr_url else None

#     data_frame = pandas.read_csv(filename)
#     data_frame = data_frame.where(data_frame.notnull(), None)
#     collection_rows = data_frame[data_frame["Object Type"] == "Collection"]

#     config = {
#         "collection_names": {
#             row["Item ARK"]: row["Title"] for _, row in collection_rows.iterrows()
#         },
#         "controlled_fields": load_field_config("./fields"),
#         "data_frame": data_frame,
#     }

#     if not solr_client:
#         print("[", end="")

#     first_row = True
#     for _, row in data_frame.iterrows():
#         if row["Object Type"] in ("ChildWork", "Page"):
#             continue

#         if first_row:
#             first_row = False
#         elif not solr_client:
#             print(", ")

#         mapped_record = map_record(row, config=config)
#         if solr_client:
#             solr_client.add([mapped_record])
#         else:
#             print(mapped_record, end="")

#     if not solr_client:
#         print("]")


# def load_field_config(base_path: str = "./fields") -> typing.Dict:
#     clone_solr_core    for file_name in files:
#             field_name = os.path.splitext(file_name)[0]
#             with open(os.path.join(path, file_name), "r") as stream:
#                 field_config[field_name] = yaml.safe_load(stream)
#             field_config[field_name]["terms"] = {
#                 t["id"]: t["term"] for t in field_config[field_name]["terms"]
#             }
#     return field_config


# # pylint: disable=bad-continuation
# def map_field_value(
#     row: DLCSRecord, field_name: str, config: typing.Dict
# ) -> typing.Any:
#     """Map value from a CSV cell to an object that will be passed to solr.

#     Mapping logic is defined by the FIELD_MAPPING dict, defined in mappery.py.
#     Keys of FIELD_MAPPING are output field names as used in Ursus. Values can
#     vary, and the behavior of map_field_value() will depend on that value.

#     If FIELD_MAPPING[field_name] is a string, then it will be interpreted as
#     clone_solr_core"""
#     mapping: mapper.MappigDictValue = mapper.FIELD_MAPPING[field_name]

#     if mapping is None:
#         return None

#     if callable(mapping):
#         return mapping(row)

#     if isinstance(mapping, str):
#         mapping = [mapping]

#     if not isinstance(mapping, typing.Collection):
#         raise TypeError(
#             f"FIELD_MAPPING[field_name] must be iterable, unless it is None, Callable, or a string."
#         )

#     output: typing.List[str] = []
#     for csv_field in mapping:
#         input_value = row.get(csv_field)
#         if input_value:
#             output.extend(input_value.split("|~|"))

#     bare_field_name = get_bare_field_name(field_name)
#     if bare_field_name in config.get("controlled_fields", {}):
#         terms = config["controlled_fields"][bare_field_name]["terms"]
#         output = [terms.get(value, value) for value in output]

#     return [value for value in output if value]  # remove untruthy values like ''


# def get_bare_field_name(field_name: str) -> str:
#     """Strips the solr suffix and initial 'human_readable_' from a field name."""

#     return re.sub(r"_[^_]+$", "", field_name).replace("human_readable_", "")


# # pylint: disable=bad-continuation
# def map_record(row: DLCSRecord, config: typing.Dict) -> UrsusRecord:
#     """Maps a metadata record from CSV to Ursus Solr.

#     Args:
#         record: A mapping representing the CSV record.

#     Returns:
#         A mapping representing the record to submit to Solr.

#     """
#     record: UrsusRecord = {
#         field_name: map_field_value(row, field_name, config=config)
#         for field_name in mapper.FIELD_MAPPING
#     }

#     # thumbnail
#     record["thumbnail_url_ss"] = (
#         record.get("thumbnail_url_ss")
#         or thumbnail_from_child(record, config=config)
#         or thumbnail_from_manifest(record)
#     )

#     # collection name
#     if "Parent ARK" in row and row["Parent ARK"] in config["collection_names"]:
#         dlcs_collection_name = config["collection_names"][row["Parent ARK"]]
#         record["dlcs_collection_name_tesim"] = [dlcs_collection_name]

#     # facet fields
#     record["features_sim"] = record.get("features_tesim")
#     record["genre_sim"] = record.get("genre_tesim")
#     record["human_readable_language_sim"] = record.get("human_readable_language_tesim")
#     record["human_readable_resource_type_sim"] = record.get("resource_type_tesim")
#     record["location_sim"] = record.get("location_tesim")
#     record["member_of_collections_ssim"] = record.get("dlcs_collection_name_tesim")
#     record["named_subject_sim"] = record.get("named_subject_tesim")
#     record["place_of_origin_sim"] = record.get("place_of_origin_tesim")
#     record["script_sim"] = record.get("script_tesim")
#     record["subject_sim"] = record.get("subject_tesim")
#     record["support_sim"] = record.get("support_tesim")
#     record["writing_system_sim"] = record.get("writing_system_tesim")
#     record["year_isim"] = year_parser.integer_years(record.get("normalized_date_tesim"))

#     # sort fields
#     titles = record.get("title_tesim")
#     if isinstance(titles, typing.Sequence) and len(titles) >= 1:
#         record["sort_title_ssort"] = titles[0]

#     years = record.get("year_isim")
#     if isinstance(years, typing.Sequence) and len(years) >= 1:
#         record["sort_year_isi"] = min(years)

#     return record


# def thumbnail_from_child(
#     record: UrsusRecord, config: typing.Dict
# ) -> typing.Optional[str]:
#     """Picks a thumbnail by looking for child rows in the CSV.

#     Tries the following strategies in order, returning the first that succeeds:
#     - Thumbnail of a child record titled "f. 001r"
#     - Thumbnail of the first child record
#     - None

#     Args:
#         record: A mapping representing the CSV record.
#         config: A config object.

#     Returns:
#         A string containing the thumbnail URL
#     """

#     if "data_frame" not in config:
#         return None

#     ark = record["ark_ssi"]
#     data = config["data_frame"]
#     children = data[data["Parent ARK"] == ark]
#     representative = children[children["Title"] == "f. 001r"]
#     if representative.shape[0] == 0:
#         representative = children

#     for _, row in representative.iterrows():
#         thumb = mapper.thumbnail_url(row)
#         if thumb:
#             return thumb
#     return None


# def thumbnail_from_manifest(record: UrsusRecord) -> typing.Optional[str]:
#     """Picks a thumbnail downloading the IIIF manifest.

#     Args:
#         record: A mapping representing the CSV record.

#     Returns:
#         A string containing the thumbnail URL
#     """

#     try:
#         manifest_url = record.get("iiif_manifest_url_ssi")
#         if not isinstance(manifest_url, str):
#             return None
#         response = requests.get(manifest_url)
#         manifest = response.json()

#         canvases = {
#             c["label"]: c["images"][0]["resource"]["service"]["@id"]
#             for seq in manifest["sequences"]
#             for c in seq["canvases"]
#         }

#         return (
#             canvases.get("f. 001r") or list(canvases.values())[0]
#         ) + "/full/!200,200/0/default.jpg"

#     except:  # pylint: disable=bare-except
#         return None


if __name__ == "__main__":
    clone_solr_core()  # pylint: disable=no-value-for-parameter
