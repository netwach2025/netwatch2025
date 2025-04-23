import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

# 1. SETUP Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Load testimony sheet
sheet = client.open("NetWatch 2025 Testimony Form (Responses)").sheet1
rows = sheet.get_all_records()

# Format testimonies
testimonies_html = ""
for row in rows:
    if "yes" in row["Do you want your story to be shared publicly?"].lower():
        name = row.get("What should we call you?", "Anonymous")
        state = row.get("What state are you in?", "")
        story = row.get("What’s your experience or story?", "").strip()
        label = f"{name}, {state}" if name and state else name
        if story:
            testimonies_html += f"""
            <div style="background-color: #fff4f4; border-left: 5px solid #cc0000; padding: 20px; margin: 20px 0; font-style: italic; border-radius: 6px;">
              “{story}” — {label}
            </div>
            """

# 2. SCRAPE WHITE HOUSE SOURCES
sources = [
    "https://www.whitehouse.gov/presidential-actions/",
    "https://www.whitehouse.gov/briefings-statements/",
    "https://www.whitehouse.gov/articles/",
    "https://www.whitehouse.gov/fact-sheets/",
    "https://www.whitehouse.gov/remarks/"
]

executive_html = ""
for url in sources:
    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")
    items = soup.select("li.briefing-statement__list-item")

    for item in items[:5]:
        title = item.find("a").text.strip()
        href = item.find("a")["href"]
        date = item.find("time").text.strip() if item.find("time") else "Date Unknown"
        full_link = href if href.startswith("http") else "https://www.whitehouse.gov" + href
        executive_html += f"<li><strong>{date}</strong>: <a href='{full_link}'>{title}</a></li>\n"

executive_html = f"<ul>\n{executive_html}</ul>"

# 3. INJECT INTO news.html
with open("news.html", "r", encoding="utf-8") as f:
    html = f.read()

# Inject testimonies
start = html.find('<div id="auto-testimonies">')
end = html.find('</div>', start) + 6
html = html[:start] + '<div id="auto-testimonies">\n' + testimonies_html + '\n</div>' + html[end:]

# Inject executive section
start_exec = html.find('<section id="executive-actions">')
end_exec = html.find('</section>', start_exec) + 10
if start_exec != -1 and end_exec != -1:
    html = html[:start_exec] + f"""
<section id="executive-actions" style="max-width: 900px; margin: 40px auto; padding: 0 20px; background: white; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.08);">
<h2 style="color:#1e4d6b;">Executive Orders & White House Updates</h2>
{executive_html}
</section>
""" + html[end_exec:]

# Update timestamp
now = datetime.now()
next_update = now + timedelta(days=1)
now_fmt = now.strftime("%B %d, %Y – %I:%M %p")
next_fmt = next_update.strftime("%B %d, %Y – %I:%M %p")

html = html.replace("🕒 Last updated:", f"🕒 Last updated: {now_fmt}  | 📅 Next update: {next_fmt}")

# Save file
with open("news.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ NetWatch site updated successfully.")
