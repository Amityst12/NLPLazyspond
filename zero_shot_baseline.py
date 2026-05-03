import json
import pandas as pd
from datasets import Dataset
from transformers import pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tqdm import tqdm

def main():
    print("Loading large dataset...")
    with open('instagram_replies_large.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)

    print("Preprocessing data and creating test set...")
    label_map = {"LEAD": 0, "SUPPORT": 1, "SPAM": 2, "IDLE": 3}
    df['label'] = df['label'].map(label_map)

    # Train/Test Split (must exactly match the SetFit split)
    dataset = Dataset.from_pandas(df)
    dataset = dataset.train_test_split(test_size=0.2, seed=42)
    test_dataset = dataset['test']

    texts = list(test_dataset['text'])
    true_labels = list(test_dataset['label'])

    print("Loading Zero-Shot pipeline (MoritzLaurer/mDeBERTa-v3-base-mnli-xnli) on GPU...")
    # device=0 loads it onto the first GPU (CUDA)
    classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli", device=0)

    candidate_labels = ["LEAD", "SUPPORT", "SPAM", "IDLE"]

    print(f"Running zero-shot predictions on {len(texts)} test samples...")
    # Using batch size for faster inference
    results = classifier(texts, candidate_labels, batch_size=16)

    predicted_labels = []
    for res in results:
        if isinstance(res, str):
            print("Error: res is a string!", res)
            continue
        # The top prediction is the first element in the 'labels' list
        top_label_str = res['labels'][0]
        predicted_labels.append(label_map[top_label_str])

    print("Calculating metrics...")
    acc = accuracy_score(true_labels, predicted_labels)
    prec = precision_score(true_labels, predicted_labels, average='macro')
    rec = recall_score(true_labels, predicted_labels, average='macro')
    f1 = f1_score(true_labels, predicted_labels, average='macro')

    metrics_str = (
        "--- Zero-Shot Baseline Metrics ---\n"
        f"Model: MoritzLaurer/mDeBERTa-v3-base-mnli-xnli\n"
        f"Accuracy:  {acc:.4f}\n"
        f"Precision: {prec:.4f}\n"
        f"Recall:    {rec:.4f}\n"
        f"F1-Score:  {f1:.4f}\n"
        "----------------------------------\n"
    )

    print("\n" + metrics_str)

    output_file = "zero_shot_baseline_results.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(metrics_str)
        
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
