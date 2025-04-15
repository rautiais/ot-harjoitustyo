import os

DIRNAME = os.path.dirname(__file__)

DATABASE_FILENAME = "database.sqlite"
DATABASE_FILE_PATH = os.path.join(DIRNAME, "..", "data", DATABASE_FILENAME)

TEST_DATABASE_FILENAME = "test-database.sqlite"
TEST_DATABASE_FILE_PATH = os.path.join(
    DIRNAME, "..", "data", TEST_DATABASE_FILENAME)
