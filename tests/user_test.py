import unittest
from unittest import TestCase

from repository.schemas.item import Item
from repository.schemas.user import User
from tests import (
    CredentialGenerator,
    insert_items,
    insert_user,
    override_get_db,
)


class UserTest(TestCase):
    def test_insert_user(self):
        db = next(override_get_db())
        password = CredentialGenerator.gen_password()
        name = CredentialGenerator.gen_username()
        email = f"{name}@example.com"
        u = insert_user(db, name, email, password)

        u_n_db = db.query(User).filter(User.id == u.id).first()

        self.assertIsNotNone(u_n_db is not None)
        self.assertIsNotNone(u_n_db.id is not None)
        self.assertEqual(u_n_db.name, u.name)
        self.assertEqual(u_n_db.email, u.email)
        self.assertEqual(u_n_db.password, u.password)
        self.assertIsNotNone(u_n_db.created_at)
        self.assertIsNone(u_n_db.updated_at)

    def test_insert_items(self):
        db = next(override_get_db())
        name = CredentialGenerator.gen_username()
        password = CredentialGenerator.gen_password()
        email = f"{name}@example.com"
        u = insert_user(db, name, email, password)
        item = insert_items(
            db,
            u.id,
            name="test_item_name",
            site="http://example.com",
            credentials="test_credentials",
        )
        item_n_db = db.query(Item).filter(Item.id == item.id).first()
        self.assertEqual(item_n_db.id, item.id)


if __name__ == "__main__":
    unittest.main()
