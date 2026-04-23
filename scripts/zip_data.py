"""
Zip the processed NER training data for upload to Google Drive.
Run this script, then upload the zip file to Drive.
"""

import os
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PROCESSED_DIR = PROJECT_ROOT / "backend" / "data" / "ner_datasets" / "processed"
OUTPUT_ZIP = PROJECT_ROOT / "backend" / "data" / "ner_datasets" / "processed.zip"


def main():
    print("=" * 60)
    print("Zipping processed data for Google Drive upload")
    print("=" * 60)

    if not PROCESSED_DIR.exists():
        print(f"ERROR: {PROCESSED_DIR} not found!")
        print("Run prepare_data.py first!")
        return

    # List files to zip
    files = list(PROCESSED_DIR.glob("*"))
    print(f"\nFound {len(files)} files to zip:")
    for f in files:
        print(f"  {f.name} ({f.stat().st_size / 1024:.1f} KB)")

    # Create zip
    print(f"\nCreating {OUTPUT_ZIP}...")
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(f, f.name)
            print(f"  Added: {f.name}")

    size_mb = OUTPUT_ZIP.stat().st_size / (1024 * 1024)
    print(f"\nDone! Zip file: {OUTPUT_ZIP}")
    print(f"Size: {size_mb:.1f} MB")

    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print(f"1. Go to https://drive.google.com")
    print(f"2. Create folder: resumegpt_ner")
    print(f"3. Upload this file: {OUTPUT_ZIP}")
    print(f"4. In Colab, rerun Cell 2 - it will auto-extract!")


if __name__ == "__main__":
    main()
