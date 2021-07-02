import json
import logging
from typing import Type, Union, Dict, Any, List
import requests
import os

from requests.packages.urllib3.filepost import encode_multipart_formdata


def pinJSONToIPFS(
    json_obj: Dict[str, Any], pinata_api_key: str, pinata_secret: str
) -> Dict[str, Any]:
    """
    Purpose:
        PIN a json obj to IPFS
    Args:
        json_obj - The json obj
    Returns:
        ipfs json - data from pin
    """
    HEADERS = {
        "pinata_api_key": pinata_api_key,
        "pinata_secret_api_key": pinata_secret,
    }

    ipfs_json = {
        "pinataMetadata": {
            "name": json_obj["name"],
        },
        "pinataContent": json_obj,
    }

    endpoint_uri = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    response = requests.post(endpoint_uri, headers=HEADERS, json=ipfs_json)
    return response.json()


# TODO how can we pin filedata...
def pinContentToIPFS(
    content: bytes, metadata: Dict[str, Any], pinata_api_key: str, pinata_secret: str
) -> Dict[str, Any]:
    """
    Purpose:
        PIN a json obj to IPFS
    Args:
        json_obj - The json obj
    Returns:
        ipfs json - data from pin
    """

    HEADERS = {
        "pinata_api_key": pinata_api_key,
        "pinata_secret_api_key": pinata_secret,
    }

    payload = {"pinataMetadata": metadata}

    # files = {"file": content, "pinataMetadata": metadata}
    bytes_payload = json.dumps(payload).encode("utf-8")

    # multipart_form_data = {"file": content, "parameters": bytes_payload}

    multipart_form_data = {"file": content}

    # encoded_data = encode_multipart_formdata(multipart_form_data)

    endpoint_uri = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    response = requests.post(endpoint_uri, data=multipart_form_data, headers=HEADERS)
    print(response.text)
    print(response.headers)
    return response.json()


def pinSearch(
    query: str, pinata_api_key: str, pinata_secret: str
) -> List[Dict[str, Any]]:
    """
    Purpose:
        Query pins for data
    Args:
        query - the query str
    Returns:
        data - array of pined objects
    """

    endpoint_uri = f"https://api.pinata.cloud/data/pinList?{query}"
    HEADERS = {
        "pinata_api_key": pinata_api_key,
        "pinata_secret_api_key": pinata_secret,
    }
    response = requests.get(endpoint_uri, headers=HEADERS).json()

    # now get the actual data from this
    data = []
    if "rows" in response:

        for item in response["rows"]:
            ipfs_pin_hash = item["ipfs_pin_hash"]
            hash_data = requests.get(
                f"https://gateway.pinata.cloud/ipfs/{ipfs_pin_hash}"
            ).json()
            data.append(hash_data)

    # print(response.json())
    return data
