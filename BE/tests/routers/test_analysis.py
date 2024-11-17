import pytest

# 수동 차원축소 테스트
@pytest.mark.asyncio
async def test_dimension_reduction_manual(async_client, auth_headers):
    request_data = {
        "project_id": "67330084d4c23c34e7550e66",
        "is_private": True,
        "history_name": "Manual Test",
        "algorithm": "tsne",
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
        ],
        "selected_tags": []
    }
    response = await async_client.post(
        "/be/api/project/analysis/manual",
        json=request_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == 200

# 자동 차원축소 테스트
@pytest.mark.asyncio
async def test_dimension_reduction_auto(async_client, auth_headers):
    request_data = {
        "project_id": "67330084d4c23c34e7550e66",
        "is_private": False,
        "history_name": "Auto Test",
        "algorithm": "umap",
        "selected_tags": []
    }
    response = await async_client.post(
        "/be/api/project/analysis/auto",
        json=request_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == 200

# 권한이 없는 사용자에 대한 테스트
@pytest.mark.asyncio
async def test_dimension_reduction_permission_denied(async_client, auth_headers):
    request_data = {
        "project_id": "67330084d4c23c34e7550e66",
        "is_private": True,
        "history_name": "Permission Denied Test",
        "algorithm": "tsne",
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
        ],
        "selected_tags": []
    }
    response = await async_client.post(
        "/be/api/project/analysis/manual",
        json=request_data,
        headers=auth_headers
    )
    assert response.status_code == 403  # Permission Denied
