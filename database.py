import os
from dotenv import load_dotenv
from postgrest import SyncPostgrestClient

# Load environment variables from the .env file
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Initialize the Postgrest client (the database part of Supabase)
supabase: SyncPostgrestClient | None = None

if SUPABASE_URL and SUPABASE_KEY:
    # Supabase REST endpoint is at /rest/v1
    rest_url = f"{SUPABASE_URL}/rest/v1"
    supabase = SyncPostgrestClient(
        rest_url,
        headers={"apikey": SUPABASE_KEY,
                 "Authorization": f"Bearer {SUPABASE_KEY}"}
    )
else:
    print("Warning: SUPABASE_URL or SUPABASE_KEY is missing in the environment variables.")
