"""Integration tests for the complete Study Helper workflow."""
import pytest
from unittest.mock import Mock, patch
import json
import re
import requests


class TestWorkflowToughPath:
    """Test complete workflow for TOUGH difficulty path."""
    
    @patch('requests.get')
    @patch('requests.post')
    def test_complete_tough_workflow(self, mock_post, mock_get):
        """Test complete workflow when content is classified as TOUGH."""
        # Mock fetch_data
        fetch_response = Mock()
        fetch_response.text = "Advanced quantum computing principles"
        fetch_response.raise_for_status = Mock()
        
        # Mock ai_analysis
        ai_response = Mock()
        ai_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"summary": "Quantum computing uses quantum mechanics", "difficulty": "TOUGH"}'
                }
            }]
        }
        ai_response.raise_for_status = Mock()
        
        # Mock search_youtube
        youtube_response = Mock()
        youtube_response.json.return_value = {
            "video_results": [{
                "title": "Introduction to Quantum Computing",
                "link": "https://youtube.com/watch?v=quantum123"
            }]
        }
        youtube_response.raise_for_status = Mock()
        
        mock_get.side_effect = [fetch_response, youtube_response]
        mock_post.return_value = ai_response
        
        # Execute workflow steps
        response = mock_get("https://example.com/notes.txt")
        response.raise_for_status()
        content = response.text
        
        ai_result = mock_post("https://router.huggingface.co/v1/chat/completions")
        ai_result.raise_for_status()
        ai_data = ai_result.json()
        generated_text = ai_data["choices"][0]["message"]["content"]
        
        match = re.search(r'\{.*\}', generated_text, re.DOTALL)
        json_str = match.group(0)
        parsed_data = json.loads(json_str)
        
        assert parsed_data['difficulty'] == 'TOUGH'


class TestWorkflowSimplePath:
    """Test complete workflow for SIMPLE difficulty path."""
    
    @patch('requests.get')
    @patch('requests.post')
    def test_complete_simple_workflow(self, mock_post, mock_get):
        """Test complete workflow when content is classified as SIMPLE."""
        fetch_response = Mock()
        fetch_response.text = "Basic Python introduction"
        fetch_response.raise_for_status = Mock()
        
        ai_response = Mock()
        ai_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"summary": "Python basics", "difficulty": "SIMPLE"}'
                }
            }]
        }
        ai_response.raise_for_status = Mock()
        
        mock_get.return_value = fetch_response
        mock_post.return_value = ai_response
        
        response = mock_get("https://example.com/notes.txt")
        response.raise_for_status()
        
        ai_result = mock_post("https://router.huggingface.co/v1/chat/completions")
        ai_result.raise_for_status()
        ai_data = ai_result.json()
        generated_text = ai_data["choices"][0]["message"]["content"]
        
        match = re.search(r'\{.*\}', generated_text, re.DOTALL)
        json_str = match.group(0)
        parsed_data = json.loads(json_str)
        
        assert parsed_data['difficulty'] == 'SIMPLE'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])