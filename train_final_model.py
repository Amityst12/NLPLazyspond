import os
import sys
import json
import pandas as pd
from datasets import Dataset
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Patch transformers so setfit doesn't fail on newer transformers versions
import transformers
if not hasattr(transformers, 'training_args'):
    import transformers.training_args
if not hasattr(transformers.training_args, 'default_logdir'):
    def default_logdir():
        import datetime
        return os.path.join("runs", datetime.datetime.now().strftime("%b%d_%H-%M-%S"))
    transformers.training_args.default_logdir = default_logdir

from setfit import SetFitModel, Trainer, TrainingArguments
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

def main():
    # 1. Load Data
    print("Loading large dataset...")
    with open('instagram_replies_large.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)

    # 2. Preprocessing & Label Mapping
    print("Preprocessing data...")
    label_map = {"LEAD": 0, "SUPPORT": 1, "SPAM": 2, "IDLE": 3}
    df['label'] = df['label'].map(label_map)

    # 3. Train/Test Split
    dataset = Dataset.from_pandas(df)
    dataset = dataset.train_test_split(test_size=0.2, seed=42)
    train_dataset = dataset['train']
    eval_dataset = dataset['test']

    # 4. Model Initialization & Training
    print("Initializing model on GPU...")
    model_body = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", device="cuda")
    model_head = LogisticRegression()
    model = SetFitModel(model_body=model_body, model_head=model_head, multi_target_strategy=None)

    args = TrainingArguments(
        batch_size=16,
        num_epochs=3,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        metric="accuracy"
    )

    print("Training model...")
    trainer.train()

    # 5. Evaluation metrics
    print("Evaluating model...")
    preds = model.predict(eval_dataset['text'])
    true_labels = eval_dataset['label']

    acc = accuracy_score(true_labels, preds)
    prec = precision_score(true_labels, preds, average='macro')
    rec = recall_score(true_labels, preds, average='macro')
    f1 = f1_score(true_labels, preds, average='macro')

    print("\n--- Final Metrics ---")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print("---------------------\n")

    # 6. Confusion Matrix
    print("Generating Confusion Matrix...")
    cm = confusion_matrix(true_labels, preds)
    labels_str = ["LEAD", "SUPPORT", "SPAM", "IDLE"]

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels_str, yticklabels=labels_str)
    plt.title("Confusion Matrix - Instagram Replies")
    plt.xlabel("Predicted Intent")
    plt.ylabel("Actual Intent")
    
    plt.tight_layout()
    plt.savefig("confusion_matrix.png", dpi=300)
    plt.close()
    print("Saved confusion_matrix.png.")

    # 7. Save Model
    print("Saving final model...")
    model.save_pretrained("./setfit_intent_model_final")
    print("Done!")

if __name__ == "__main__":
    main()
