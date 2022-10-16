from dataclasses import dataclass
import time

@dataclass
class OrderStats:
    total_spent: float = 0.0
    current_value: float = 0.0
    pnl: float = 0.0
    delta: float = 0.0
    timestamp: int = int(time.time() * 1000)
