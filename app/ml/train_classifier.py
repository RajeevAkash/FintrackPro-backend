"""
ML Training Script for Transaction Category Classifier.

Usage:
    python -m app.ml.train_classifier

Before running, update DATASET_PATH to your dataset CSV file location.
The CSV must have:
  - A text column (tried in order: 'description', 'transaction_description', 'text', 'title', 'narration')
  - A 'category' column with category labels
"""

import os
import sys

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# UPDATE THIS PATH to your dataset location, or set the DATASET_PATH environment variable
DATASET_PATH = os.getenv("DATASET_PATH", "path/to/your/dataset.csv")

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "artifacts", "transaction_clf.pkl")

TEXT_COLUMNS = ["description", "transaction_description", "text", "title", "narration"]


def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded dataset with {len(df)} rows and columns: {list(df.columns)}")
    return df


def get_text_column(df: pd.DataFrame) -> str:
    for col in TEXT_COLUMNS:
        if col in df.columns:
            print(f"Using text column: '{col}'")
            return col
    raise ValueError(
        f"No suitable text column found. Expected one of: {TEXT_COLUMNS}. "
        f"Found columns: {list(df.columns)}"
    )


def preprocess(df: pd.DataFrame, text_col: str) -> pd.DataFrame:
    df = df.dropna(subset=[text_col, "category"])
    df[text_col] = df[text_col].astype(str).str.lower().str.strip()
    df["category"] = df["category"].astype(str).str.strip()
    return df


def build_pipeline(classifier) -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=10000)),
        ("clf", classifier),
    ])


def train():
    if not os.path.exists(DATASET_PATH):
        print(f"ERROR: Dataset not found at '{DATASET_PATH}'.")
        print("Please update DATASET_PATH in app/ml/train_classifier.py.")
        sys.exit(1)

    df = load_dataset(DATASET_PATH)
    text_col = get_text_column(df)
    df = preprocess(df, text_col)

    X = df[text_col].values
    y = df["category"].values

    print(f"\nTotal samples after cleaning: {len(X)}")
    print(f"Unique categories: {sorted(set(y))}\n")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    classifiers = {
        "MultinomialNB": MultinomialNB(),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    }

    best_name = None
    best_accuracy = -1.0
    best_pipeline = None

    for name, clf in classifiers.items():
        print(f"Training {name}...")
        pipeline = build_pipeline(clf)
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"{name} Accuracy: {acc:.4f}")
        print(classification_report(y_test, y_pred))

        if acc > best_accuracy:
            best_accuracy = acc
            best_name = name
            best_pipeline = pipeline

    print(f"\nBest model: {best_name} with accuracy {best_accuracy:.4f}")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    joblib.dump(best_pipeline, OUTPUT_PATH)
    print(f"Model saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    train()
