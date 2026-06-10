import os
import sys

# Patch transformers so setfit doesn't fail on newer transformers versions
import transformers
if not hasattr(transformers, 'training_args'):
    import transformers.training_args
if not hasattr(transformers.training_args, 'default_logdir'):
    def default_logdir():
        import datetime
        return os.path.join("runs", datetime.datetime.now().strftime("%b%d_%H-%M-%S"))
    transformers.training_args.default_logdir = default_logdir

import json
import pandas as pd
from datasets import Dataset
from setfit import SetFitModel, Trainer, TrainingArguments

def main():
    # 2. Data Loading
    print("Loading data...")
    with open('instagram_replies.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)

    # 3. Preprocessing
    print("Preprocessing data...")
    label_map = {"LEAD": 0, "SUPPORT": 1, "SPAM": 2, "IDLE": 3}
    df['label'] = df['label'].map(label_map)

    dataset = Dataset.from_pandas(df)
    dataset = dataset.train_test_split(test_size=0.2, seed=42)
    train_dataset = dataset['train']
    eval_dataset = dataset['test']

    # 4. Model Initialization
    print("Initializing model...")
    from sentence_transformers import SentenceTransformer
    from sklearn.linear_model import LogisticRegression
    model_body = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    model_head = LogisticRegression()
    model = SetFitModel(model_body=model_body, model_head=model_head, multi_target_strategy=None)

    # 5. Training Setup & Execution
    print("Setting up training...")
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

    # 6. Evaluation & Saving
    print("Evaluating model...")
    metrics = trainer.evaluate()
    print("Evaluation results:", metrics)

    print("Saving model...")
    model.save_pretrained("./setfit_intent_model")

    # 7. Inference Test
    print("Running inference test...")
    test_sentences = [
        "כמה עולה המנוי שלכם?",
        "האוטומציה נתקעה לי באמצע",
        "חחחחח איזה גבר",
        "כנסו לקישור בביו שלי לעוקבים בחינם"
    ]

    preds = model.predict(test_sentences)
    
    inverse_label_map = {0: "LEAD", 1: "SUPPORT", 2: "SPAM", 3: "IDLE"}
    
    print("\n--- Predictions ---")
    for sentence, pred in zip(test_sentences, preds):
        # depending on numpy scalar vs standard int
        pred_val = pred.item() if hasattr(pred, 'item') else pred
        label_str = inverse_label_map[pred_val]
        print(f"Text: {sentence} \nPrediction: {label_str}\n")

if __name__ == "__main__":
    main()
