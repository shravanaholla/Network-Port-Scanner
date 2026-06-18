# Port Scanner Frontend

This workspace adds a simple Flask web frontend for the existing `port_scanner.py`.

Quick start:

1. Create a virtual environment and activate it.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Unix
source .venv/bin/activate
```

2. Install deps:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open http://127.0.0.1:5000 in your browser and enter a target to scan.

Notes:
- The backend uses the functions in `port_scanner.py` and returns JSON results.
- Scanning remote systems without permission may be illegal; only scan hosts you own or are authorized to test.
