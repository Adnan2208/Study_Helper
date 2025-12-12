"""
Test suite for validating the Kestra workflow YAML schema.
Tests the structure, required fields, and configuration of the workflow.
"""
import pytest
import yaml
from pathlib import Path


class TestWorkflowSchema:
    """Test the YAML workflow file structure and schema."""
    
    @pytest.fixture
    def workflow_data(self):
        """Load the workflow YAML file."""
        workflow_path = Path(__file__).parent.parent / "company.team.Study_Helper.yaml"
        with open(workflow_path, 'r') as f:
            return yaml.safe_load(f)
    
    def test_workflow_file_exists(self):
        """Test that the workflow YAML file exists."""
        workflow_path = Path(__file__).parent.parent / "company.team.Study_Helper.yaml"
        assert workflow_path.exists(), "Workflow YAML file should exist"
    
    def test_workflow_is_valid_yaml(self):
        """Test that the workflow file is valid YAML."""
        workflow_path = Path(__file__).parent.parent / "company.team.Study_Helper.yaml"
        try:
            with open(workflow_path, 'r') as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"Workflow YAML is invalid: {e}")
    
    def test_required_top_level_fields(self, workflow_data):
        """Test that required top-level fields are present."""
        assert 'id' in workflow_data
        assert 'namespace' in workflow_data
        assert 'inputs' in workflow_data
        assert 'tasks' in workflow_data
    
    def test_workflow_id(self, workflow_data):
        """Test that the workflow ID is correctly set."""
        assert workflow_data['id'] == 'Study_Helper'
    
    def test_workflow_namespace(self, workflow_data):
        """Test that the workflow namespace is correctly set."""
        assert workflow_data['namespace'] == 'company.team'
    
    def test_inputs_structure(self, workflow_data):
        """Test that inputs are properly defined."""
        inputs = workflow_data['inputs']
        assert isinstance(inputs, list)
        assert len(inputs) > 0
        
        input_ids = [inp['id'] for inp in inputs]
        assert 'drive_url' in input_ids
        assert 'huggingface_api_key' in input_ids
        assert 'serpapi_api_key' in input_ids
    
    def test_tasks_structure(self, workflow_data):
        """Test that tasks are properly structured."""
        tasks = workflow_data['tasks']
        assert isinstance(tasks, list)
        assert len(tasks) > 0
        
        for task in tasks:
            assert 'id' in task
            assert 'type' in task
    
    def test_expected_tasks_present(self, workflow_data):
        """Test that all expected tasks are present."""
        tasks = workflow_data['tasks']
        task_ids = [task['id'] for task in tasks]
        
        expected_tasks = ['fetch_data', 'ai_analysis', 'parse_json', 'check_difficulty', 'final_output']
        
        for expected_task in expected_tasks:
            assert expected_task in task_ids
    
    def test_conditional_task_structure(self, workflow_data):
        """Test that the conditional task is properly structured."""
        tasks = workflow_data['tasks']
        check_difficulty_task = next((task for task in tasks if task['id'] == 'check_difficulty'), None)
        
        assert check_difficulty_task is not None
        assert check_difficulty_task['type'] == 'io.kestra.plugin.core.flow.If'
        assert 'condition' in check_difficulty_task
        assert 'then' in check_difficulty_task
        assert 'TOUGH' in check_difficulty_task['condition']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])