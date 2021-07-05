# Highwind

`Highwind` is a tool that allows you to deploy NFT smart contracts through a Graphic User Interface (GUI). With Highwind you can easily create and mint items that can be sold on [OpenSea](https://opensea.io/).

Leveraging Streamlit, Docker and web3 this tool is run on your local machine and works straight out of the box without any advanced configruation.


![Deploy contract](images/deploy_contract.png)

## Requirements

* docker (https://docs.docker.com/get-docker/)

### 3rd Party APIs

In order to streamline deployments, Highwind leverages these 3rd party APIs. You must register and get an API key from these services to use Highwind

#### Infura

[Infura](https://infura.io/) is a blockchain development suite that provides easy access to Ethereum networks.

#### Pinata

[Pinata](https://pinata.cloud/) provides an API to easily interact with [IPFS](https://ipfs.io/)

#### Metamask

[MetaMask](https://metamask.io/) is a software cryptocurrency wallet used to interact with the Ethereum blockchain.


## QuickStart

Here is how you can easily get started using Highwind

```bash
git clone https://github.com/banjtheman/highwind.git
cd highwind
./build_docker.sh
./run_docker.sh
# view website on localhost:8501
```


## Deploy

With Highwind you can deploy Smart Contracts easily just by entering in your wallet info and infura key. You will need to have some ETH/MATIC in your wallet depending on the network. The faucet links are displayed in the UI.

![Deploy contract](images/deploy_contract.png)


## Create Item

With Highwind, you can easily create item metadata that is uploaded to [IPFS](https://ipfs.io/) powered by [Pinata](https://pinata.cloud/). Simply enter in the infromation and press the Pin button


![Enter Item](images/enter_item.png)

![Create Item](images/create_item.png)


## Mint Item

Once you have created an item, you can now mint it on the blockchain. Enter the address you would like to send the NFT to, and press the mint button.


![Mint item](images/mint_item.png)



## View on OpenSea

Once items have been minted, you can view your collection and items on OpenSea. 

![View on OpenSea](images/opensea_item.png)
