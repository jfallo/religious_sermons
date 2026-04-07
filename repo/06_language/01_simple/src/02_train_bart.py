import pandas as pd
import torch
from itertools import combinations
from torch.utils.data import Dataset, DataLoader
from transformers import BartTokenizer, BartForConditionalGeneration
import os


if torch.backends.mps.is_available():
    device = torch.device('mps')
elif torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')
print(f"Using device: {device}")


# --- get train and validation data --- #

OSE_dir = "01_simple/input/one_stop_english_texts/"
level_order = {'Elementary': 0, 'Intermediate': 1, 'Advanced': 2}

def get_pairs(OSE_dir):
    pairs = []
    
    for file in os.listdir(OSE_dir):
        df = pd.read_csv(os.path.join(OSE_dir, file), encoding= 'latin-1')
        
        for _, row in df.iterrows():
            levels = [
                ('Elementary', row['Elementary']), 
                ('Intermediate', row['Intermediate']), 
                ('Advanced', row['Advanced'])
            ]
            
            for (level_a, text_a), (level_b, text_b) in combinations(levels, 2):
                pairs.append({
                    'prompt': f"Text A: {str(text_a)[:1000]} Text B: {str(text_b)[:1000]} Easier:",
                    'label': 'Text A'
                })
                pairs.append({
                    'prompt': f"Text A: {str(text_b)[:1000]} Text B: {str(text_a)[:1000]} Easier:",
                    'label': 'Text B'
                })
    
    return pd.DataFrame(pairs)

pairs_df = get_pairs(OSE_dir).sample(frac= 1, random_state= 42).reset_index(drop= True)
split = int(len(pairs_df) * 0.8)
train_df = pairs_df[:split].reset_index(drop= True)
val_df = pairs_df[split:].reset_index(drop= True)
print(f"Training samples: {len(train_df)}, Validation samples: {len(val_df)}")


# --- dataset --- #

class ReadabilityDataset(Dataset):
    def __init__(self, df, tokenizer, max_length= 512):
        self.df = df
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        inputs = self.tokenizer(
            row['prompt'],
            max_length= self.max_length,
            truncation= True,
            padding= 'max_length',
            return_tensors= 'pt'
        )

        labels = self.tokenizer(
            row['label'],
            max_length= 10,
            truncation= True,
            padding= 'max_length',
            return_tensors= 'pt'
        )

        label_ids = labels['input_ids'].squeeze()
        label_ids[label_ids == self.tokenizer.pad_token_id] = -100

        return {
            'input_ids': inputs['input_ids'].squeeze(),
            'attention_mask': inputs['attention_mask'].squeeze(),
            'labels': label_ids
        }


# --- model --- #

tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-base')
model.to(device)

train_dataset = ReadabilityDataset(train_df, tokenizer)
val_dataset = ReadabilityDataset(val_df, tokenizer)

train_loader = DataLoader(train_dataset, batch_size= 8, shuffle= True)
val_loader = DataLoader(val_dataset, batch_size= 8)

optimizer = torch.optim.AdamW(model.parameters(), lr= 1e-5)


# --- training --- #

best_val_acc = 0

for epoch in range(30):
    model.train()
    train_loss = 0

    for batch in train_loader:
        optimizer.zero_grad()
        output = model(
            input_ids= batch['input_ids'].to(device),
            attention_mask= batch['attention_mask'].to(device),
            labels= batch['labels'].to(device)
        )
        output.loss.backward()
        optimizer.step()
        train_loss += output.loss.item()

    # validation
    model.eval()
    correct = 0

    with torch.no_grad():
        for batch in val_loader:
            preds = model.generate(
                input_ids=batch['input_ids'].to(device),
                attention_mask=batch['attention_mask'].to(device),
                max_new_tokens= 10
            )
            decoded = tokenizer.batch_decode(preds, skip_special_tokens= True)

            label_ids = batch['labels'].clone()
            label_ids[label_ids == -100] = tokenizer.pad_token_id
            gold = tokenizer.batch_decode(label_ids, skip_special_tokens= True)

            correct += sum(d.strip() == g.strip() for d, g in zip(decoded, gold))

    val_acc = correct / len(val_dataset)
    avg_loss = train_loss / len(train_loader)
    print(f"Epoch {epoch+1:02d}: loss={avg_loss:.4f}, val_acc={val_acc:.3f}")

    # save best model
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        model.save_pretrained("01_simple/bart-simplicity")
        tokenizer.save_pretrained("01_simple/bart-simplicity")

print(f"\nTraining complete. Best validation accuracy: {best_val_acc:.3f}")
