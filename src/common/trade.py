from dataclasses import dataclass

@dataclass
class Trade:
    order_id: int
    asset: str
    currency: str
    price_per_unit: float
    amount_of_asset_bought: float
    quantity_of_currency_used: float
    quantity_of_usd_used: float
    exchange: str

    last_update_timestamp: float
    last_pnl: float
    last_delta_percentage: float
    