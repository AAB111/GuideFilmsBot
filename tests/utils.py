from aiogram.types import User, Chat

TEST_USER = User(id=1080557340, is_bot=False, first_name="test_user", last_name="test_user", username="test_user")

TEST_USER_CHAT = Chat(id=140, type="private", username=TEST_USER.username, first_name=TEST_USER.first_name,
                      last_name=TEST_USER.last_name)

TEST_USER_NO_VALID = User(id=5, is_bot=False, first_name="test_user", last_name="test_user", username="test_user_2")
