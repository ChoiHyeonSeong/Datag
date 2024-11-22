import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))

from services.project.project_service import ProjectService
from dto.project_dto import ProjectRequest

@pytest.mark.asyncio
async def test_create_project_service(test_maria_db, test_mongo_db):
    # ProjectService 인스턴스 생성
    project_service = ProjectService(test_maria_db, test_mongo_db)

    # 테스트 데이터 준비
    request_data = ProjectRequest(
        project_name="Test Project",
        project_model_task="cls",
        project_model_name="efficientnet_v2_s",
        description="This is a test project description.",
        accesscontrol={
            "view_users": ["user1", "user2"],
            "edit_users": ["user3", "user4"],
            "view_departments": ["dept1"],
            "edit_departments": ["dept2"]
        },
        is_private=True
    )

    # 프로젝트 생성 테스트 실행
    project_id = await project_service.create_project(creator_user_id=2, request=request_data)
    assert project_id is not None
    return project_id

@pytest.mark.asyncio
async def test_get_project_list_service(test_maria_db, test_mongo_db):
    project_service = ProjectService(test_maria_db, test_mongo_db)

    # 프로젝트 리스트 조회 테스트
    projects = await project_service.get_project_list(user_id=2, page=1, limit=5)
    assert projects is not None
    assert len(projects['data']) >= 0

@pytest.mark.asyncio
async def test_delete_project_service(test_maria_db, test_mongo_db):
    project_service = ProjectService(test_maria_db, test_mongo_db)

    # 프로젝트 생성 후 삭제 테스트
    request_data = ProjectRequest(
        project_name="Delete Test Project",
        project_model_task="cls",
        project_model_name="efficientnet_v2_s",
        description="This is a test project description.",
        accesscontrol={
            "view_users": ["user1"],
            "edit_users": ["user2"],
            "view_departments": ["dept1"],
            "edit_departments": ["dept2"]
        },
        is_private=False
    )
    project_id = await project_service.create_project(creator_user_id=2, request=request_data)
    assert project_id is not None

    # 삭제 실행
    await project_service.delete_project(project_id=project_id)
    assert True  # 예외가 발생하지 않으면 성공