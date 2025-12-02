# scripts/demo_ingest.py
"""
Simple demo ingestion script.

Run:
    python scripts/demo_ingest.py

This will:
 - create a small demo text file (if not present)
 - call the backend ingestion function (local import) to index chunks into Qdrant
"""
import os
import sys
import argparse

# Import the ingest helper from the backend package
# Note: When running from project root, Python path will find backend package.
try:
    from backend.app.ingest import ingest_file
except Exception as e:
    # Provide helpful error if imports fail
    print("Failed to import backend.app.ingest. Make sure you're running from the repo root and backend is available.")
    print("Error:", e)
    sys.exit(1)


def create_demo_file(path: str) -> None:
    if os.path.exists(path):
        print(f"Demo file already exists: {path}")
        return
    content = """Brand X - Demo Playbook
Product: XPhone
Key benefits: exceptional battery life (48h typical), pro-grade camera, ultra-fast charging, and cinematic video.
Previous campaign: 'Everyday Epic' (2024) - achieved 2.1% CTR on social.
Tone: youthful, confident, slightly witty.
Promotional offers: 10% launch discount for first 10k buyers.
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created demo file at {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="demo_brand_playbook.txt", help="Path to demo playbook .txt")
    parser.add_argument("--brand", default="brand_x", help="Brand id to tag ingested chunks")
    args = parser.parse_args()

    create_demo_file(args.file)

    print("Starting ingest...")
    try:
        ids = ingest_file(file_path=args.file, brand_id=args.brand)
        print("Ingested chunk ids:", ids)
    except AssertionError as ae:
        print("Ingest assertion error:", ae)
    except Exception as e:
        print("Ingest failed:", e)


if __name__ == "__main__":
    main()
