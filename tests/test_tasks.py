import unittest
from unittest.mock import patch
import pytest
from fastapi import HTTPException
from .conftest import client

class TestTasksSuccess:
    def setup_method(self):
        self.auth_header = {"authorization": "Bearer test-token"}
        self.mock_task_data = {
                    "title": "Complete project report",
                    "description": "Finalize the report for the Q3 project and submit it by the end of the week.",
                    "status": "pending",
                    "priority": 2,
                    "id": 3,
                    "owner_id": 1,
                    "created_at": "2025-05-02T15:19:21.351458"
                }
        self.mock_task_data_list = [self.mock_task_data]
        self.mock_user_id = 1

    def test_get_tasks(self):
        with patch('app.api.tasks.check_auth') as mock_check_auth, patch('app.api.tasks.get_task_list') as mock_get_task_list:
            mock_check_auth.return_value = self.mock_user_id
            mock_get_task_list.return_value = self.mock_task_data_list
            result = client.get("/tasks", headers={"authorization": "Bearer fake-token"})
            assert result.status_code == 200
            mock_get_task_list.assert_called_once()
            mock_check_auth.assert_called_once()

    def test_get_task(self):
        with patch('app.api.tasks.check_auth') as mock_check_auth, patch(
                'app.api.tasks.get_task_by_id') as mock_get_task_by_id:
            mock_check_auth.return_value = self.mock_user_id
            mock_get_task_by_id.return_value = self.mock_task_data

            client_response = client.get("/tasks/5", headers={"authorization": "Bearer fake-token"})

            assert client_response.status_code == 200
            data = client_response.json()
            assert data["id"] == 3
            assert data["title"] == "Complete project report"

            mock_check_auth.assert_called_once()
            mock_get_task_by_id.assert_called_once_with(1, 5)

    def test_search_task(self):
        with patch('app.api.tasks.check_auth') as mock_check_auth, patch('app.api.tasks.search_tasks') as mock_search_tasks:
            mock_check_auth.return_value = self.mock_user_id
            mock_search_tasks.return_value = self.mock_task_data_list
            result = client.get("/tasks/search/?q=Complete", headers={"authorization": "Bearer fake-token"})
            assert result.status_code == 200
            mock_search_tasks.assert_called_once()
            mock_check_auth.assert_called_once()

    def test_create_task(self):
        with patch('app.api.tasks.check_auth') as mock_check_auth, patch('app.api.tasks.create_new_task') as mock_create_new_task:
            mock_check_auth.return_value = self.mock_user_id
            mock_create_new_task.return_value = self.mock_task_data
            client_response = client.post("/tasks", headers={"authorization": "Bearer fake-token"}, json=self.mock_task_data)
            assert client_response.status_code == 201
            data = client_response.json()
            assert data == self.mock_task_data
            mock_check_auth.assert_called_once()
            mock_create_new_task.assert_called_once()

    def test_update_task(self):
        with patch('app.api.tasks.check_auth') as mock_check_auth, patch('app.api.tasks.update_task_by_id') as mock_update_task_by_id:
            mock_check_auth.return_value = self.mock_user_id
            mock_update_task_by_id.return_value = self.mock_task_data
            client_response = client.put("/tasks/3", headers={"authorization": "Bearer fake-token"}, json=self.mock_task_data)
            assert client_response.status_code == 200
            data = client_response.json()
            assert data == self.mock_task_data
            mock_check_auth.assert_called_once()
            mock_update_task_by_id.assert_called_once()


class TestTasksFailure:
    def setup_method(self):
        self.auth_header = {"authorization": "Bearer test-token"}
        self.mock_user_id = 1
        self.valid_payload = {
            "title": "Sample",
            "description": "Desc",
            "status": "pending",
            "priority": 1
        }

    def test_get_tasks_unauthorized(self):
        with patch('app.api.tasks.check_auth') as mock_check_auth, \
             patch('app.api.tasks.get_task_list') as mock_get_task_list:
            mock_check_auth.side_effect = HTTPException(status_code=401, detail="Unauthorized")
            result = client.get("/tasks", headers=self.auth_header)
            assert result.status_code == 401
            mock_get_task_list.assert_not_called()
            mock_check_auth.assert_called_once()

    def test_get_task_not_found(self):
        with patch('app.api.tasks.check_auth') as mock_check_auth, \
             patch('app.api.tasks.get_task_by_id') as mock_get_task_by_id:
            mock_check_auth.return_value = self.mock_user_id
            mock_get_task_by_id.side_effect = HTTPException(status_code=404, detail="Not Found")
            result = client.get("/tasks/999", headers=self.auth_header)
            assert result.status_code == 404
            mock_get_task_by_id.assert_called_once_with(self.mock_user_id, 999)
            mock_check_auth.assert_called_once()

    def test_search_task_no_query(self):
        # missing required q parameter
        result = client.get("/tasks/search/", headers=self.auth_header)
        assert result.status_code == 422

    def test_create_task_unauthorized(self):
        with patch('app.api.tasks.check_auth') as mock_check_auth, \
             patch('app.api.tasks.create_new_task') as mock_create:
            mock_check_auth.side_effect = HTTPException(status_code=401, detail="Unauthorized")
            result = client.post("/tasks", headers=self.auth_header, json=self.valid_payload)
            assert result.status_code == 401
            mock_create.assert_not_called()
            mock_check_auth.assert_called_once()

    def test_create_task_validation_error(self):
        # missing required field 'title'
        payload = {"description": "Desc only"}
        result = client.post("/tasks", headers=self.auth_header, json=payload)
        assert result.status_code == 422

    def test_update_task_not_found(self):
        with patch('app.api.tasks.check_auth') as mock_check_auth, \
             patch('app.api.tasks.update_task_by_id') as mock_update:
            mock_check_auth.return_value = self.mock_user_id
            mock_update.side_effect = HTTPException(status_code=404, detail="Not Found")
            result = client.put("/tasks/123", headers=self.auth_header, json=self.valid_payload)
            assert result.status_code == 404
            mock_update.assert_called_once_with(self.mock_user_id, 123, unittest.mock.ANY)
            mock_check_auth.assert_called_once()

    def test_update_task_unauthorized(self):
        with patch('app.api.tasks.check_auth') as mock_check_auth, \
             patch('app.api.tasks.update_task_by_id') as mock_update:
            mock_check_auth.side_effect = HTTPException(status_code=403, detail="Forbidden")
            result = client.put("/tasks/3", headers=self.auth_header, json=self.valid_payload)
            assert result.status_code == 403
            mock_update.assert_not_called()
            mock_check_auth.assert_called_once()
