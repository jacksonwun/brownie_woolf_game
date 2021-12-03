from brownie import Woolf, WOOL, Traits, Barn, accounts, interface
from .helper import get_account
import random

# Set Barn to Woolf
WOOLF_CAP = 100
TOTAL_ACCOUNTS = len(accounts)

# User
USER_WOOL = 100

def output_balance(user_account, wool_address):
    eth_balance = user_account.balance().to('ether')
    wool_balance = wool_address.balanceOf(user_account)
    return eth_balance, wool_balance

def deploy(owner_account):
    # Deploy Wool (addController first), Trait -> Woolf => Barn
    wool_address = WOOL.deploy({"from":owner_account})
    wool_address.addController(owner_account, {'from':owner_account})
    traits_address = Traits.deploy({"from":owner_account})
    woolf_address = Woolf.deploy(wool_address, traits_address, WOOLF_CAP, {"from":owner_account})
    barn_address = Barn.deploy(woolf_address, wool_address, {'from': owner_account})
    return wool_address, traits_address, woolf_address, barn_address

def mint_wool(user_account, wool_address, owner_account):
    return wool_address.mint(user_account, USER_WOOL, {'from':owner_account})

def mint_woolf(user_account, woolf_address):
    mint_quantity = random.randint(1,3)
    mint_total_value = mint_quantity * 0.069420
    woolf_address.mint(mint_quantity, False, {'from':user_account, 'value': f'{mint_total_value} ether'})

def get_woolf_list(user_account, woolf_address):
    woolf_list = []
    total_woolf = woolf_address.balanceOf(user_account)

    for i in range(0, total_woolf):
        token_id = woolf_address.tokenOfOwnerByIndex(user_account, i)
        if woolf_address.tokenTraits(token_id)[0]:
            token_traits = 'Sheep'
        else:
            token_traits = 'Wolf'
        woolf_list.append((token_id, token_traits, woolf_address.tokenTraits(i)))

    return woolf_list


def main():
    owner_account = accounts[0]
    wool_address, traits_address, woolf_address, barn_address = deploy(owner_account)

    print('-----Minting Wool-----')
    for i in range(1,10):
        print(i,':', accounts[i])
        tx = mint_wool(accounts[i], wool_address, owner_account)
    tx.wait(1)

    print('-----Minting Woolf-----')
    for i in range(1,10):
        print(i,':', accounts[i])
        mint_woolf(accounts[i], woolf_address)

    print('-----Output Balance-----')
    for i in range(1,10):
        print(i,':', accounts[i])
        print(output_balance(accounts[i], wool_address))
        print('Woolf: ', woolf_address.balanceOf(accounts[i]))

    print('-----Woolf Id List-----')
    for i in range(1, 10):
        print(i,':', accounts[i])
        print('Woolf ID: ', get_woolf_list(accounts[i], woolf_address))



