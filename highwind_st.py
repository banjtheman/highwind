"""
Purpose:
    Start Highwind UI
"""

# Python imports
import logging
import os
import streamlit as st
from typing import Type, Union, Dict, Any, List
import glob
from pathlib import Path


from modules import utils, mint_nft, pinata_api
import streamlit.components.v1 as components


###
# Streamlit Main Functionality
###


def get_items() -> List:
    """
    Purpose:
        Load list of items
    Args:
        N/A
    Returns:
        items
    """
    items = {}

    json_files = glob.glob("highwind_jsons/items/*.json")

    for json_file in json_files:

        json_obj = utils.load_json(json_file)
        key = Path(json_file).stem
        item_name = json_obj["item"]["name"]
        items[f"{item_name}_{key}"] = json_obj

    return items


def load_contracts() -> List:
    """
    Purpose:
        Load list of contracts
    Args:
        N/A
    Returns:
        contrats
    """
    contracts = {}

    json_files = glob.glob("highwind_jsons/contracts/*.json")

    for json_file in json_files:

        json_obj = utils.load_json(json_file)
        key = Path(json_file).stem
        contracts[key] = json_obj

    return contracts


def opensea() -> None:
    """
    Purpose:
        Shows the opensea page for your contract
    Args:
        N/A
    Returns:
        N/A
    """

    st.subheader("OpenSea")

    contracts = load_contracts()
    contracts_list = list(contracts.keys())

    st.subheader("Select Contract")
    contract_name = st.selectbox("Contract", contracts_list)

    # if no contracts stop
    if len(contracts_list) == 0:
        st.warning("Deploy a contract first")
        st.stop()

    token_name = contracts[contract_name]["token_name"].lower()
    contract = contracts[contract_name]["contract_address"]

    st.write(f"Contract address: {contract}")
    st.write(f"OpenSea URL: https://testnets.opensea.io/collection/{token_name}/")

    components.iframe(
        f"https://testnets.opensea.io/collection/{token_name}/",
        height=1000,
        width=1000,
        scrolling=True,
    )


def create_item():
    """
    Purpose:
        Shows the create item screen
    Args:
        N/A
    Returns:
        N/A
    """
    st.subheader("Create new item")

    item_name = st.text_input("Item name", "", help="Name of the item.")
    ext_url = st.text_input(
        "External URL",
        "",
        help="This is the URL that will appear below the asset's image on OpenSea and will allow users to leave OpenSea and view the item on your site.",
    )
    item_desc = st.text_input(
        "Description",
        "",
        help="A human readable description of the item. Markdown is supported.",
    )
    image_url = st.text_input(
        "Image Url",
        "",
        help="This is the URL to the image of the item. Can be just about any type of image (including SVGs, which will be cached into PNGs by OpenSea, and even MP4s), and can be IPFS URLs or paths. We recommend using a 350 x 350 image.",
    )

    item_color = st.color_picker(
        "background_color",
        "#ffffff",
        help="Background color of the item on OpenSea. Must be a six-character hexadecimal without a pre-pended #.",
    )

    animation_url = st.text_input(
        "animation_url",
        "",
        help="A URL to a multi-media attachment for the item. The file extensions GLTF, GLB, WEBM, MP4, M4V, OGV, and OGG are supported, along with the audio-only extensions MP3, WAV, and OGA.Animation_url also supports HTML pages, allowing you to build rich experiences and interactive NFTs using JavaScript canvas, WebGL, and more. Scripts and relative paths within the HTML page are now supported. However, access to browser extensions is not supported.",
    )

    youtube_url = st.text_input(
        "youtube_url",
        "",
        help="A URL to a YouTube video.",
    )

    # This is where session state will shine
    if "attrs" not in st.session_state:
        st.session_state.attrs = 1

    if st.button("Add attribute"):
        st.session_state.attrs += 1

    if st.button("Remove attribute"):
        st.session_state.attrs -= 1

    attr_types = ["Text", "Number", "Date"]
    attr_list = []

    for index in range(st.session_state.attrs):

        st.subheader(f"Attribute {index}")

        attr_json = {}
        attr_type = st.selectbox(
            "Attribute type", attr_types, key=f"attr_types_index_{index}"
        )

        if attr_type == "Text":

            trait_type = st.text_input("trait type", "", key=f"trait_index_{index}")
            value = st.text_input("Value", "", key=f"value_index_{index}")

            attr_json["trait_type"] = trait_type
            attr_json["value"] = value

        if attr_type == "Number":

            display_types = ["number", "boost_number", "boost_percentage", "ranking"]
            display_type = st.selectbox(
                "dislay type", display_types, key=f"display_index_{index}"
            )

            trait_type = st.text_input("trait type", "", key=f"trait_index_{index}")
            value = st.text_input("Value", "", key=f"value_index_{index}")

            if not display_type == "ranking":
                attr_json["display_type"] = display_type
            attr_json["trait_type"] = trait_type
            attr_json["value"] = value

        if attr_type == "Date":

            trait_type = st.text_input("trait type", "", key=f"trait_index_{index}")

            st.write("Pass in a unix timestamp for the value")
            value = st.text_input("Value", "", key=f"value_index_{index}")

            attr_json["display_type"] = "date"
            attr_json["trait_type"] = trait_type
            attr_json["value"] = value

        attr_list.append(attr_json)

    item_json = {}
    item_json["name"] = item_name
    item_json["image"] = image_url
    item_json["external_url"] = ext_url
    item_json["description"] = item_desc
    item_json["background_color"] = item_color.replace("#", "")
    item_json["animation_url"] = animation_url
    item_json["youtube_url"] = youtube_url
    # attrs = st.session_state.attrs
    item_json["attributes"] = attr_list

    return item_json


def mint() -> None:
    """
    Purpose:
        Shows the mint Page
    Args:
        N/A
    Returns:
        N/A
    """

    st.subheader("Mint items")

    contracts = load_contracts()
    contracts_list = list(contracts.keys())

    st.subheader("Select Contract for minting")
    contract_name = st.selectbox("Contract", contracts_list)

    # if no contracts stop
    if len(contracts_list) == 0:
        st.warning("Deploy a contract first")
        st.stop()

    abi_path = contracts[contract_name]["abi_path"]
    network = contracts[contract_name]["network"]
    contract = contracts[contract_name]["contract_address"]

    # Facuet info
    if network == "mumbai":
        st.subheader("Faucet")
        st.write("The Faucet allows you to get free matic on test networks")
        st.write("https://faucet.matic.network/")

    elif network == "rinkeby":
        st.subheader("Faucet")
        st.write("The Faucet allows you to get free eth on test networks")
        st.write("https://faucet.rinkeby.io/")

    st.subheader("NFT Info")
    st.write(
        f'{contracts[contract_name]["token_name"]}  - {contracts[contract_name]["token_symbol"]} '
    )
    st.write(f"Contract address: {contract}")

    st.subheader("API Keys")
    st.write("Enter in your infura.io API KEY")
    st.write("https://infura.io/dashboard/ethereum")

    infura_key = st.text_input("infura_key", "", type="password")

    st.subheader("Wallet Info")
    public_key = st.text_input("Public Key", "")
    private_key = st.text_input("Private key", "", type="password")

    new_item = st.checkbox("Create new item?")

    ### Display item info
    if new_item:

        item_json = create_item()

        st.subheader("Current Metadata")
        st.write(item_json)

        st.write("Enter in your pinata.cloud API keys")
        st.write("https://pinata.cloud/keys")

        pinata_key = st.text_input("Pinata Key", "", type="password")
        pinata_secret_key = st.text_input("Pinata Secret key", "", type="password")

        if st.button("Pin Metadata to IPFS?"):
            hash_info = pinata_api.pinJSONToIPFS(
                item_json, pinata_key, pinata_secret_key
            )

            ipfs_hash = hash_info["IpfsHash"]
            item_final_json = {}
            item_final_json["hash_info"] = hash_info
            item_final_json["item"] = item_json
            item_final_json["url"] = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
            item_final_json["ipfs_url"] = f"ipfs://{ipfs_hash}"

            utils.save_json(f"highwind_jsons/items/{ipfs_hash}.json", item_final_json)

            st.write(item_final_json["url"])

    else:
        items = get_items()
        item_list = list(items.keys())
        item_list_name = st.selectbox("Items", item_list)

        if item_list_name:

            item_obj = items[item_list_name]

            token_uri = item_obj["ipfs_url"]
            item_json = item_obj["item"]

            st.write("Item metadata")
            st.write(item_json)

            token_address = st.text_input("Address to send token", "")

            if st.button(f"Mint token"):
                with st.spinner("Minting..."):
                    eth_json = mint_nft.set_up_blockchain(
                        contract,
                        abi_path,
                        public_key,
                        private_key,
                        infura_key,
                        network,
                    )

                    txn_hash = mint_nft.web3_mint(token_address, token_uri, eth_json)

                    if network == "mumbai":
                        scan_url = "https://explorer-mumbai.maticvigil.com/tx/"
                    elif network == "rinkeby":
                        scan_url = "https://rinkeby.etherscan.io/tx/"

                    st.success(f"txn hash: {txn_hash}")
                    st.write(f"{scan_url}{txn_hash}")
                    st.balloons()


def deploy() -> None:
    """
    Purpose:
        Shows the deploy Page
    Args:
        N/A
    Returns:
        N/A
    """

    st.subheader("Deploy Contracts")

    # Deploy Contracts
    networks = ["mumbai", "rinkeby"]
    st.subheader("Network")
    st.write("Select the network to deploy your smart contract")
    network = st.selectbox("Network", networks)

    # Facuet info

    if network == "mumbai":
        st.subheader("Faucet")
        st.write("The Faucet allows you to get free matic on test networks")
        st.write("https://faucet.matic.network/")

    elif network == "rinkeby":
        st.subheader("Faucet")
        st.write("The Faucet allows you to get free eth on test networks")
        st.write("https://faucet.rinkeby.io/")

    st.subheader("NFT Name")

    st.write("Enter in the name and Symbol for your NFT")
    nft_name = st.text_input("NFT Name", "MyNFT")
    nft_symbol = st.text_input("NFT Symbol", "MyNFT")

    st.subheader("API Keys")
    st.write("Enter in your infura.io API KEY")
    st.write("https://infura.io/dashboard/ethereum")

    infura_key = st.text_input("infura_key", "", type="password")

    st.subheader("Wallet Info")
    public_key = st.text_input("Public Key", "")
    mnemonic = st.text_input("mnemonic", "", type="password")

    if st.button(f"Deploy {nft_name} Smart Contract"):
        with st.spinner("Deploying..."):

            # TODO do we want to check for invalid chars
            nft_name = nft_name.replace(" ", "_")

            # Do a find and replace in the for the Contrant Name
            contracts_dir = f"contracts_{nft_name}"
            contracts_build = f"./build/contracts_{nft_name}"

            #  Replace contract code
            copy_command = f"cp -r contracts_temp {contracts_dir}"
            os.system(copy_command)
            file_data = utils.read_from_file(f"{contracts_dir}/MyNFT.sol")
            file_data = file_data.replace("REPLACE_NAME", f"{nft_name}")
            file_data = file_data.replace("REPLACE_SYM", f"{nft_symbol}")
            utils.write_to_file(f"{contracts_dir}/MyNFT.sol", file_data)

            # Replace migrations file
            copy_command = f"cp migrations_temp/2_deploy_contracts.js migrations/2_deploy_contracts.js"
            os.system(copy_command)
            con_data = utils.read_from_file(f"migrations/2_deploy_contracts.js")
            con_data = con_data.replace("REPLACE_NAME", f"{nft_name}")
            utils.write_to_file(f"migrations/2_deploy_contracts.js", con_data)

            # Get all env vars
            export_statements = f'INFURA_KEY={infura_key} OWNER_ADDRESS={public_key} MNEMONIC="{mnemonic}" CONTRACTS_DIR={contracts_dir} CONTRACTS_BUILD={contracts_build}'

            cmd = f"{export_statements} truffle migrate --reset --network {network}"
            output = os.popen(cmd).read()

            with st.beta_expander("Log output"):
                st.write(output)

            try:
                cas = output.split("contract address:    ")
                contract_address = cas[2].split(" ")[0].strip()
            except:
                if network == "mumbai":
                    token = "MATIC"
                else:
                    token = "ETH"
                st.warning(f"Do you have enough {token} in wallet {public_key}?")
                st.error("Check log output for error details")
                st.stop()

            if network == "mumbai":
                scan_url = "https://explorer-mumbai.maticvigil.com/address/"
            elif network == "rinkeby":
                scan_url = "https://rinkeby.etherscan.io/address/"

            st.success(f"Contract Address: {contract_address}")
            st.write(f"{scan_url}{contract_address}")

            # Contract metadata
            contract_json = {}
            contract_json["token_name"] = nft_name
            contract_json["token_symbol"] = nft_symbol
            contract_json["contract_address"] = contract_address
            contract_json["network"] = network
            contract_json["scan_url"] = f"{scan_url}{contract_address}"
            contract_json["abi_path"] = f"{contracts_build}/{nft_name}.json"

            # do we want to check for duplicates?

            file_name = f"highwind_jsons/contracts/{nft_name}.json"
            if os.path.exists(file_name):
                # loop until we find a free file name
                counter = 1
                while True:
                    file_name = f"highwind_jsons/contracts/{nft_name}_{counter}.json"

                    if os.path.exists(file_name):
                        counter += 1
                    else:
                        break

            utils.save_json(file_name, contract_json)
            st.subheader("Deployed")
            st.balloons()


def sidebar() -> None:
    """
    Purpose:
        Shows the side bar
    Args:
        N/A
    Returns:
        N/A
    """

    st.sidebar.title("Highwind")

    # Create the Navigation Section
    st.sidebar.header("Navigation")
    pages = ["Deploy", "Mint", "OpenSea"]
    default_page = 0
    page = st.sidebar.selectbox("Go To", options=pages, index=default_page)

    if page == "Deploy":
        deploy()
    elif page == "Mint":
        mint()
    elif page == "OpenSea":
        opensea()
    else:
        st.error("Invalid Page")


def app() -> None:
    """
    Purpose:
        Controls the app flow
    Args:
        N/A
    Returns:
        N/A
    """

    # Spin up the sidebar, will control which page is loaded in the
    # main app
    sidebar()


def main() -> None:
    """
    Purpose:
        Controls the flow of the streamlit app
    Args:
        N/A
    Returns:
        N/A
    """

    # Start the streamlit app
    st.title("Highwind")
    st.write("Highwind allows you to manage NFT contracts")
    app()


if __name__ == "__main__":
    main()
