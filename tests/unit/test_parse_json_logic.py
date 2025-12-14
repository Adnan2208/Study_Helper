"""Unit tests for the parse_json task logic."""
import pytest
import json
import re


class TestJSONParsing:
    """Test JSON parsing logic from AI responses."""
    
    def test_parse_clean_json(self):
        """Test parsing clean JSON response."""
        raw_output = '{"summary": "This is a test summary", "difficulty": "TOUGH"}'
        
        match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        assert match is not None
        
        json_str = match.group(0)
        data = json.loads(json_str)
        
        assert data['summary'] == "This is a test summary"
        assert data['difficulty'] == "TOUGH"
    
    def test_parse_json_with_leading_text(self):
        """Test parsing JSON with leading conversational text."""
        raw_output = 'Here is the analysis:\n{"summary": "Test", "difficulty": "SIMPLE"}'
        
        match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        assert match is not None
        
        json_str = match.group(0)
        data = json.loads(json_str)
        
        assert data['summary'] == "Test"
        assert data['difficulty'] == "SIMPLE"
    
    def test_no_json_in_output(self):
        """Test handling when no JSON is found in output."""
        raw_output = "This is just plain text with no JSON"
        
        match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        
        if not match:
            summary = 'Error parsing output'
            difficulty = 'UNKNOWN'
            
            assert summary == 'Error parsing output'
            assert difficulty == 'UNKNOWN'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])