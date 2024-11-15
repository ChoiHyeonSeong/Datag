from fastapi import HTTPException
from httpx import AsyncClient
from unittest.mock import patch
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))

from app.main import app


@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="module")
async def auth_headers(async_client):
    login_data = {
        "email": "test1@tmail.ws",  
        "password": "1234"
    }
    response = await async_client.post("be/api/auth/login", json=login_data)
    assert response.status_code == 200 
    token = response.json()["data"].get("access_token")
    assert token is not None, "토큰이 반환되지 않았습니다."
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_get_dimension_reduction_manual(async_client, auth_headers):
    data = {
    "algorithm": "umap",
    "project_id": "67330de9c6e5eb128e8a0600",
    "history_name": "history_tset_manual",
    "is_private": False,
    "selected_tags": [
        {
            "and_condition": [
            ],
            "not_condition": [
            ],
            "or_condition": [
            ]
        }
    ],
    "image_ids": [
        "67330e5135cedc092c5471c2",
        "67330e6635cedc092c547216",
        "67330e4d35cedc092c5471b2",
        "67330e6435cedc092c54720e",
        "67330e6535cedc092c547212",
        "67330e5d35cedc092c5471f2",
        "67330e5a35cedc092c5471e6",
        "67330e5e35cedc092c5471f6",
        "67330e5935cedc092c5471e2",
        "67330e5335cedc092c5471ca",
        "67330e6335cedc092c54720a",
        "67330e6835cedc092c54721e",
        "67330e5535cedc092c5471d2",
        "67330e6a35cedc092c547226",
        "67330e4c35cedc092c5471ae",
        "67330e5835cedc092c5471de",
        "67330e6135cedc092c547202",
        "67330e6035cedc092c5471fe",
        "67330e6235cedc092c547206",
        "67330e6935cedc092c547222",
        "67330e6735cedc092c54721a"
    ]
    }

    response = await async_client.post(
        "/be/api/project/analysis/manual",
        json = data,
        headers=auth_headers
    )

    print(response.json())

    assert response.status_code == 200



@pytest.mark.asyncio
async def test_get_dimension_reduction_auto(async_client, auth_headers):
    data = {
        "algorithm": "tsne",
        "project_id": "67330de9c6e5eb128e8a0600",
        "history_name": "history_tset_auto",
        "is_private": 1,
        "selected_tags": [
            {
                "and_condition": [
                ],
                "not_condition": [
                ],
                "or_condition": [
                ]
            }
        ]
    }
    response = await async_client.post(
    "/be/api/project/analysis/auto",
    json = data,
    headers=auth_headers
    )

    assert response.status_code == 200
    
