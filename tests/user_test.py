from unittest import TestCase
from tests import override_get_db, insert_user, gen_password, gen_username
from util.crypto import PasswordContext
from repository.schemas.user import User, CryptoKey
from repository.schemas.session_info import SessionInfo
from sqlalchemy.orm import sessionmaker


class UserTest(TestCase):
    def test_insert_user(self):
        db = next(override_get_db())
        password = gen_password()
        username = gen_username()
        email = f"{username}@example.com"
        u = insert_user(db, username, email, password)

        u_n_db = db.query(User).filter(User.id == u.id).first()

        self.assertIsNotNone(u_n_db)
        self.assertIsNotNone(u_n_db.id)
        self.assertEqual(u_n_db.name, u.name)
        self.assertEqual(u_n_db.email, u.email)
        self.assertTrue(PasswordContext(password, u.email).verify(u_n_db.password))
        self.assertIsNotNone(u_n_db.created_at)
        self.assertIsNone(u_n_db.updated_at)

    def test_insert_crypto_key(self):
        db = next(override_get_db())
        password = gen_password()
        username = gen_username()
        email = f"{username}@example.com"
        u = insert_user(db, username, email, password)

        
        private_key = "private_key_example"
        public_key = "public_key_example"
        salt = "salt_example"
        crypto_key = CryptoKey(
            private_key=private_key, public_key=public_key, salt=salt, user_id=u.id
        )
        db.add(crypto_key)
        db.commit()

        crypto_key_n_db = db.query(CryptoKey).filter(CryptoKey.user_id == u.id).first()

        self.assertIsNotNone(crypto_key_n_db)
        self.assertEqual(crypto_key_n_db.private_key, private_key)
        self.assertEqual(crypto_key_n_db.public_key, public_key)
        self.assertEqual(crypto_key_n_db.salt, salt)
        self.assertEqual(crypto_key_n_db.user_id, u.id)

    def test_insert_session_info(self):
        db = next(override_get_db())
        password = gen_password()
        username = gen_username()
        email = f"{username}@example.com"
        u = insert_user(db, username, email, password)

        # Assuming insert_session_info is a function that inserts a SessionInfo
        session_info = SessionInfo(
            location="New York",
            ip="192.168.0.1",
            status="ACTIVE",
            user_agent="Mozilla/5.0",
            device_fk="device_id_example",
            user_id=u.id,
        )
        db.add(session_info)
        db.commit()

        session_info_n_db = (
            db.query(SessionInfo).filter(SessionInfo.user_id == u.id).first()
        )

        self.assertIsNotNone(session_info_n_db)
        self.assertEqual(session_info_n_db.location, "New York")
        self.assertEqual(session_info_n_db.ip, "192.168.0.1")
        self.assertEqual(session_info_n_db.status, "ACTIVE")
        self.assertEqual(session_info_n_db.user_agent, "Mozilla/5.0")
        self.assertEqual(session_info_n_db.device_fk, "device_id_example")
        self.assertEqual(session_info_n_db.user_id, u.id)


if __name__ == "__main__":
    unittest.main()
