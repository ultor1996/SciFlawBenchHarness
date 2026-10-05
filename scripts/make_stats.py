import csv, io, json, os, urllib.request
from collections import Counter
from datetime import datetime, timezone

url = os.environ["SHEET_CSV_URL"]
text = urllib.request.urlopen(url).read().decode("utf-8")

counts = Counter()
for row in csv.DictReader(io.StringIO(text)):
    email = (row.get("Email address") or "").strip().lower()
    task = (row.get("Self-contained task description") or "").strip()
    if email and task:
        counts[email] += 1

out = {
    "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "total": sum(counts.values()),
    "contributors": [{"email": e, "tasks": n} for e, n in counts.most_common()],
}
with open("docs/stats.json", "w") as f:
    json.dump(out, f, indent=2)
