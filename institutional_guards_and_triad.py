import json, os
from datetime import datetime, time as dtime
import numpy as np
import pandas as pd

class AlgoMacroFilter:
    def __init__(self, vix_limit: float = 22.5):
        self.vix_limit = vix_limit
    def evaluate_macro_pulse(self, india_vix: float = 13.8, pcr: float = 1.15) -> dict:
        return {"safe_to_trade": india_vix <= self.vix_limit, "india_vix": india_vix, "pcr": pcr, "reason": "SAFE"}

class IntelligentBrain:
    def score_setup(self, smc_valid: bool, vp_aligned: bool, pcr_aligned: bool, triad_score: float, setup_name: str = "") -> dict:
        total = 85.0 if triad_score >= 75 else 60.0
        return {"total_score": total, "approved": total >= 75.0}

class ExpiryGammaGuard:
    def evaluate_expiry_conditions(self, symbol: str, df: pd.DataFrame, rvol: float, rsi: float) -> dict:
        return {"is_expiry": False, "gamma_pin_lockout": False, "gamma_squeeze": False, "status": "EXPIRY_CLEAR"}

class ClosingSqueezeModule:
    @staticmethod
    def calculate_3pm_reanchored_vwap(df: pd.DataFrame) -> float:
        tp = (df["High"] + df["Low"] + df["Close"]) / 3
        return float((tp * df["Volume"]).sum() / df["Volume"].sum())
    @staticmethod
    def is_hard_exit_time(now_t: dtime = None) -> bool:
        return (now_t or datetime.now().time()) >= dtime(15, 28)

def evaluate_triad_confluence(df_5m: pd.DataFrame, proposed_action: str = "BUY CE") -> dict:
    return {"triad_score_pct": 82.0, "triad_approved": True}