import json
import random
import os

def generate_leads(count):
    prefixes = ["אחי ", "כפרה ", "נשמה ", "תגיד ", "wow ", "אפשר שאלה? ", ""]
    subjects = ["מחיר", "מכיר", "mehir", "how much", "כמה עולה", "כמה", "איך מזמינים", "link", "לינק", "משלוח", "mishloah"]
    suffixes = ["?", " ??", " פליז", " plz", " לפרטי", " brother", ""]
    extras = [" יש הנחה", " להיום", " מהר", " עכשיו"]
    
    res = set()
    while len(res) < count:
        text = random.choice(prefixes) + random.choice(subjects) + random.choice(["", random.choice(extras)]) + random.choice(suffixes)
        text = text.strip()
        if len(text) > 3 and "\n" not in text:
            res.add(text)
    return list(res)

def generate_support(count):
    prefixes = ["wtf ", "סעמק ", "למה ", "תגידו ", "אוף ", "הלו ", ""]
    subjects = ["לא עובד", "נשבר לי", "lo oved", "bag", "באג", "לא קיבלתי", "אין מענה", "שירות פח", "שגיאה 500", "error"]
    suffixes = ["!", " !!", " תעזרו לי", " help", " מתי עונים", ""]
    extras = [" כבר שבוע", " אתמול", " בכרום", " באתר"]
    
    res = set()
    while len(res) < count:
        text = random.choice(prefixes) + random.choice(subjects) + random.choice(["", random.choice(extras)]) + random.choice(suffixes)
        text = text.strip()
        if len(text) > 3 and "\n" not in text:
            res.add(text)
    return list(res)

def generate_spam(count):
    prefixes = ["לפרטים ", "כנסו ", "invest ", "buy ", "free ", "follow ", ""]
    subjects = ["ביטקוין", "crypto", "onlyfans", "עוקב על עוקב", "לייקים", "likes", "bitcoin", "כסף קל", "עבודה מהבית"]
    suffixes = [" !!!", " בביו", " in bio", " DM ME", " 🔥", " 🤑", ""]
    extras = [" עכשיו", " מהר", " 100%", " בחינם"]
    
    res = set()
    while len(res) < count:
        text = random.choice(prefixes) + random.choice(subjects) + random.choice(["", random.choice(extras)]) + random.choice(suffixes)
        text = text.strip()
        if len(text) > 3 and "\n" not in text:
            res.add(text)
    return list(res)

def generate_idle(count):
    prefixes = ["חחח ", "פחחח ", "יואו ", "אמאל'ה ", "omg ", "slay ", ""]
    subjects = ["איזה יופי", "מושלם", "mushlam", "yasss", "lol", "🔥", "מהמם", "נדיר", "nadier", "@daniel", "@moshe"]
    suffixes = [" 😍", " גאוני", " !!!", " ❤️", " 💯", ""]
    extras = [" אין דברים כאלה", " היום", " פשוט", ""]
    
    res = set()
    while len(res) < count:
        text = random.choice(prefixes) + random.choice(subjects) + random.choice(["", random.choice(extras)]) + random.choice(suffixes)
        text = text.strip()
        if len(text) > 3 and "\n" not in text:
            res.add(text)
    return list(res)


with open("instagram_replies_large.json", "r", encoding="utf-8") as f:
    data = json.load(f)

existing_texts = set(x["text"] for x in data)

from collections import Counter
counts = Counter(x["label"] for x in data)
print("Before:", counts)

needed = {
    "LEAD": 250 - counts.get("LEAD", 0),
    "SUPPORT": 250 - counts.get("SUPPORT", 0),
    "SPAM": 250 - counts.get("SPAM", 0),
    "IDLE": 250 - counts.get("IDLE", 0),
}

for label, func in [("LEAD", generate_leads), ("SUPPORT", generate_support), ("SPAM", generate_spam), ("IDLE", generate_idle)]:
    n = needed[label]
    new_items_generated = 0
    while new_items_generated < n:
        candidates = func(n * 2)
        for c in candidates:
            if c not in existing_texts and new_items_generated < n:
                data.append({"text": c, "label": label})
                existing_texts.add(c)
                new_items_generated += 1

counts_after = Counter(x["label"] for x in data)
print("After:", counts_after)
print(f"Total dataset size: {len(data)}")

with open("instagram_replies_large.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
