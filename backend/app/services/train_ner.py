"""
Training script for fine-tuning NER model on resume data.
This script creates a custom spaCy NER model that can extract:
- Skills
- Companies
- Job titles
- Education
- Dates
- Locations
"""

import spacy
from spacy.tokens import DocBin
from spacy.training import Example
import random
import json
import os
from pathlib import Path


# Entity labels for resume NER
ENTITY_LABELS = [
    "SKILL",  # Programming languages, tools, frameworks
    "COMPANY",  # Company names
    "JOB_TITLE",  # Job positions
    "DEGREE",  # Educational degrees
    "SCHOOL",  # Educational institutions
    "DATE",  # Employment/education dates
    "LOCATION",  # Cities, states, countries
    "CERTIFICATION",  # Professional certifications
]


def create_training_data():
    """
    Create sample training data for resume NER.
    In production, you'd use a real dataset like ResumeNER or create your own.
    """
    training_data = [
        (
            "John Smith is a Senior Software Engineer at Google with 5 years of experience in Python and JavaScript.",
            {
                "entities": [
                    (0, 10, "PERSON"),
                    (16, 37, "JOB_TITLE"),
                    (41, 47, "COMPANY"),
                    (71, 77, "SKILL"),
                    (82, 92, "SKILL"),
                ]
            },
        ),
        (
            "Graduated with a Bachelor of Science in Computer Science from MIT in 2020.",
            {
                "entities": [
                    (19, 47, "DEGREE"),
                    (51, 54, "SCHOOL"),
                    (58, 62, "DATE"),
                ]
            },
        ),
        (
            "Worked at Microsoft as a Data Scientist from January 2021 to December 2023.",
            {
                "entities": [
                    (10, 19, "COMPANY"),
                    (25, 38, "JOB_TITLE"),
                    (44, 58, "DATE"),
                    (62, 76, "DATE"),
                ]
            },
        ),
        (
            "Proficient in React, Node.js, Docker, AWS, and PostgreSQL.",
            {
                "entities": [
                    (14, 19, "SKILL"),
                    (21, 28, "SKILL"),
                    (30, 36, "SKILL"),
                    (38, 41, "SKILL"),
                    (47, 56, "SKILL"),
                ]
            },
        ),
        (
            "AWS Certified Solutions Architect with expertise in cloud infrastructure.",
            {
                "entities": [
                    (0, 33, "CERTIFICATION"),
                ]
            },
        ),
        (
            "Located in San Francisco, California. Previously worked in New York.",
            {
                "entities": [
                    (12, 35, "LOCATION"),
                    (58, 66, "LOCATION"),
                ]
            },
        ),
        (
            "Master of Business Administration from Stanford University, 2019.",
            {
                "entities": [
                    (0, 32, "DEGREE"),
                    (38, 57, "SCHOOL"),
                    (59, 63, "DATE"),
                ]
            },
        ),
        (
            "Software Developer at Amazon Web Services. Skills: Java, Kubernetes, Terraform.",
            {
                "entities": [
                    (0, 18, "JOB_TITLE"),
                    (22, 43, "COMPANY"),
                    (53, 57, "SKILL"),
                    (59, 69, "SKILL"),
                    (71, 80, "SKILL"),
                ]
            },
        ),
    ]

    return training_data


def convert_to_spacy_format(training_data, nlp):
    """Convert training data to spaCy's Example format."""
    examples = []

    for text, annotations in training_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        examples.append(example)

    return examples


def train_ner_model(
    output_dir: str = "models/resume_ner", n_iter: int = 30, dropout: float = 0.5
):
    """
    Train a custom NER model for resume parsing.

    Args:
        output_dir: Directory to save the trained model
        n_iter: Number of training iterations
        dropout: Dropout rate for training
    """
    print("=" * 50)
    print("Resume NER Model Training")
    print("=" * 50)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Load base model
    print("\nLoading base model...")
    nlp = spacy.load("en_core_web_sm")

    # Get or create NER pipeline
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")

    # Add custom entity labels
    for label in ENTITY_LABELS:
        ner.add_label(label)

    # Get training data
    print("Loading training data...")
    training_data = create_training_data()
    print(f"Loaded {len(training_data)} training examples")

    # Convert to spaCy format
    examples = convert_to_spacy_format(training_data, nlp)

    # Disable other pipes during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

    print(f"\nTraining for {n_iter} iterations...")
    print("-" * 50)

    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()

        for iteration in range(n_iter):
            random.shuffle(examples)
            losses = {}

            for example in examples:
                nlp.update([example], drop=dropout, losses=losses)

            if (iteration + 1) % 5 == 0:
                print(f"Iteration {iteration + 1}/{n_iter}, Losses: {losses}")

    print("-" * 50)
    print("Training complete!")

    # Save model
    print(f"\nSaving model to {output_dir}...")
    nlp.to_disk(output_dir)
    print("Model saved successfully!")

    # Test the model
    print("\n" + "=" * 50)
    print("Testing the trained model")
    print("=" * 50)

    test_texts = [
        "Jane Doe, Software Engineer at Apple, proficient in Swift and Python.",
        "Bachelor of Science from Harvard University, graduated 2021.",
        "Experience with AWS, Docker, and Kubernetes at Netflix.",
    ]

    for text in test_texts:
        print(f"\nInput: {text}")
        doc = nlp(text)
        if doc.ents:
            for ent in doc.ents:
                print(f"  {ent.label_}: {ent.text}")
        else:
            print("  No entities found")

    return nlp


def evaluate_model(nlp, test_data=None):
    """Evaluate the trained model on test data."""
    if test_data is None:
        test_data = create_training_data()[-2:]  # Use last 2 examples for testing

    examples = convert_to_spacy_format(test_data, nlp)

    scorer = spacy.scorer.Scorer()
    scores = scorer.score(examples)

    print("\n" + "=" * 50)
    print("Model Evaluation")
    print("=" * 50)
    print(f"Precision: {scores['ents_p']:.2%}")
    print(f"Recall: {scores['ents_r']:.2%}")
    print(f"F1 Score: {scores['ents_f']:.2%}")

    return scores


if __name__ == "__main__":
    # Train the model
    model_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "models", "resume_ner"
    )
    trained_nlp = train_ner_model(output_dir=model_path, n_iter=30)

    # Evaluate
    evaluate_model(trained_nlp)
