import os
import sqlite3
import database

def setup_module(module):
    # ensure fresh database for tests
    if os.path.exists(database.DB_PATH):
        os.remove(database.DB_PATH)
    database.init_db()


def test_create_and_authenticate_user():
    assert database.create_user("foo@example.com", "secret")
    # duplicate should fail
    assert not database.create_user("foo@example.com", "secret")
    assert database.authenticate_user("foo@example.com", "secret")
    assert not database.authenticate_user("foo@example.com", "wrong")
    assert not database.authenticate_user("nonexistent@example.com", "secret")


def test_crop_entries_present():
    crops = database.get_crops()
    assert "Wheat" in crops
    info = database.get_crop_info("Rice")
    assert info["water"] == "Very high"
