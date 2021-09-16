from typing import List

from pydantic import BaseModel, constr


class WalletModel(BaseModel):
    wallet_address: str
    volume_1m_usd: float = None
    txns_1m: int = None
    category: constr(to_lower=True) = ''
    timestamp: int = None


class WalletsListModel(BaseModel):
    total: int
    data: List[WalletModel]