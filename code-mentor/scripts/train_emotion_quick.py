import json, random
from pathlib import Path
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer

MODEL = "distilbert-base-uncased"
OUT = "models/emotion-small"
Path(OUT).mkdir(parents=True, exist_ok=True)

# 1) Load tiny dataset
rows = [json.loads(l) for l in Path("data/emotion.jsonl").read_text().splitlines()]
random.shuffle(rows)
split = max(1, int(0.8 * len(rows)))
train_rows, test_rows = rows[:split], rows[split:] or rows[:1]

tok = AutoTokenizer.from_pretrained(MODEL, use_fast=True)

def to_ds(items):
    enc = []
    for x in items:
        t = tok(x["text"], truncation=True, padding="max_length", max_length=96)
        t["labels"] = x["label"]
        enc.append(t)
    return Dataset.from_list(enc)

train_ds = to_ds(train_rows)
test_ds  = to_ds(test_rows)

# 2) Model
model = AutoModelForSequenceClassification.from_pretrained(MODEL, num_labels=2)

# 3) Arguments — keep it simple & compatible
args = TrainingArguments(
    output_dir="tmp_out",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    learning_rate=3e-5,
    logging_steps=5,
    save_strategy="no",     # no checkpointing to avoid strategy args issues
    report_to=[],           # disable wandb etc.
)

# 4) Train + manual eval
trainer = Trainer(model=model, args=args, train_dataset=train_ds, eval_dataset=test_ds)
trainer.train()
metrics = trainer.evaluate()
print("Eval metrics:", metrics)

# 5) Save fine-tuned model + tokenizer
trainer.save_model(OUT)
tok.save_pretrained(OUT)
print(f"Saved fine-tuned emotion model to {OUT}")
