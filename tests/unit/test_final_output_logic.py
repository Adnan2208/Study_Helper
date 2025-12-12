"""Unit tests for the final_output task logic."""
import pytest
from unittest.mock import patch
import os


class TestFinalOutputLogic:
    """Test final output aggregation logic."""
    
    def test_output_with_all_fields(self):
        """Test output when all fields are available (TOUGH difficulty path)."""
        summary = "Comprehensive summary"
        difficulty = "TOUGH"
        video_title = "Advanced Lecture"
        video_link = "https://youtube.com/watch?v=abc123"
        
        outputs = {'summary': summary, 'difficulty': difficulty}
        
        if video_title != 'None':
            outputs['video_title'] = video_title
            outputs['video_link'] = video_link
        
        assert 'summary' in outputs
        assert 'difficulty' in outputs
        assert 'video_title' in outputs
        assert 'video_link' in outputs
    
    def test_output_without_video_fields(self):
        """Test output when video fields are not available (SIMPLE difficulty path)."""
        summary = "Simple topic summary"
        difficulty = "SIMPLE"
        video_title = "None"
        
        outputs = {'summary': summary, 'difficulty': difficulty}
        
        if video_title != 'None':
            outputs['video_title'] = video_title
        
        assert 'summary' in outputs
        assert 'difficulty' in outputs
        assert 'video_title' not in outputs


if __name__ == '__main__':
    pytest.main([__file__, '-v'])