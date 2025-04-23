
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

SPREADSHEET_NAME = 'NetWatch 2025 Testimony Form (Responses)'
NEWS_FILE = 'news.html'

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).sheet1

data = sheet.get_all_records()
formatted_blocks = []

for row in data:
    story = row.get("What’s your experience or story?")
    state = row.get("What state are you in?")
    permission = row.get("Do you want your story to be shared publicly?")
    name = row.get("What should we call you?")

    if story and "yes" in permission.lower():
        label = name if name else f"Anonymous, {state}" if state else "Anonymous"
        formatted_blocks.append(f'''
        <div class="testimony-block">
          “{story.strip()}” — {label}
        </div>
        ''')

timestamp = datetime.now().strftime("%B %d, %Y – %I:%M %p")

clock_bar = f'''
<div id="clock-container">
  <span id="clock-time">Loading time...</span> | 🕒 Last updated: {timestamp}
</div>
<script>
function updateClock() {{
  const now = new Date();
  const options = {{
    hour: '2-digit', minute: '2-digit', second: '2-digit',
    weekday: 'short', year: 'numeric', month: 'short', day: 'numeric'
  }};
  document.getElementById('clock-time').textContent = now.toLocaleString('en-US', options);
}}
setInterval(updateClock, 1000);
window.onload = updateClock;
</script>
'''

with open(NEWS_FILE, "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('<body>', f'<body>\n{clock_bar}')

start = html.find('<section id="testimony">')
end = html.find('</section>', start)
if start != -1 and end != -1:
    before = html[:end]
    after = html[end:]
    new_html = before + "\n" + "\n".join(formatted_blocks) + "\n" + after
else:
    new_html = html

with open(NEWS_FILE, "w", encoding="utf-8") as f:
    f.write(new_html)

print("✅ Testimonies updated successfully.")
