import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import transformers
if not hasattr(transformers, 'training_args'):
    import transformers.training_args
if not hasattr(transformers.training_args, 'default_logdir'):
    def default_logdir():
        import datetime
        return os.path.join("runs", datetime.datetime.now().strftime("%b%d_%H-%M-%S"))
    transformers.training_args.default_logdir = default_logdir
from setfit import SetFitModel

def main():
    print("Loading saved model...")
    model = SetFitModel.from_pretrained("./setfit_intent_model")

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
        pred_val = pred.item() if hasattr(pred, 'item') else pred
        label_str = inverse_label_map[pred_val]
        print(f"Text: {sentence} \nPrediction: {label_str}\n")

if __name__ == "__main__":
    main()
