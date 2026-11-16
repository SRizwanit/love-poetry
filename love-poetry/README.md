# প্রেমের কবিতা – GitHub Pages ওয়েবসাইট

`mylove.txt` (WhatsApp চ্যাট এক্সপোর্ট) থেকে Python দিয়ে স্বয়ংক্রিয়ভাবে ওয়েবসাইট তৈরি হয়।

## ব্যবহার
1. এই ফাইলগুলো GitHub repo-র `main` branch-এ পুশ করুন।
2. **Settings → Pages → Source = GitHub Actions** সিলেক্ট করুন।
3. `mylove.txt` এডিট করে commit করলেই সাইট নিজে আপডেট হবে।

লোকালি টেস্ট: `python build.py` → `site/index.html` ব্রাউজারে খুলুন।

## কাস্টমাইজ (`build.py`-এর উপরে)
- `LINES_PER_BOX` – প্রতি বক্সে লাইন সংখ্যা (৪)
- `WHATSAPP_NUMBER` – শেয়ার বাটনের নাম্বার
- `SENDER_FILTER` – শুধু একজনের মেসেজ নিতে চাইলে নাম দিন
