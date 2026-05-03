import json
import os

def main():
    print("Generating massive local dataset...")
    
    new_data = [
        # LEAD (50 items)
        {"text": "כמה עלה לכם לייצר את זה? רוצה לקנות בסיטונאות", "label": "LEAD"},
        {"text": "אחי איפה החנות שלכם ממוקמת?", "label": "LEAD"},
        {"text": "how much is it with delivery?", "label": "LEAD"},
        {"text": "יש את זה במידה M?", "label": "LEAD"},
        {"text": "וואלה אהבתי, אפשר לשלם בהעברה בנקאית?", "label": "LEAD"},
        {"text": "כמה זמן לוקח משלוח לירושלים?", "label": "LEAD"},
        {"text": "send link for purchase plz", "label": "LEAD"},
        {"text": "אפשר פרטים על הקורס בפרטי?", "label": "LEAD"},
        {"text": "איך נרשמים אחים שלי?", "label": "LEAD"},
        {"text": "יש לכם קוד קופון של משפיענים אולי?", "label": "LEAD"},
        {"text": "תגיד אם אני לוקח 2 יש הנחה?", "label": "LEAD"},
        {"text": "where can i buy this??", "label": "LEAD"},
        {"text": "איך אני מזמינה כזה בורוד?", "label": "LEAD"},
        {"text": "יש אחריות על המוצר הזה?", "label": "LEAD"},
        {"text": "מתי אתם פתוחים ביום שישי בא לי לבוא לקנות", "label": "LEAD"},
        {"text": "אפשר לינק בפרטי בבקשה? אני לא מוצאת באתר", "label": "LEAD"},
        {"text": "I want to buy this right now", "label": "LEAD"},
        {"text": "שלח לי בפרטי מספר טלפון להזמנות", "label": "LEAD"},
        {"text": "האם זה מתאים גם לגברים?", "label": "LEAD"},
        {"text": "מחיר כפרה?", "label": "LEAD"},
        {"text": "כמה עולה סט שלם?", "label": "LEAD"},
        {"text": "אפשר לשלם בתשלומים?", "label": "LEAD"},
        {"text": "אחי יש לכם משלוחים מעבר לקו הירוק?", "label": "LEAD"},
        {"text": "is there a black friday discount?", "label": "LEAD"},
        {"text": "וואו איך אני משיג את זה?", "label": "LEAD"},
        {"text": "תגידו מי מכין את זה? אפשר להזמין עיצוב אישי?", "label": "LEAD"},
        {"text": "מה המחיר של השחור?", "label": "LEAD"},
        {"text": "link plsss", "label": "LEAD"},
        {"text": "יש החזרות במידה וזה לא מתאים?", "label": "LEAD"},
        {"text": "כפרה שלח קישור לאתר", "label": "LEAD"},
        {"text": "איך אני מוסיף את זה לעגלה?", "label": "LEAD"},
        {"text": "יש איסוף עצמי מראשון לציון?", "label": "LEAD"},
        {"text": "how to order?", "label": "LEAD"},
        {"text": "כמה זה יוצא עם משלוח אקספרס?", "label": "LEAD"},
        {"text": "אני רוצה להזמין לאישה, תוך כמה זמן מגיע?", "label": "LEAD"},
        {"text": "מתי מגיע המלאי החדש? אני מחכה לקנות", "label": "LEAD"},
        {"text": "price?", "label": "LEAD"},
        {"text": "יש אפשרות לשלם למשלוחן במזומן?", "label": "LEAD"},
        {"text": "אחי זה במלאי כרגע?", "label": "LEAD"},
        {"text": "תגיד אפשר פרטים מלאים על מה זה כולל?", "label": "LEAD"},
        {"text": "מאיפה קונים???", "label": "LEAD"},
        {"text": "אפשר לקבל קטלוג בפרטי?", "label": "LEAD"},
        {"text": "יש כזה גם במידות גדולות יותר? אני אקנה", "label": "LEAD"},
        {"text": "send me the checkout link", "label": "LEAD"},
        {"text": "איך אני עושה מנוי שנתי?", "label": "LEAD"},
        {"text": "אפשר לשלם בביט באתר?", "label": "LEAD"},
        {"text": "מחכה שיחזור למלאי בשביל להזמין", "label": "LEAD"},
        {"text": "אח שלי כמה עולה להשכיר את זה?", "label": "LEAD"},
        {"text": "איפה רואים את המחירים?", "label": "LEAD"},
        {"text": "אני מעוניין לרכוש, שלחו לי מספר", "label": "LEAD"},

        # SUPPORT (50 items)
        {"text": "האתר שלכם נפל לי באמצע התשלום, חויבתי?", "label": "SUPPORT"},
        {"text": "אחי אני מנסה להתחבר וזה עושה error 502", "label": "SUPPORT"},
        {"text": "החבילה שלי הגיעה שבורה פיזדץ!", "label": "SUPPORT"},
        {"text": "לא קיבלתי אישור הזמנה למייל", "label": "SUPPORT"},
        {"text": "i forgot my password and reset email is not arriving", "label": "SUPPORT"},
        {"text": "המסך נתקע לי כל פעם שאני פותחת את האפליקציה", "label": "SUPPORT"},
        {"text": "אי אפשר ללחוץ על הכפתור אישור, זה באג", "label": "SUPPORT"},
        {"text": "עשיתי טעות בכתובת המשלוח איך משנים?", "label": "SUPPORT"},
        {"text": "הקוד קופון משום מה לא מזדכה בסל", "label": "SUPPORT"},
        {"text": "why is the site down?", "label": "SUPPORT"},
        {"text": "לא מצליח לשים כרטיס אשראי הוא לא שומר אותו", "label": "SUPPORT"},
        {"text": "אחי זה כבר שבועיים במכס מה נסגר", "label": "SUPPORT"},
        {"text": "הבאתם לי חולצה לא במידה שלי איזה מעצבן", "label": "SUPPORT"},
        {"text": "איך אני מוחק את המשתמש שלי?", "label": "SUPPORT"},
        {"text": "where is your customer service number?", "label": "SUPPORT"},
        {"text": "אני שולח הודעות בוואטסאפ ולא עונים לי מאתמול", "label": "SUPPORT"},
        {"text": "האפליקציה פשוט קורסת", "label": "SUPPORT"},
        {"text": "סליחה אבל המוצר לא נדלק לי בכלל", "label": "SUPPORT"},
        {"text": "זה עושה לי loading שעה בלי להתקדם", "label": "SUPPORT"},
        {"text": "help with my account please", "label": "SUPPORT"},
        {"text": "קיבלתי מייל ביטול למרות שלא ביטלתי", "label": "SUPPORT"},
        {"text": "עשיתם לי חיוב כפול בחשבון אשראי!", "label": "SUPPORT"},
        {"text": "הלינק בביו שבור", "label": "SUPPORT"},
        {"text": "החשבון שלי ננעל פתאום", "label": "SUPPORT"},
        {"text": "i can't login it says wrong credentials", "label": "SUPPORT"},
        {"text": "הסרטון של ההדרכה פשוט לא עובד אצלי", "label": "SUPPORT"},
        {"text": "האוטומציה שעשיתי לא נשלחת", "label": "SUPPORT"},
        {"text": "שלחתי מוצר חזרה ועוד לא ראיתי זיכוי", "label": "SUPPORT"},
        {"text": "יש לי שגיאה system error 100", "label": "SUPPORT"},
        {"text": "my payment failed but money was taken", "label": "SUPPORT"},
        {"text": "למה אי אפשר לעשות העתק הדבק באתר שלכם?", "label": "SUPPORT"},
        {"text": "לא קיבלתי את הקוד בSMS", "label": "SUPPORT"},
        {"text": "השרת שלכם איטי ברמות על", "label": "SUPPORT"},
        {"text": "ניסיתי לשנות סיסמה וזה לא עובד לי", "label": "SUPPORT"},
        {"text": "how to contact support?", "label": "SUPPORT"},
        {"text": "החלפתי טלפון וזה לא משחזר לי את הרכישות", "label": "SUPPORT"},
        {"text": "מישהו פרץ לי לחשבון תעזרו לי דחוף", "label": "SUPPORT"},
        {"text": "קיבלתי משהו אחר לגמרי ממה שהזמנתי", "label": "SUPPORT"},
        {"text": "יש לי בעיה בחיבור לגוגל בחשבון שלכם", "label": "SUPPORT"},
        {"text": "the app is buggy", "label": "SUPPORT"},
        {"text": "הפיצ'ר החדש לא עובד בדפדפן כרום", "label": "SUPPORT"},
        {"text": "תענו כבר למייל ששלחתי!", "label": "SUPPORT"},
        {"text": "כל פעם שאני לוחץ על שמור זה מוחק לי הכל", "label": "SUPPORT"},
        {"text": "אחי לא קיבלתי כרטיסים למייל", "label": "SUPPORT"},
        {"text": "לא נותן לי לכתוב בעברית בטופס", "label": "SUPPORT"},
        {"text": "i have a problem with my order", "label": "SUPPORT"},
        {"text": "מנסה לשלוח פנייה באתר וזה לא שולח", "label": "SUPPORT"},
        {"text": "שירות לקוחות הכי גרוע שיש, למה לא עונים לטלפון?", "label": "SUPPORT"},
        {"text": "יש באג מטורף בחיפוש שלכם, לא מוצא כלום", "label": "SUPPORT"},
        {"text": "תסדרו את הבעיה עם החשבוניות המערכת לא שולחת למייל", "label": "SUPPORT"},

        # SPAM (50 items)
        {"text": "רוצה להרוויח 20,000 שקל מהספה? שלח הודעה בפרטי", "label": "SPAM"},
        {"text": "buy active followers real cheap check link in bio", "label": "SPAM"},
        {"text": "collab? DM us @israel_promote", "label": "SPAM"},
        {"text": "פתיחת מזל בטארוט החזרת אהבות כנסו", "label": "SPAM"},
        {"text": "dm me for crypto pump groups", "label": "SPAM"},
        {"text": "click the link in my bio to see my private photos 💋🔥", "label": "SPAM"},
        {"text": "הגרלה על אייפון 16!! לייק ותגובה אצלי בעמוד", "label": "SPAM"},
        {"text": "crypto daily signals check my story", "label": "SPAM"},
        {"text": "בואו לקבל וי כחול במחיר בדיחה, פרטים בפרטי", "label": "SPAM"},
        {"text": "promote your reel send it to @viral_hype", "label": "SPAM"},
        {"text": "רוצים שכל פוסט יגיע לאקספלור? קנו דרכנו שירותי קידום", "label": "SPAM"},
        {"text": "dm us pic for feature ❤️", "label": "SPAM"},
        {"text": "fsfdsfdsfsd", "label": "SPAM"},
        {"text": "hot singles in your area bio link", "label": "SPAM"},
        {"text": "מחפשת גברים דיסקרטים בואו לסטורי שלי חחח", "label": "SPAM"},
        {"text": "bitcoin investment return 300% in a week", "label": "SPAM"},
        {"text": "send it to @huge_israeli_page", "label": "SPAM"},
        {"text": "בואו להרוויח כסף קל בלי להתאמץ! תשלחו הודעה עכשיו", "label": "SPAM"},
        {"text": "לייקים ישראלים במחיר של שקל לעוקב", "label": "SPAM"},
        {"text": "invest in my new coin dm for whitelist", "label": "SPAM"},
        {"text": "עבודה מהבית 200 דולר ביום", "label": "SPAM"},
        {"text": "collab dm @brand_ambassadors", "label": "SPAM"},
        {"text": "קבוצת טלגרם בלי צנזורה כנסו ללינק בביו", "label": "SPAM"},
        {"text": "i made 10k today ask me how", "label": "SPAM"},
        {"text": "כנסו עכשיו לעמוד שלי אם אתם רוצים להיות עשירים", "label": "SPAM"},
        {"text": "שירותי קידום אורגני באינסטגרם בהנחה מטורפת", "label": "SPAM"},
        {"text": "check bio for spicy content 🌶️", "label": "SPAM"},
        {"text": "dfgdhfdsgdfg", "label": "SPAM"},
        {"text": "אנחנו מחפשים שגרירים למותג שלנו, שלחו הודעה!", "label": "SPAM"},
        {"text": "send us a dm to be a model", "label": "SPAM"},
        {"text": "מלווה בריבית חוקי אשראי מהיר בלי ערבים", "label": "SPAM"},
        {"text": "buy verification badge cheap", "label": "SPAM"},
        {"text": "רוצה להרוויח כסף מהטיקטוק? יש לי קורס בחינם בביו", "label": "SPAM"},
        {"text": "dm to buy shoutouts", "label": "SPAM"},
        {"text": "הצטרפו לערוץ הויאיפי שלנו בטלגרם לעדכונים חמים", "label": "SPAM"},
        {"text": "crypto trading bot 100% win rate", "label": "SPAM"},
        {"text": "עבודה קלה לנוער מכל הארץ דברו איתי", "label": "SPAM"},
        {"text": "free likes hack in my bio", "label": "SPAM"},
        {"text": "תלחצו על הלינק ותקבלו 50$ מתנה", "label": "SPAM"},
        {"text": "send pic to @repost_hub", "label": "SPAM"},
        {"text": "קוראת בקפה במחירים שווים לכל כיס", "label": "SPAM"},
        {"text": "get free followers just download app", "label": "SPAM"},
        {"text": "הלוואה למוגבלים בבנק אישור מיידי", "label": "SPAM"},
        {"text": "we love your vibe dm us for collab", "label": "SPAM"},
        {"text": "רוצה להתעשר? כנס לקישור המצורף בפרופיל שלי", "label": "SPAM"},
        {"text": "trade forex with me msg me", "label": "SPAM"},
        {"text": "פרצו לכם לחשבון? אני יכול לפרוץ חזרה רק דברו איתי", "label": "SPAM"},
        {"text": "only 5$ for 10k followers", "label": "SPAM"},
        {"text": "בואו להרוויח הכנסה פסיבית עכשיו", "label": "SPAM"},
        {"text": "we pay you to post on IG dm us", "label": "SPAM"},

        # IDLE (50 items)
        {"text": "חחחח איזה שרוטים בחיי", "label": "IDLE"},
        {"text": "וואלה אהבתי רצח", "label": "IDLE"},
        {"text": "יא אללה איזה רמה", "label": "IDLE"},
        {"text": "bro you are crazy", "label": "IDLE"},
        {"text": "פסיכי לחלוטין!", "label": "IDLE"},
        {"text": "אין עליכם בעולם כולו", "label": "IDLE"},
        {"text": "🔥🔥🔥 פשוט אש", "label": "IDLE"},
        {"text": "מתתת מרוב צחוק", "label": "IDLE"},
        {"text": "חיים שלי אתה", "label": "IDLE"},
        {"text": "omg this is epic", "label": "IDLE"},
        {"text": "מטורףףףף", "label": "IDLE"},
        {"text": "איזה יופי של דבר", "label": "IDLE"},
        {"text": "וואו זה נראה פגז", "label": "IDLE"},
        {"text": "חזקקקק אחי", "label": "IDLE"},
        {"text": "lmao ded 💀", "label": "IDLE"},
        {"text": "לא נושם חחחח", "label": "IDLE"},
        {"text": "יואוווו איזה סרטון", "label": "IDLE"},
        {"text": "אחלה גבר שבעולם", "label": "IDLE"},
        {"text": "שרוף עליכם יא תותחים", "label": "IDLE"},
        {"text": "wow amazing bro", "label": "IDLE"},
        {"text": "איזה סטייל מטורף", "label": "IDLE"},
        {"text": "פיזדץ נדיר!", "label": "IDLE"},
        {"text": "יא מלךךך", "label": "IDLE"},
        {"text": "👑👑👑 הכתר שלך", "label": "IDLE"},
        {"text": "חחחחח הכל מדויק", "label": "IDLE"},
        {"text": "love it", "label": "IDLE"},
        {"text": "אהבתי מאוד, נראה מעולה", "label": "IDLE"},
        {"text": "הלוואי עליי ככה", "label": "IDLE"},
        {"text": "שברתם אותי עכשיו חחח", "label": "IDLE"},
        {"text": "sick edit", "label": "IDLE"},
        {"text": "אלופים, פשוט אלופים", "label": "IDLE"},
        {"text": "יפה מאוד!", "label": "IDLE"},
        {"text": "אני עף על זה באוויר", "label": "IDLE"},
        {"text": "חחח מי הגאון שחשב על זה", "label": "IDLE"},
        {"text": "that is so cool", "label": "IDLE"},
        {"text": "טירוףףף", "label": "IDLE"},
        {"text": "הכי טובים שראיתי", "label": "IDLE"},
        {"text": "וואלה נותן לכם לייק על זה", "label": "IDLE"},
        {"text": "אליפות עולם", "label": "IDLE"},
        {"text": "respect", "label": "IDLE"},
        {"text": "יא תותחחח אין דברים כאלה", "label": "IDLE"},
        {"text": "חחחחחח איזה מוגזם", "label": "IDLE"},
        {"text": "אין מילים פשוט מושלם", "label": "IDLE"},
        {"text": "אחלה יום יא גבר", "label": "IDLE"},
        {"text": "so funny lmao", "label": "IDLE"},
        {"text": "שמעתם פעם על שלמות? זה זה", "label": "IDLE"},
        {"text": "קטלני אחי", "label": "IDLE"},
        {"text": "וואווו איזה קונספט מגניב", "label": "IDLE"},
        {"text": "חחחחח בא לי גם", "label": "IDLE"},
        {"text": "מדהיםםם פשוט מדהים", "label": "IDLE"},
    ]

    target_file = "instagram_replies_large.json"
    
    if os.path.exists(target_file):
        print(f"Loading existing {target_file}...")
        with open(target_file, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        print(f"File {target_file} not found. Creating a new list.")
        existing_data = []

    print(f"Found {len(existing_data)} existing records.")
    
    combined = existing_data + new_data
    
    # Remove exact text duplicates
    seen = set()
    unique_data = []
    for item in combined:
        if item["text"] not in seen:
            seen.add(item["text"])
            unique_data.append(item)

    print(f"Total unique records after merge: {len(unique_data)}")

    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(unique_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved to {target_file}")

if __name__ == "__main__":
    main()
