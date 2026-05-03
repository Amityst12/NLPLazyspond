# Lazyspond Intent Classification: Hebrew/Heblish Instagram Replies

## 1. Project Overview
Lazyspond is an automation SaaS platform designed to streamline social media interactions. A significant challenge in this domain is handling noisy, unstructured direct messages (DMs) and story replies on Instagram, particularly in the Israeli demographic. 

The objective of this project is to build an Intent Classification system capable of categorizing short, informal Hebrew and "Heblish" (a mixture of Hebrew and English) texts into one of four distinct actionable categories:
- **LEAD:** High-intent users inquiring about pricing, product details, or purchase links.
- **SUPPORT:** Existing users experiencing technical issues, bugs, or needing assistance.
- **SPAM:** Automated bot messages, crypto scams, or generic collaboration requests.
- **IDLE:** Casual engagements such as emojis, laughter, or compliments with no actionable intent.

## 2. Data Engineering (Synthetic Data)
A primary challenge in this domain is the absence of publicly available, high-quality Hebrew datasets that capture authentic social media vernacular. To overcome this cold-start problem, we engineered a custom synthetic dataset utilizing Large Language Models (LLMs).

We generated approximately 400 highly authentic examples that mimic real-world Israeli users. The generation process strictly enforced:
- **Linguistic Realism:** Incorporation of common typos, heavy Israeli slang (e.g., "אח יקר", "פיזדץ"), Heblish, and emojis.
- **Class Balancing:** Ensuring a balanced distribution of examples across each of the 4 intent categories.
- **Nuanced Differentiation:** Establishing clear linguistic boundaries between genuine purchase intent (`LEAD`) and promotional bot behavior (`SPAM`).

## 3. Model Architecture & Training
Given the relatively small size of our custom dataset (~400 records), traditional fine-tuning of large transformer models would likely result in overfitting. To address this, we adopted **SetFit** (Sentence Transformer Fine-tuning), a highly efficient framework designed for Few-Shot Text Classification.

- **Base Model:** We utilized `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, an exceptionally fast and capable multilingual model.
- **Training Strategy:** SetFit operates in a two-stage process. First, it fine-tunes the Sentence Transformer body using contrastive learning on sentence pairs to generate robust embeddings. Second, it trains a classification head (Logistic Regression) on these enhanced embeddings.
- **Refinement:** Initial tests on a smaller subset showed instability. By expanding the synthetic dataset to nearly 400 diverse records, the model stabilized and learned to generalize effectively across the noisy linguistic variance.

## 4. Results & Zero-Shot Comparison
To scientifically validate our approach, we established a baseline using a state-of-the-art multilingual zero-shot classifier (`MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`). The test set constituted an 80/20 split (seed=42) of our dataset.

As hypothesized, the generic zero-shot model failed significantly. It struggled to map its pre-trained linguistic understanding to the highly localized, informal, and domain-specific Heblish slang. Conversely, our SetFit model demonstrated exceptional performance.

| Metric | Zero-Shot Baseline (`mDeBERTa-v3-base`) | Fine-Tuned SetFit |
|--------|---------------------------------------|-------------------|
| **Accuracy** | 21.79% | **94.87%** |
| **Precision** | 16.23% | **95.05%** |
| **Recall** | 21.50% | **94.62%** |
| **F1-Score** | 18.18% | **94.80%** |

*Note: The baseline accuracy of ~21% is statistically equivalent to random guessing among 4 classes, emphasizing the absolute necessity of our domain-specific fine-tuning.*

## 5. Evaluation Visuals
To further analyze the model's predictive boundaries, we generated a Confusion Matrix on the test set. 

This visualization (saved locally as `confusion_matrix.png`) allows us to inspect edge cases where the model might hesitate—for instance, distinguishing between a highly enthusiastic `IDLE` compliment and a `LEAD` query.

## 6. Next Steps
With the core algorithmic pipeline validated and achieving ~95% accuracy, the immediate next steps involve transitioning from experimentation to production:
- **Deployment:** Wrap the final saved model (`./setfit_lazyspond_final`) inside a highly concurrent API endpoint using **FastAPI**.
- **Integration:** Connect the inference API to the primary Lazyspond webhook system to route incoming Instagram story replies in real-time.
- **Continuous Learning:** Implement a feedback loop in the user dashboard to flag misclassifications, subsequently feeding this active data back into future SetFit training cycles.

## 7. How to Run the API

### Prerequisites

Install all dependencies using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

> **Note (Windows / Python 3.13):** Due to a known compatibility issue between `setfit` and recent versions of `transformers`, the `app.py` file includes a monkey-patch that resolves the `ImportError: cannot import name 'default_logdir'` error automatically. No manual intervention is needed.

### Starting the Server

Run the following command from the project root directory:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

The server will load the fine-tuned SetFit model into memory on startup and will be ready to serve requests at `http://127.0.0.1:8000`.

### Sending a Prediction Request

**Using Python (`requests`):**

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/predict",
    json={"text": "אחי כמה עולה משלוח לצפון?"}
)
print(response.json())
```

**Using cURL:**

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "אחי כמה עולה משלוח לצפון?"}'
```

### Expected Response

```json
{
  "text": "אחי כמה עולה משלוח לצפון?",
  "intent": "LEAD"
}
```

The API returns a JSON object with the original `text` and the predicted `intent` label (`LEAD`, `SUPPORT`, `SPAM`, or `IDLE`).

