import asyncio
from unittest.mock import MagicMock, AsyncMock
import database
import scheduler
import os

# Setup test DB
TEST_DB = "verify_fix.db"
database.DB_NAME = TEST_DB
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
database.init_db()

# Add test user
USER_ID = 999
database.add_user(USER_ID, "en")
TEAM_ID = 1
database.set_favorite(USER_ID, TEAM_ID, "Test Team")

# Mock dependencies
mock_api = MagicMock()
scheduler.api = mock_api
mock_bot = AsyncMock()

async def verify():
    print("--- Verifying Goal Notification Change ---")
    
    # Simulate a goal
    mock_api.get_all_matches.return_value = [{
        "id": 123,
        "home": "Arsenal",
        "away": "Chelsea",
        "home_id": TEAM_ID,
        "away_id": 2,
        "score": "1 - 0",
        "status_text": "12'",
        "is_live": True,
        "is_finished": False,
        "match_time": "12"
    }]
    
    # Mock match events with goalscorer
    mock_api.get_match_events.return_value = ["Bukayo Saka (12')"]
    
    # Run notification check
    await scheduler.check_live_notifications(mock_bot)
    
    if mock_bot.send_message.called:
        msg = mock_bot.send_message.call_args[0][1]
        print(f"Sent message:\n{msg}")
        
        # Check if Saka or time is in message
        if "Saka" in msg:
            print("❌ FAILED: Goalscorer name still present in notification!")
        elif "(12')" in msg:
             print("❌ FAILED: Goal time still present in notification!")
        else:
            print("✅ SUCCESS: Goal timing and scorer removed.")
    else:
        print("❌ FAILED: No notification sent!")

    # Cleanup
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

if __name__ == "__main__":
    asyncio.run(verify())
