import requests
import pytest
from jsonschema import validate, ValidationError
from schemas.activities_schema import ACTIVITIES_LIST_SCHEMA, ACTIVITY_SCHEMA
import time

class TestActivities:
    @pytest.fixture(autouse=True)
    def setup(self, api_base_url):
        self.base_url = api_base_url
        self.activities_list_schema = ACTIVITIES_LIST_SCHEMA
        self.activity_schema = ACTIVITY_SCHEMA

    def test_get_activities(self):
        """Test GET /api/v1/Activities with JSON schema validation"""
        url = f"{self.base_url}/api/v1/Activities"
        headers = {
            'accept': 'text/plain; v=1.0'
        }
        response = requests.get(url, headers=headers)
        print(response.text)
        
        # Status code assertion
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Response time assertion (should be less than 5 seconds)
        assert response.elapsed.total_seconds() < 5, "Response time exceeded 5 seconds"
        
        # Content-Type header assertion
        assert 'application/json' in response.headers.get('Content-Type', ''), \
            f"Expected JSON content type, got {response.headers.get('Content-Type')}"
        
        # Parse JSON response
        activities = response.json()
        
        # Assert response is a list
        assert isinstance(activities, list), "Response should be a list"
        
        # Assert list is not empty
        assert len(activities) > 0, "Activities list should not be empty"
        
        # Validate JSON schema
        try:
            validate(instance=activities, schema=self.activities_list_schema)
            print("✓ JSON schema validation passed for activities list")
        except ValidationError as e:
            pytest.fail(f"JSON schema validation failed: {e.message}")
        
        # Validate each activity object in the list
        for idx, activity in enumerate(activities):
            try:
                validate(instance=activity, schema=self.activity_schema)
                print(f"✓ Activity {idx + 1} schema validation passed")
            except ValidationError as e:
                pytest.fail(f"Activity {idx + 1} schema validation failed: {e.message}")
            
            # Additional field validations
            assert activity.get('title'), f"Activity {idx + 1} missing or empty title"
            assert activity.get('id'), f"Activity {idx + 1} missing or empty id"
            assert isinstance(activity.get('title'), str), f"Activity {idx + 1} title should be a string"
    
    
    def test_get_activities_data_integrity(self):
        """Test data integrity and consistency in activities response"""
        url = f"{self.base_url}/api/v1/Activities"
        headers = {
            'accept': 'text/plain; v=1.0'
        }
        response = requests.get(url, headers=headers)
        
        assert response.status_code == 200
        activities = response.json()
        
        # Check for duplicate IDs
        ids = [activity.get('id') for activity in activities]
        assert len(ids) == len(set(ids)), "Duplicate activity IDs found"
        
        # Validate timestamps if present
        for idx, activity in enumerate(activities):
            if 'createdAt' in activity:
                created_at = activity.get('createdAt')
                assert created_at, f"Activity {idx + 1} has empty createdAt"
            
            # If updatedAt exists, it should be >= createdAt (if timestamps are comparable)
            if 'updatedAt' in activity and activity.get('updatedAt'):
                assert activity.get('updatedAt'), f"Activity {idx + 1} has empty updatedAt"
        
