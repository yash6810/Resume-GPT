"""
Fine-tune existing NER model with additional training data.
This script loads a pre-trained model and continues training with more examples.

Usage in Colab:
1. Train initial model (5,000 examples) - done in train_ner.ipynb
2. Run this script to fine-tune with remaining examples
"""

# Paste this into a NEW CELL in Colab after initial training completes

fine_tune_code = """
# Cell 10: Fine-tune with remaining examples
import spacy
from spacy.training import Example
import random
import gc
import time

print("=" * 60)
print("Fine-tuning Model with Additional Examples")
print("=" * 60)

# Load the trained model
print("Loading pre-trained model...")
nlp = spacy.load(f'{MODEL_OUTPUT}/model-best')
print(f"Model loaded with pipeline: {nlp.pipe_names}")

# Get remaining examples (skip first 5,000 already used)
START_INDEX = 5000
MAX_ADDITIONAL = 10000  # Use up to 10,000 more examples
END_INDEX = min(START_INDEX + MAX_ADDITIONAL, len(train_docs))

print(f"\\nUsing examples {START_INDEX} to {END_INDEX}")
print(f"Additional examples: {END_INDEX - START_INDEX}")

additional_docs = train_docs[START_INDEX:END_INDEX]

# Create training examples
print("Creating training examples...")
train_examples = []
for doc in additional_docs:
    pred_doc = nlp.make_doc(doc.text)
    example = Example(pred_doc, doc)
    train_examples.append(example)

print(f"Created {len(train_examples)} training examples")

# Fine-tuning config (lower learning rate, fewer epochs)
N_EPOCHS = 10
BATCH_SIZE = 32
DROPOUT = 0.2

print(f"\\nFine-tuning: {N_EPOCHS} epochs, batch size {BATCH_SIZE}")
print("=" * 60)

start_time = time.time()

for epoch in range(N_EPOCHS):
    epoch_start = time.time()
    random.shuffle(train_examples)
    losses = {}
    
    batches = spacy.util.minibatch(train_examples, size=BATCH_SIZE)
    for batch in batches:
        nlp.update(batch, drop=DROPOUT, losses=losses)
    
    epoch_time = time.time() - epoch_start
    loss = losses.get('ner', 0)
    print(f"Epoch {epoch+1}/{N_EPOCHS} - Loss: {loss:.4f} - Time: {epoch_time:.1f}s")

# Save fine-tuned model
nlp.to_disk(f'{MODEL_OUTPUT}/model-finetuned')
total_time = time.time() - start_time

print("\\n" + "=" * 60)
print(f"Fine-tuning complete! Total time: {total_time/60:.1f} minutes")
print(f"Model saved to: {MODEL_OUTPUT}/model-finetuned")
print("=" * 60)

gc.collect()
"""

print(fine_tune_code)
