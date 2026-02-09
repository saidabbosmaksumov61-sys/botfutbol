import asyncio
from unittest.mock import MagicMock, AsyncMock
import database
import handlers
import scheduler
import os

# Setup test DB
TEST_DB = "verify_notification_fix.db"
database.DB_NAME = TEST_DB
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
database.init_db()

# Mock dependencies
mock_api = MagicMock()
handlers.api = mock_api
scheduler.api = mock_api
mock_bot = AsyncMock()

async def verify():
    print("--- Verifying Notification Fixes ---")
    
    user_id = 999
    database.add_user(user_id, "uz") # Add user first
    
    league_id = 47
    team_id = 1
    team_name = "Arsenal"
    
    # 1. Test Favoriting (Team Name Fetching)
    handlers.temp_state[user_id] = league_id
    mock_api.get_teams.return_value = [{"id": team_id, "name": team_name}]
    
    # Simulate fav_ callback
    callback = MagicMock()
    callback.from_user.id = user_id
    callback.data = f"fav_{team_id}"
    callback.message.edit_reply_markup = AsyncMock()
    callback.answer = AsyncMock()
    
    print("Testing favorite toggle...")
    await handlers.toggle_favorite(callback)
    
    user = database.get_user(user_id)
    if user and user['fav_team_name'] == team_name:
        print(f"✅ SUCCESS: Real team name '{team_name}' saved to DB.")
    else:
        print(f"❌ FAILED: Saved team name: {user['fav_team_name'] if user else 'None'}")

    # 2. Test Formatting (Scorecard layout)
    print("\nTesting message formatting...")
    lang = "uz"
    home = "Atalanta"
    away = "Cremonese"
    score = "v"
    
    formatted = scheduler.format_match_info(lang, home, away, score, "Upcoming", False, False, "")
    print(f"Formatted message:\n{formatted}")
    
    if "\n" not in formatted and "| ⏳" in formatted:
        print("✅ SUCCESS: Scorecard formatting is more compact and on one line.")
    else:
        print("❌ FAILED: Unexpected formatting.")

    # Cleanup
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

if __name__ == "__main__":
    asyncio.run(verify())
