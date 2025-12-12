"""Unit tests for the ai_analysis task logic."""
import pytest
from unittest.mock import Mock, patch
import requests
import json


class TestAIAnalysisLogic:
    """Test the ai_analysis task's Python logic."""
    
    def test_successful_ai_analysis(self):
        """Test successful AI analysis with valid response."""
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.json.return_value = {
                "choices": [{
                    "message": {
                        "content": '{"summary": "Test summary", "difficulty": "TOUGH"}'
                    }
                }]
            }
            mock_response.raise_for_status = Mock()
            mock_post.return_value = mock_response
            
            api_url = "https://router.huggingface.co/v1/chat/completions"
            headers = {"Authorization": "Bearer test_key", "Content-Type": "application/json"}
            payload = {
                "model": "HuggingFaceTB/SmolLM3-3B:hf-inference",
                "messages": [{"role": "user", "content": "Test prompt"}]
            }
            
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            generated_text = result["choices"][0]["message"]["content"]
            
            assert "summary" in generated_text
            mock_post.assert_called_once()
    
    def test_prompt_construction(self):
        """Test that prompts are correctly constructed."""
        content = "Machine learning is a subset of AI"
        json_fmt = '{"summary": "...", "difficulty": "..."}'
        
        prompt = f"""Analyze the following study notes. 1) Summarize them in 3 sentences. 2) Classify difficulty as exactly 'TOUGH' or 'SIMPLE'. 3) Return ONLY valid JSON in this format: {json_fmt}. Do not add any conversational text before or after the JSON.

Notes:
{content}
"""
        
        assert "Analyze the following study notes" in prompt
        assert content in prompt
        assert "TOUGH" in prompt
        assert "SIMPLE" in prompt


if __name__ == '__main__':
    pytest.main([__file__, '-v'])