from uuid import uuid4

import pytest

from tests.conftest import create_test_auth_headers_for_user
from core.models import PortalRole


async def test_get_user(client, create_user_in_database):

    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }

    await create_user_in_database(**user_data)

    resp = client.get(
        f"/api/v1/users/?email={user_data['email']}",
        headers=create_test_auth_headers_for_user(user_data["email"]),
    )

    assert resp.status_code == 200
