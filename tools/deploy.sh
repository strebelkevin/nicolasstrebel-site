#!/usr/bin/env bash
# Hardened deploy for nicolasstrebel.com (Cloudflare Pages).
# Syncs ONLY the public static site to the deploy folder, then publishes.
# Excludes anything that could carry secrets, source code, tooling, or internal CRM data.
# The API secret lives in ~/.config/sooprema/credentials.json and is never in this project,
# so it physically cannot be rsynced from here - this script is belt-and-braces on top of that.
set -euo pipefail

SRC="$(cd "$(dirname "$0")/.." && pwd)"
DEPLOY="${DEPLOY_DIR:-$HOME/Desktop/nicolasstrebel-deploy}"
mkdir -p "$DEPLOY"

rsync -a --delete \
  --exclude '.git' --exclude '.github' --exclude '.gitignore' \
  --exclude '*.py' --exclude '__pycache__' \
  --exclude 'tools' --exclude 'scrape' \
  --exclude 'data' \
  --exclude 'node_modules' --exclude '.DS_Store' --exclude '.claude' \
  --exclude '*.env' --exclude '.env' --exclude 'credentials.json' --exclude 'config.php' \
  --exclude '*sooprema*api*' --exclude '*.zip' \
  --exclude 'index-alt*.html' --exclude '_preview_guide.html' \
  "$SRC"/ "$DEPLOY"/
echo "Synced public site -> $DEPLOY"

# Safety net: read the real secret from the secure store (never hardcoded here) and
# refuse to publish if it somehow appears in the deploy folder.
CREDS="$HOME/.config/sooprema/credentials.json"
if [ -f "$CREDS" ]; then
  SECRET="$(python3 -c "import json;print(json.load(open('$CREDS')).get('secretKey',''))" 2>/dev/null || true)"
  if [ -n "$SECRET" ] && grep -rqF "$SECRET" "$DEPLOY" 2>/dev/null; then
    echo "ABORT: API secret key found in deploy folder. Not publishing." >&2
    exit 1
  fi
fi
# Note: functions/api/enquiry.js legitimately references the env-var NAME SOOPREMA_SECRET_KEY
# (read at runtime from Cloudflare). That's safe - we only block the actual secret VALUE above.
echo "Secret-leak check passed."

cd "$DEPLOY"
npx -y wrangler@latest pages deploy . --project-name nicolasstrebel --branch main
