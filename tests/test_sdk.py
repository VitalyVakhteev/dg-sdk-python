import time
from pprint import pprint

import pytest

from src.models import enums
from src.sdk.dg_sdk import DexGuru
from src import models


@pytest.fixture()
def sdk():
    yield DexGuru(api_key='-ER8PuY9iBB_x5n-_AYJCtF9aTRDxn2OAJtfhWMCxrU',
                  endpoint='https://api-public-stage.prod-euc1.dexguru.net')


@pytest.fixture()
def eth_address():
    return '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'


@pytest.fixture()
def btc_address():
    return '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599'


@pytest.fixture()
def eth_wallets():
    return ['0x5452ee47f16ead43a6984f101d2dfc7ec2e714e3', '0xb7b25f87fb87bb0f4a833499cb8ce58a01184943']


@pytest.fixture()
def polygon_wallets():
    return ['0x7942aec6f7a31e7e89c5477c97ca288acd205adb', '0xfa79ac8667e37dee9b1a6c2f9b9a38f94af77119']


@pytest.mark.asyncio
async def test_get_chains(sdk):
    chains = await sdk.get_chains()
    assert isinstance(chains, models.ChainsListModel)


@pytest.mark.asyncio
async def test_get_chain(sdk):
    chains = await sdk.get_chain(chain_id=1)
    assert isinstance(chains, models.ChainModel)
    assert chains.chain_id == 1


@pytest.mark.asyncio
async def test_get_transactions(sdk):
    txs = await sdk.get_transactions(chain_id=1, amm_id=enums.AmmChoices.quickswap.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 0
    txs = await sdk.get_transactions(chain_id=1, amm_id=enums.AmmChoices.uniswap.value, limit=2)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 2
    for item in txs.data:
        assert item.amm_id == enums.AmmChoices.uniswap.value
    assert isinstance(txs.total, int)
    assert txs.total > 0
    txs = await sdk.get_transactions(chain_id=1, wallet_category=enums.CategoriesChoices.heavy.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 10
    for item in txs.data:
        assert item.wallet_category == enums.CategoriesChoices.heavy.value


@pytest.mark.asyncio
async def test_get_txs_swaps(sdk):
    txs = await sdk.get_txs_swaps(chain_id=1, amm_id=enums.AmmChoices.quickswap.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 0
    txs = await sdk.get_txs_swaps(chain_id=1, amm_id=enums.AmmChoices.uniswap.value, limit=2)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 2
    for item in txs.data:
        assert item.amm_id == enums.AmmChoices.uniswap.value
    assert isinstance(txs.total, int)
    assert txs.total > 0
    txs = await sdk.get_txs_swaps(chain_id=1, wallet_category=enums.CategoriesChoices.heavy.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 10
    for item in txs.data:
        assert item.wallet_category == enums.CategoriesChoices.heavy.value
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 10
    for item in txs.data:
        assert item.transaction_type == enums.TransactionChoices.swap.value


@pytest.mark.asyncio
async def test_get_txs_burns(sdk):
    txs = await sdk.get_txs_burns(chain_id=enums.ChainChoices.eth.value, amm_id=enums.AmmChoices.quickswap.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 0
    txs = await sdk.get_txs_burns(chain_id=enums.ChainChoices.eth.value, amm_id=enums.AmmChoices.uniswap.value, limit=2)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 2
    for item in txs.data:
        assert item.amm_id == enums.AmmChoices.uniswap.value
    assert isinstance(txs.total, int)
    assert txs.total > 0
    txs = await sdk.get_txs_burns(chain_id=enums.ChainChoices.bsc.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 10
    for item in txs.data:
        assert item.transaction_type == enums.TransactionChoices.burn.value


@pytest.mark.asyncio
async def test_get_txs_mints(sdk):
    txs = await sdk.get_txs_mints(chain_id=enums.ChainChoices.eth.value, amm_id=enums.AmmChoices.quickswap.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 0
    txs = await sdk.get_txs_mints(chain_id=enums.ChainChoices.eth.value, amm_id=enums.AmmChoices.uniswap.value, limit=2)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 2
    for item in txs.data:
        assert item.amm_id == enums.AmmChoices.uniswap.value
    assert isinstance(txs.total, int)
    assert txs.total > 0
    txs = await sdk.get_txs_mints(
        chain_id=enums.ChainChoices.polygon.value,
        amm_id=enums.AmmChoices.quickswap.value,
        sort_by=enums.SortChoices.timestamp.value,
        limit=1,
        offset=2,
        begin_timestamp=1630934916,
        end_timestamp=1631021316,
    )
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 1
    for item in txs.data:
        assert item.transaction_type == enums.TransactionChoices.mint.value


@pytest.mark.asyncio
async def test_get_tokens_inventory(sdk):
    tokens = await sdk.get_tokens_inventory(1, name='eth')
    assert isinstance(tokens, models.TokensInventoryListModel)
    for token in tokens.data:
        assert isinstance(token, models.TokenInventoryModel)
    with pytest.raises(Exception, match='Specify name'):
        await sdk.get_tokens_inventory(1)


@pytest.mark.asyncio
async def test_get_tokens_finance(sdk, btc_address, eth_address):
    tokens = await sdk.get_tokens_finance(1, limit=5)
    assert isinstance(tokens, models.TokensFinanceListModel)
    assert len(tokens.data) == 5
    for token in tokens.data:
        assert isinstance(token, models.TokenFinanceModel)
    token_addresses = [btc_address, eth_address]
    tokens = await sdk.get_tokens_finance(1, token_addresses=token_addresses, limit=10)
    assert len(tokens.data) == 2
    for token in tokens.data:
        assert token.address in token_addresses


@pytest.mark.asyncio
async def test_get_token_inventory(sdk, eth_address):
    token = await sdk.get_token_inventory(1, eth_address)
    assert isinstance(token, models.TokenInventoryModel)
    assert token.address == eth_address
    with pytest.raises(Exception, match='Token not found'):
        await sdk.get_token_inventory(1, 'invalid')


@pytest.mark.asyncio
async def test_get_token_finance(sdk, eth_address):
    token = await sdk.get_token_finance(1, eth_address)
    assert isinstance(token, models.TokenFinanceModel)
    assert token.address == eth_address
    with pytest.raises(Exception, match='Not found token finance'):
        await sdk.get_token_finance(1, 'invalid')


@pytest.mark.asyncio
async def test_get_token_transactions(sdk, eth_address):
    wallet_category = enums.CategoriesChoices.heavy.value
    amm = enums.AmmChoices.sushiswap.value
    txs = await sdk.get_token_transactions(1, token_address=eth_address,
                                           wallet_category=wallet_category,
                                           limit=5, amm_id=amm)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 5
    for tx in txs.data:
        assert tx.wallet_category == wallet_category
        assert tx.amm_id == amm


@pytest.mark.asyncio
async def test_get_token_swaps(sdk, eth_address):
    wallet_category = enums.CategoriesChoices.heavy.value
    amm = enums.AmmChoices.sushiswap.value
    txs = await sdk.get_token_swaps(1, token_address=eth_address,
                                    wallet_category=wallet_category,
                                    limit=5, amm_id=amm)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 5
    for tx in txs.data:
        assert tx.wallet_category == wallet_category
        assert tx.amm_id == amm
        assert tx.transaction_type == enums.TransactionChoices.swap


@pytest.mark.asyncio
async def test_get_token_burns(sdk, eth_address):
    amm = enums.AmmChoices.sushiswap.value
    txs = await sdk.get_token_burns(1, token_address=eth_address,
                                    limit=5, amm_id=amm)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 5
    for tx in txs.data:
        assert tx.amm_id == amm
        assert tx.transaction_type == enums.TransactionChoices.burn


@pytest.mark.asyncio
async def test_get_token_mints(sdk, eth_address):
    amm = enums.AmmChoices.sushiswap.value
    txs = await sdk.get_token_mints(1, token_address=eth_address,
                                    limit=5, amm_id=amm)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 5
    for tx in txs.data:
        assert tx.amm_id == amm
        assert tx.transaction_type == enums.TransactionChoices.mint


@pytest.mark.asyncio
async def test_get_token_market_history(sdk, eth_address):
    begin_ts = int(time.time() - 3000)
    end_ts = int(time.time() - 1000)
    txs = await sdk.get_token_market_history(1, token_address=eth_address,
                                             begin_timestamp=begin_ts, end_timestamp=end_ts)
    assert isinstance(txs, models.TokensHistoryListModel)
    assert txs.total != 0
    for tx in txs.data:
        assert tx.address == eth_address
        assert isinstance(tx, models.TokenHistory)
        assert tx.timestamp > begin_ts
        assert tx.timestamp < end_ts
    with pytest.raises(Exception, match='Token not found'):
        await sdk.get_token_market_history(1, ('i' * 42))


@pytest.mark.asyncio
async def test_get_wallets_info(sdk, eth_wallets, polygon_wallets):
    info = await sdk.get_wallets_info(1, wallet_address=eth_wallets + polygon_wallets)
    assert isinstance(info, models.WalletsListModel)
    assert info.total != 0
    for wallet in info.data:
        assert isinstance(wallet, models.WalletModel)
    assert len(info.data) == 4
    info = await sdk.get_wallets_info(1, wallet_address=polygon_wallets)
    assert isinstance(info, models.WalletsListModel)
    assert len(info.data) == 2
    for wallet in info.data:
        assert wallet.category
        assert wallet.volume_1m_usd is None
    with pytest.raises(Exception, match='Wallets not found'):
        await sdk.get_wallets_info(1, wallet_address=['invalid'])


@pytest.mark.asyncio
async def test_get_wallet_info(sdk, eth_wallets, polygon_wallets):
    wallet = await sdk.get_wallet_info(1, wallet_address=eth_wallets[0])
    assert isinstance(wallet, models.WalletModel)
    wallet = await sdk.get_wallet_info(1, wallet_address=polygon_wallets[0])
    assert wallet.category
    assert wallet.volume_1m_usd is None
    with pytest.raises(Exception, match='Wallet not found'):
        await sdk.get_wallet_info(1, wallet_address='invalid')


@pytest.mark.asyncio
async def test_get_wallet_transactions(sdk, eth_wallets, polygon_wallets):
    txs = await sdk.get_wallet_transactions(1, wallet_address=eth_wallets[0])
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.wallet_address == eth_wallets[0]
    txs = await sdk.get_wallet_transactions(1, wallet_address='invalid')
    assert txs.total == 0
    assert txs.data == []


@pytest.mark.asyncio
async def test_get_wallet_swaps(sdk, eth_wallets):
    txs = await sdk.get_wallet_swaps(1, wallet_address=eth_wallets[0], limit=7)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert 0 < len(txs.data) == 7
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.wallet_address == eth_wallets[0]
        assert tx.transaction_type == enums.TransactionChoices.swap


@pytest.mark.asyncio
async def test_get_wallet_burns(sdk):
    txs = await sdk.get_wallet_burns(1, wallet_address='0x935d2fd458fdf41b6f7b62471f593797866a3ce6', limit=6)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert 0 < len(txs.data) <= 6
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.wallet_address == '0x935d2fd458fdf41b6f7b62471f593797866a3ce6'
        assert tx.transaction_type == enums.TransactionChoices.burn


@pytest.mark.asyncio
async def test_get_wallet_mints(sdk):
    txs = await sdk.get_wallet_mints(1, wallet_address='0x935d2fd458fdf41b6f7b62471f593797866a3ce6', limit=5)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert 0 < len(txs.data) <= 5
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.wallet_address == '0x935d2fd458fdf41b6f7b62471f593797866a3ce6'
        assert tx.transaction_type == enums.TransactionChoices.mint


@pytest.mark.asyncio
async def test_get_amms_swaps(sdk, eth_address):
    begin_ts = time.time() - 3000
    end_ts = time.time() - 1000
    wallet_category = enums.CategoriesChoices.noob.value
    txs = await sdk.get_amms_swaps(1, token_address=eth_address, wallet_category=wallet_category, limit=8,
                                   begin_timestamp=int(begin_ts), end_timestamp=int(end_ts))
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert len(txs.data) == 8
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.wallet_category == wallet_category
        assert tx.transaction_type == enums.TransactionChoices.swap
        assert eth_address == tx.tokens_in[0]['address'] or eth_address == tx.tokens_out[0]['address']
        assert tx.timestamp >= begin_ts
        assert tx.timestamp <= end_ts


@pytest.mark.asyncio
async def test_get_amms_burns(sdk, eth_address):
    begin_ts = time.time() - 3000
    end_ts = time.time() - 1000
    txs = await sdk.get_amms_burns(1, token_address=eth_address, limit=8,
                                   begin_timestamp=int(begin_ts), end_timestamp=int(end_ts))
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert len(txs.data) == 8
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.transaction_type == enums.TransactionChoices.burn
        assert eth_address in [item.get('address') for item in tx.tokens_in + tx.tokens_out]
        assert tx.timestamp >= begin_ts
        assert tx.timestamp <= end_ts


@pytest.mark.asyncio
async def test_get_amms_mints(sdk, eth_address):
    begin_ts = time.time() - 3000
    end_ts = time.time() - 1000
    txs = await sdk.get_amms_mints(1, token_address=eth_address, limit=8,
                                   begin_timestamp=int(begin_ts), end_timestamp=int(end_ts))
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert len(txs.data) == 8
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.transaction_type == enums.TransactionChoices.mint
        assert eth_address in [item.get('address') for item in tx.tokens_in + tx.tokens_out]
        assert tx.timestamp >= begin_ts
        assert tx.timestamp <= end_ts


@pytest.mark.asyncio
async def test_get_amm_swaps(sdk, eth_address):
    amm = enums.AmmChoices.uniswap_v3.value
    chain = enums.ChainChoices.eth.value
    begin_ts = time.time() - 3000
    end_ts = time.time() - 1000
    wallet_category = enums.CategoriesChoices.noob.value
    txs = await sdk.get_amm_swaps(chain, amm_id=amm, token_address=eth_address, wallet_category=wallet_category,
                                  limit=8,
                                  begin_timestamp=int(begin_ts), end_timestamp=int(end_ts))
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert len(txs.data) == 8
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.wallet_category == wallet_category
        assert tx.transaction_type == enums.TransactionChoices.swap
        assert eth_address == tx.tokens_in[0]['address'] or eth_address == tx.tokens_out[0]['address']
        assert tx.timestamp >= begin_ts
        assert tx.timestamp <= end_ts
        assert tx.amm_id == amm


@pytest.mark.asyncio
async def test_get_amm_burns(sdk):
    amm = enums.AmmChoices.quickswap.value
    chain = enums.ChainChoices.polygon.value
    begin_ts = time.time() - 3000
    end_ts = time.time() - 1000
    txs = await sdk.get_amm_burns(chain, amm_id=amm, limit=8,
                                  begin_timestamp=int(begin_ts), end_timestamp=int(end_ts))
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert len(txs.data) == 8
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.transaction_type == enums.TransactionChoices.burn
        assert tx.timestamp >= begin_ts
        assert tx.timestamp <= end_ts
        assert tx.amm_id == amm


@pytest.mark.asyncio
async def test_get_amm_mints(sdk):
    amm = enums.AmmChoices.pancakeswap.value
    chain = enums.ChainChoices.bsc.value
    begin_ts = int(time.time() - 3000)
    end_ts = int(time.time() - 1000)
    txs = await sdk.get_amm_mints(chain, amm_id=amm, limit=8)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert len(txs.data) == 8
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.transaction_type == enums.TransactionChoices.mint
        assert tx.timestamp >= begin_ts
        assert tx.timestamp <= end_ts
        assert tx.amm_id == amm


@pytest.mark.asyncio
async def test_get_all_amm_inventory(sdk):
    chain = enums.ChainChoices.eth.value
    amms = await sdk.get_all_amm_inventory(chain)
    assert amms
    assert len(amms.data) > 0
    assert isinstance(amms, models.AmmListModel)
    for amm in amms.data:
        assert isinstance(amm, models.AmmModel)


@pytest.mark.asyncio
async def test_get_amm_inventory(sdk):
    chain = enums.ChainChoices.eth.value
    amm_ = enums.AmmChoices.uniswap_v3.value
    amm = await sdk.get_amm_inventory(chain, amm_)
    assert isinstance(amm, models.AmmModel)

