from dataclasses import dataclass

@dataclass
class Trade:
    asset: str
    currency: str
    price_per_unit: float
    amount_of_asset_bought: float
    quantity_of_currency_used: float
    quantity_of_usd_used: float
    exchange: str