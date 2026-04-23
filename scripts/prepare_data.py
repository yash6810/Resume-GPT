"""
Prepare NER training data for spaCy.
Converts combined_dataset.json to spaCy DocBin format.

Input: backend/data/ner_datasets/raw/combined_dataset.json
Output: backend/data/ner_datasets/processed/
  - train.spacy
  - dev.spacy
  - test.spacy
"""

import json
import os
import random
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def load_combined_dataset(input_path: str) -> Dict:
    """Load the combined dataset from JSON."""
    print(f"Loading dataset from {input_path}...")

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded {len(data['examples'])} examples")
    print(f"Sources: {data['metadata']['sources']}")
    return data


def convert_to_spacy_format(examples: List[Dict]) -> List[Tuple[str, Dict]]:
    """
    Convert examples to spaCy training format.

    Input format (all sources now use same format):
    - {"text": "...", "entities": [{"start": N, "end": N, "label": "..."}]}

    Output format: (text, {"entities": [(start, end, label), ...]})
    """
    training_data = []

    for example in examples:
        source = example.get("source", "unknown")
        text = example.get("text", "")
        raw_entities = example.get("entities", [])

        # Skip if no text
        if not text or len(text) < 10:
            continue

        # Convert entities to tuple format
        entities = []
        for ent in raw_entities:
            if isinstance(ent, dict):
                start = ent.get("start", 0)
                end = ent.get("end", len(text))
                label = ent.get("label", "MISC")
                # Validate entity bounds
                if 0 <= start < end <= len(text):
                    entities.append((start, end, label))
            elif isinstance(ent, (list, tuple)) and len(ent) >= 3:
                start, end, label = ent[0], ent[1], ent[2]
                if 0 <= start < end <= len(text):
                    entities.append((start, end, label))

        training_data.append((text, {"entities": entities}))

    print(f"Converted {len(training_data)} examples to spaCy format")
    return training_data


def split_dataset(
    data: List[Tuple[str, Dict]],
    train_ratio: float = 0.8,
    dev_ratio: float = 0.1,
    test_ratio: float = 0.1,
    seed: int = 42,
) -> Tuple[List, List, List]:
    """Split dataset into train/dev/test sets."""
    random.seed(seed)
    random.shuffle(data)

    total = len(data)
    train_end = int(total * train_ratio)
    dev_end = train_end + int(total * dev_ratio)

    train_data = data[:train_end]
    dev_data = data[train_end:dev_end]
    test_data = data[dev_end:]

    print(f"\nDataset split:")
    print(f"  Train: {len(train_data)} examples ({train_ratio * 100:.0f}%)")
    print(f"  Dev:   {len(dev_data)} examples ({dev_ratio * 100:.0f}%)")
    print(f"  Test:  {len(test_data)} examples ({test_ratio * 100:.0f}%)")

    return train_data, dev_data, test_data


def create_spacy_docbin(data: List[Tuple[str, Dict]], output_path: str):
    """
    Convert training data to spaCy DocBin format.
    This is the format required for spaCy training.
    """
    try:
        import spacy
        from spacy.tokens import DocBin

        # Create blank English pipeline
        nlp = spacy.blank("en")

        docbin = DocBin()
        skipped = 0

        for text, annotations in data:
            doc = nlp.make_doc(text)
            raw_entities = annotations.get("entities", [])

            # Sort entities by start position
            sorted_entities = sorted(raw_entities, key=lambda x: x[0])

            # Filter out overlapping entities
            filtered_entities = []
            last_end = 0

            for start, end, label in sorted_entities:
                # Skip if overlaps with previous entity
                if start >= last_end and start < end and end <= len(text):
                    filtered_entities.append((start, end, label))
                    last_end = end

            # Create spans
            ents = []
            for start, end, label in filtered_entities:
                span = doc.char_span(start, end, label=label)
                if span:
                    ents.append(span)

            # Only add if we have entities or if text is valid
            if len(text) >= 10:
                try:
                    doc.ents = ents
                    docbin.add(doc)
                except ValueError:
                    # Skip documents with entity issues
                    skipped += 1
                    continue

        docbin.to_disk(output_path)
        print(f"  Saved {len(data) - skipped} examples to {output_path}")
        if skipped > 0:
            print(f"  Skipped {skipped} examples due to entity overlaps")

    except ImportError:
        print("ERROR: spaCy not installed. Install with: pip install spacy")
        # Fallback: save as JSON
        json_path = output_path.replace(".spacy", ".json")
        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Saved as JSON fallback: {json_path}")


def save_as_json(data: List[Tuple[str, Dict]], output_path: str):
    """Save data as JSON (alternative format)."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Saved {len(data)} examples to {output_path}")


def main():
    """Main function to prepare training data."""
    print("=" * 60)
    print("ResumeGPT NER Data Preparation")
    print("=" * 60)

    # Paths
    input_path = (
        PROJECT_ROOT
        / "backend"
        / "data"
        / "ner_datasets"
        / "raw"
        / "combined_dataset.json"
    )
    output_dir = PROJECT_ROOT / "backend" / "data" / "ner_datasets" / "processed"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Check if input exists
    if not os.path.exists(input_path):
        print(f"\nERROR: Input file not found: {input_path}")
        print("Run download_datasets.py first!")
        return

    # Load data
    data = load_combined_dataset(str(input_path))
    examples = data.get("examples", [])

    if not examples:
        print("\nERROR: No examples found in dataset!")
        return

    # Convert to spaCy format
    print("\n" + "-" * 40)
    print("Converting to spaCy format...")
    training_data = convert_to_spacy_format(examples)

    # Split dataset
    print("\n" + "-" * 40)
    print("Splitting dataset...")
    train_data, dev_data, test_data = split_dataset(training_data)

    # Save in spaCy DocBin format
    print("\n" + "-" * 40)
    print("Saving processed data...")

    create_spacy_docbin(train_data, str(output_dir / "train.spacy"))
    create_spacy_docbin(dev_data, str(output_dir / "dev.spacy"))
    create_spacy_docbin(test_data, str(output_dir / "test.spacy"))

    # Also save as JSON for inspection
    save_as_json(train_data, str(output_dir / "train.json"))
    save_as_json(dev_data, str(output_dir / "dev.json"))
    save_as_json(test_data, str(output_dir / "test.json"))

    print("\n" + "=" * 60)
    print("DONE! Data prepared for training.")
    print("=" * 60)
    print(f"\nOutput directory: {output_dir}")
    print("\nFiles created:")
    print("  - train.spacy (for training)")
    print("  - dev.spacy (for validation)")
    print("  - test.spacy (for testing)")
    print("  - train.json, dev.json, test.json (for inspection)")

    print(
        "\nNext step: Upload 'processed' folder to Google Drive and run train_ner.ipynb in Colab"
    )


if __name__ == "__main__":
    main()
