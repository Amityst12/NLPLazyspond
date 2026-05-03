import json
import os

def main():
    print("Reading existing data...")
    with open("instagram_replies.json", "r", encoding="utf-8") as f:
        existing_data = json.load(f)
        
    print(f"Found {len(existing_data)} existing records.")

    # Synthetic data generated directly by the AI assistant (acting as the LLM)
    new_data = [
        # LEAD
        {"text": "כמה עולה משלוח לתל אביב?", "label": "LEAD"},
        {"text": "איך אני מזמין את החולצה הלבנה?", "label": "LEAD"},
        {"text": "יש את זה בעוד צבעים?", "label": "LEAD"},
        {"text": "אפשר לקבל לינק לקנייה?", "label": "LEAD"},
        {"text": "כמה עולה אחי?", "label": "LEAD"},
        {"text": "price please", "label": "LEAD"},
        {"text": "שלח פרטים בפרטי", "label": "LEAD"},
        {"text": "מתי זה חוזר למלאי???", "label": "LEAD"},
        {"text": "יש לכם קוד קופון?", "label": "LEAD"},
        {"text": "מאיפה אוספים את זה?", "label": "LEAD"},
        {"text": "אפשר לשלם בביט או פייבוקס?", "label": "LEAD"},
        {"text": "תשלח לי לינק מהר אני רוצה לקנות", "label": "LEAD"},
        {"text": "האם יש משלוחים גם לצפון?", "label": "LEAD"},
        {"text": "how much for the whole set?", "label": "LEAD"},
        {"text": "שלח הודעה בפרטי לגבי מחירים", "label": "LEAD"},
        {"text": "איפה קונים את זה כפרה?", "label": "LEAD"},
        {"text": "אני חייבת כזה! מאיפה?", "label": "LEAD"},
        {"text": "יש מידה לארג' מזה?", "label": "LEAD"},
        {"text": "דבר איתי כמה עולה", "label": "LEAD"},
        {"text": "link in dm plz", "label": "LEAD"},
        {"text": "היי מתי יהיה זמין שוב בסניף?", "label": "LEAD"},
        {"text": "אפשר להזמין עכשיו ולקבל מחר?", "label": "LEAD"},
        {"text": "איך נרשמים לתוכנית שלכם?", "label": "LEAD"},
        {"text": "יש הנחת חיילים?", "label": "LEAD"},
        {"text": "תגיד יש תשלומים ללא ריבית?", "label": "LEAD"},

        # SUPPORT
        {"text": "הזמנתי לפני שבועיים ועוד לא קיבלתי אישור!", "label": "SUPPORT"},
        {"text": "אחי הלינק שבור לא עובד לי", "label": "SUPPORT"},
        {"text": "איך אני מבטל את ההזמנה שעשיתי הרגע?", "label": "SUPPORT"},
        {"text": "שלחתי לכם הודעה בוואטסאפ ולא עונים", "label": "SUPPORT"},
        {"text": "יש באג באפליקציה זה קורס לי בכניסה", "label": "SUPPORT"},
        {"text": "לא מצליח לשחזר סיסמה", "label": "SUPPORT"},
        {"text": "my package didn't arrive", "label": "SUPPORT"},
        {"text": "תענו בשירות לקוחות אני מחכה שעה", "label": "SUPPORT"},
        {"text": "חויבתי פעמיים באשראי למה זה???", "label": "SUPPORT"},
        {"text": "איך מחזירים מוצר פגום?", "label": "SUPPORT"},
        {"text": "האתר שלכם קרס באמצע התשלום איזה פיזדץ", "label": "SUPPORT"},
        {"text": "אני מנסה להתחבר וזה כותב שגיאה 500", "label": "SUPPORT"},
        {"text": "לא עובד לי הקופון שפרסמתם", "label": "SUPPORT"},
        {"text": "help my app is crashing", "label": "SUPPORT"},
        {"text": "היי המשלוח שלי הגיע קרוע, מה עושים?", "label": "SUPPORT"},
        {"text": "אפשר לדבר עם נציג אנושי?", "label": "SUPPORT"},
        {"text": "הורדתי את התוכנה וזה לא נפתח במק", "label": "SUPPORT"},
        {"text": "שכחתי את המייל שלי למערכת, איך מסדרים את זה?", "label": "SUPPORT"},
        {"text": "שגיאה 404 כשאני לוחץ על הקישור לקנייה", "label": "SUPPORT"},
        {"text": "i need technical support please", "label": "SUPPORT"},
        {"text": "המוצר הגיע במידה לא נכונה!", "label": "SUPPORT"},
        {"text": "שלחתי מייל ועדיין אין תשובה...", "label": "SUPPORT"},
        {"text": "למה התשלום בפייפאל נכשל כל הזמן?", "label": "SUPPORT"},
        {"text": "יש לכם מספר טלפון לשירות?", "label": "SUPPORT"},
        {"text": "המערכת שלכם איטית בטירוף אי אפשר לעבוד ככה", "label": "SUPPORT"},

        # SPAM
        {"text": "כנסו לקישור בביו שלי לעוקבים בחינם!", "label": "SPAM"},
        {"text": "collab? dm us immediately", "label": "SPAM"},
        {"text": "send pic to @big_brand_pages", "label": "SPAM"},
        {"text": "רוצה לעשות 10,000 שקל בחודש מהבית? כנסו לסטורי שלי", "label": "SPAM"},
        {"text": "dm me for crypto tips and tricks", "label": "SPAM"},
        {"text": "fsdfsdfsdfs", "label": "SPAM"},
        {"text": "get verified for cheap. link in bio", "label": "SPAM"},
        {"text": "הלוואות בלי ערבים שלחו הודעה", "label": "SPAM"},
        {"text": "promote it on @israel_viral", "label": "SPAM"},
        {"text": "hot girls in my bio check it out 🔥🔥🔥", "label": "SPAM"},
        {"text": "עוקבים ולייקים באינסטגרם בהנחה מטורפת", "label": "SPAM"},
        {"text": "invest 50$ get 5000$ msg me", "label": "SPAM"},
        {"text": "buy fast followers and views link in bio", "label": "SPAM"},
        {"text": "sdasdsa asdsd", "label": "SPAM"},
        {"text": "קבוצת טלגרם סודית להרוויח מיליונים - לינק בביו", "label": "SPAM"},
        {"text": "DM @promote_page_2026 to get featured!", "label": "SPAM"},
        {"text": "vfvbfbfbfbf", "label": "SPAM"},
        {"text": "פתיחת מזל והחזרת אהבות דברו איתי", "label": "SPAM"},
        {"text": "win a free iphone just click the link", "label": "SPAM"},
        {"text": "בוטים ושרתים לאינסטגרם - מחיר רצפה", "label": "SPAM"},
        {"text": "message for shoutout and promos", "label": "SPAM"},
        {"text": "crypto trading bot is live see my stories", "label": "SPAM"},
        {"text": "עבודה מהבית שעתיים ביום 20 אלף שקל בחודש שלחו פרטי", "label": "SPAM"},
        {"text": "increase your reach with us DM NOW", "label": "SPAM"},
        {"text": "הרווחתי מלא כסף תודה לאל תבדקו את הפרופיל", "label": "SPAM"},

        # IDLE
        {"text": "חחחחחח שרוף עליך!", "label": "IDLE"},
        {"text": "פסיכי לגמרי אחי", "label": "IDLE"},
        {"text": "אח יקר אתה אין דברים כאלה", "label": "IDLE"},
        {"text": "😍😍😍😍", "label": "IDLE"},
        {"text": "וואלה אתה גאון", "label": "IDLE"},
        {"text": "מתתתת עליך", "label": "IDLE"},
        {"text": "lmao this is too good", "label": "IDLE"},
        {"text": "פיזדץ מטורף!", "label": "IDLE"},
        {"text": "חיים שלי אהבתי רצח", "label": "IDLE"},
        {"text": "🔥❤️🔥❤️", "label": "IDLE"},
        {"text": "איזה מלך וואו", "label": "IDLE"},
        {"text": "הרגת אותי מצחוק חחחח", "label": "IDLE"},
        {"text": "niceeeeee", "label": "IDLE"},
        {"text": "שמע זה אדיר", "label": "IDLE"},
        {"text": "omggg yes", "label": "IDLE"},
        {"text": "תותח מלידה", "label": "IDLE"},
        {"text": "יואו מטורףףף", "label": "IDLE"},
        {"text": "אין עליכם בעולם", "label": "IDLE"},
        {"text": "וואו איזה סטייל 👑", "label": "IDLE"},
        {"text": "חזק ביותר", "label": "IDLE"},
        {"text": "יא אללה איזה רמה", "label": "IDLE"},
        {"text": "love ittt", "label": "IDLE"},
        {"text": "בוכה מרוב צחוק", "label": "IDLE"},
        {"text": "שברת את הרשת אחי", "label": "IDLE"},
        {"text": "💯💯💯", "label": "IDLE"},
    ]
    
    print(f"Generated {len(new_data)} new synthetic examples locally.")

    combined = existing_data + new_data

    # Remove exact text duplicates
    seen = set()
    unique_data = []
    for item in combined:
        if item["text"] not in seen:
            seen.add(item["text"])
            unique_data.append(item)

    print(f"Total unique records after merge: {len(unique_data)}")

    output_file = "instagram_replies_large.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(unique_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved to {output_file}")

if __name__ == "__main__":
    main()
