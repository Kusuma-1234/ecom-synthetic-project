# Ecom Synthetic Project

This small project:
- Generates synthetic e-commerce CSVs
- Loads them into an SQLite database (ecom.db)
- Provides example SQL queries.

## Quick usage (phone-friendly)

### Option A — Using GitHub mobile / web UI
1. Create a new repo `ecom-synthetic-project` on GitHub.
2. Use the "Add file → Create new file" option to create the files under `src/` and paste the code above.
3. Create `.gitignore`, `requirements.txt`, and `README.md`.
4. To run: clone or download to a device with Python (or use Termux).

### Option B — Using Termux (Android)
1. Install Termux from Play Store / F-Droid.
2. In Termux:
   ```bash
   pkg install python git
   pip install -r requirements.txt
   git clone https://github.com/<yourname>/ecom-synthetic-project.git
   cd ecom-synthetic-project/src
   python generate_data.py
   python ingest_sqlite.py
   ject
