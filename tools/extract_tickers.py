import io
import json

import pandas as pd


def extract_tickers(json_file):
    try:
        with open(json_file) as f:
            data = json.load(f)

        content = data.get("content", "")
        if not content:
            return []

        dfs = pd.read_html(io.StringIO(content))
        for df in dfs:
            if "Symbol" in df.columns:
                tickers = df["Symbol"].unique().tolist()
                return [str(t).strip().replace(".", "-") for t in tickers if isinstance(t, str)]
    except Exception:
        pass
    return []


# Manually trigger extraction logic since I can't run python directly easily
# I will read the file and do it in my head/logic if needed,
# but I can also just list the tickers I see in the preview.
# However, I must return ALL tickers.

# Since I cannot reliably run the script and get 500 lines back in one go,
# I'll use the search_files tool to find the CIKs or Symbols in the saved web_scrape file.
