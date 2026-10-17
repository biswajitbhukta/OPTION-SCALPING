import sys, time, argparse
from datetime import datetime, timezone, timedelta
import numpy as np, pandas as pd
import yfinance as yf
from institutional_guards_and_triad import AlgoMacroFilter, IntelligentBrain, ExpiryGammaGuard, evaluate_triad_confluence

IST = timezone(timedelta(hours=5, minutes=30))

INSTRUMENT_REGISTRY = {
    INSTRUMENT_REGISTRY = {
    "^NSEI": {"name": "NIFTY 50", "exchange": "NSE", "segment": "index", "strike_step": 50, "lot_size": 75},
    "^NSEBANK": {"name": "BANK NIFTY", "exchange": "NSE", "segment": "index", "strike_step": 100, "lot_size": 30},
    "^BSESN": {"name": "BSE SENSEX", "exchange": "BSE", "segment": "index", "strike_step": 100, "lot_size": 20},
    "CL=F": {"name": "CRUDE OIL", "exchange": "MCX", "segment": "commodity", "strike_step": 100, "lot_size": 100},
    "NG=F": {"name": "NATURAL GAS", "exchange": "MCX", "segment": "commodity", "strike_step": 5.0, "lot_size": 1250}
}
}

class MasterExecutionEngine:
    def __init__(self, capital: float, max_loss: float, itm_rank: int):
        self.capital = capital
        self.macro = AlgoMacroFilter()
        self.brain = IntelligentBrain()
        self.gamma = ExpiryGammaGuard()
        self.itm_rank = itm_rank
        self.realized_pnl = 0.0

    def fetch_live_data(self, symbol: str) -> pd.DataFrame:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="1d", interval="5m")
            if df.empty or len(df) < 5:
                df = ticker.history(period="5d", interval="1d")
            return df
        except Exception as e:
            print(f"  [!] Error fetching live data for {symbol}: {e}", flush=True)
            return pd.DataFrame()

    def run_scanner_loop(self, segment: str, poll_interval: int, max_cycles: int):
        universe = {k: v for k, v in INSTRUMENT_REGISTRY.items() if segment == "all" or v["segment"] == segment}
        print(f"[✓] Live Market Volume Engine Online. Monitoring {len(universe)} instruments.", flush=True)

        cycle = 0
        while True:
            cycle += 1
            now_ist = datetime.now(IST).strftime('%H:%M:%S IST')
            print(f"\n[🔄 CYCLE #{cycle}] {now_ist} | P&L: ₹{self.realized_pnl:+,.2f}", flush=True)

            for symbol, meta in universe.items():
                df = self.fetch_live_data(symbol)
                if df.empty:
                    print(f"  [!] Skipping {meta['name']} due to empty feed.", flush=True)
                    continue

                latest_volume = int(df['Volume'].iloc[-1]) if 'Volume' in df.columns else 0
                latest_close = float(df['Close'].iloc[-1])

                triad = evaluate_triad_confluence(df, "BUY CE")
                score = self.brain.score_setup(True, True, True, triad["triad_score_pct"])

                print(f"  [📊 LIVE FEED] {meta['name']} -> Price: ₹{latest_close:,.2f} | Vol: {latest_volume:,} | Triad: {triad['triad_score_pct']}%", flush=True)

            if 0 < max_cycles <= cycle:
                break
            time.sleep(poll_interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--segment", default="index")
    parser.add_argument("--capital", type=float, default=100000.0)
    parser.add_argument("--max-loss", type=float, default=4000.0)
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--cycles", type=int, default=0)
    args = parser.parse_args()
    engine = MasterExecutionEngine(capital=args.capital, max_loss=args.max_loss, itm_rank=1)
    engine.run_scanner_loop(segment=args.segment, poll_interval=args.interval, max_cycles=args.cycles)