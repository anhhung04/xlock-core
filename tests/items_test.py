from unittest import TestCase
from tests import (
    override_get_db,
    insert_user,
    insert_item,
    insert_personal_item,
    insert_shared_item,
    insert_item_history,
    insert_sharing_history,
    insert_filling_history,
    gen_username,
    gen_password,
)
from repository.schemas.item import (
    Item,
    PersonalItem,
    SharedItem,
    ItemHistory,
    SharingHistory,
    FillingHistory,
)
from datetime import datetime, timezone
from uuid import uuid4


class ItemsTest(TestCase):
    def test_insert_item(self):
        db = next(override_get_db())
        user = insert_user(db, gen_username(), "user@example.com", gen_password())
        item = insert_item(
            db, user.id, "Item Name", "http://example.com", "item_type", "credentials"
        )

        item_n_db = db.query(Item).filter(Item.id == item.id).first()

        self.assertIsNotNone(item_n_db)
        self.assertEqual(item_n_db.name, "Item Name")
        self.assertEqual(item_n_db.url, "http://example.com")
        self.assertEqual(item_n_db.type, "item_type")
        self.assertEqual(item_n_db.credentials, "credentials")
        self.assertEqual(item_n_db.user_id, user.id)
        self.assertIsNotNone(item_n_db.added_at)
        self.assertIsNone(item_n_db.updated_at)

    def test_insert_personal_item(self):
        db = next(override_get_db())
        user = insert_user(db, gen_username(), "user@example.com", gen_password())
        item = insert_personal_item(
            db, user.id, "Personal Item Name", "http://example.com", "credentials"
        )

        personal_item_n_db = (
            db.query(PersonalItem).filter(PersonalItem.item_id == item.id).first()
        )

        self.assertIsNotNone(personal_item_n_db)
        self.assertEqual(personal_item_n_db.name, "Personal Item Name")
        self.assertEqual(personal_item_n_db.url, "http://example.com")
        self.assertEqual(personal_item_n_db.type, "personal_item")
        self.assertEqual(personal_item_n_db.credentials, "credentials")
        self.assertEqual(personal_item_n_db.user_id, user.id)

    def test_insert_shared_item(self):
        db = next(override_get_db())
        user = insert_user(db, gen_username(), "user@example.com", gen_password())
        item = insert_shared_item(
            db,
            user.id,
            "Shared Item Name",
            "http://example.com",
            "credentials",
            "private_key",
        )

        shared_item_n_db = (
            db.query(SharedItem).filter(SharedItem.item_id == item.id).first()
        )

        self.assertIsNotNone(shared_item_n_db)
        self.assertEqual(shared_item_n_db.name, "Shared Item Name")
        self.assertEqual(shared_item_n_db.url, "http://example.com")
        self.assertEqual(shared_item_n_db.type, "shared_item")
        self.assertEqual(shared_item_n_db.credentials, "credentials")
        self.assertEqual(shared_item_n_db.private_key, "private_key")
        self.assertEqual(shared_item_n_db.user_id, user.id)

    def test_insert_item_history(self):
        db = next(override_get_db())
        user = insert_user(db, gen_username(), "user@example.com", gen_password())
        item = insert_item(
            db, user.id, "Item Name", "http://example.com", "item_type", "credentials"
        )
        history = insert_item_history(
            db, item.id, "history_type", "New York", "192.168.0.1", "ACTIVE"
        )

        history_n_db = (
            db.query(ItemHistory).filter(ItemHistory.id == history.id).first()
        )

        self.assertIsNotNone(history_n_db)
        self.assertEqual(history_n_db.type, "history_type")
        self.assertEqual(history_n_db.location, "New York")
        self.assertEqual(history_n_db.ip, "192.168.0.1")
        self.assertEqual(history_n_db.status, "ACTIVE")
        self.assertEqual(history_n_db.item_id, item.id)

    def test_insert_sharing_history(self):
        db = next(override_get_db())
        provider = insert_user(
            db, gen_username(), "provider@example.com", gen_password()
        )
        recipient = insert_user(
            db, gen_username(), "recipient@example.com", gen_password()
        )
        item = insert_shared_item(
            db,
            provider.id,
            "Shared Item Name",
            "http://example.com",
            "credentials",
            "private_key",
        )
        sharing_history = insert_sharing_history(db, item.id, provider.id, recipient.id)

        sharing_history_n_db = (
            db.query(SharingHistory)
            .filter(SharingHistory.id == sharing_history.id)
            .first()
        )

        self.assertIsNotNone(sharing_history_n_db)
        self.assertEqual(sharing_history_n_db.provider_id, provider.id)
        self.assertEqual(sharing_history_n_db.recipient_id, recipient.id)
        self.assertEqual(sharing_history_n_db.item_id, item.id)

    def test_insert_filling_history(self):
        db = next(override_get_db())
        user = insert_user(db, gen_username(), "user@example.com", gen_password())
        item = insert_item(
            db, user.id, "Item Name", "http://example.com", "item_type", "credentials"
        )
        filling_history = insert_filling_history(db, item.id)

        filling_history_n_db = (
            db.query(FillingHistory)
            .filter(FillingHistory.id == filling_history.id)
            .first()
        )

        self.assertIsNotNone(filling_history_n_db)
        self.assertEqual(filling_history_n_db.item_id, item.id)


if __name__ == "__main__":
    unittest.main()
