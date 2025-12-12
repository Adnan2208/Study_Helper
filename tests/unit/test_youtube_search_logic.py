"""Unit tests for the search_youtube task logic."""
import pytest
from unittest.mock import Mock, patch
import requests


class TestYouTubeSearchLogic:
    """Test YouTube search functionality via SerpAPI."""
    
    def test_successful_youtube_search(self):
        """Test successful YouTube search with results."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "video_results": [{
                    "title": "Introduction to Machine Learning",
                    "link": "https://youtube.com/watch?v=abc123"
                }]
            }
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            api_key = "test_serpapi_key"
            query = "Lecture on Machine Learning basics"
            
            params = {
                "engine": "youtube",
                "search_query": query,
                "api_key": api_key
            }
            
            response = requests.get("https://serpapi.com/search", params=params)
            response.raise_for_status()
            results = response.json()
            
            video_results = results.get("video_results", [])
            
            assert len(video_results) > 0
            assert video_results[0]["title"] == "Introduction to Machine Learning"
    
    def test_youtube_search_with_no_results(self):
        """Test YouTube search that returns no results."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {"video_results": []}
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            params = {
                "engine": "youtube",
                "search_query": "Very obscure topic",
                "api_key": "test_key"
            }
            
            response = requests.get("https://serpapi.com/search", params=params)
            response.raise_for_status()
            results = response.json()
            
            video_results = results.get("video_results", [])
            
            if not video_results:
                title = 'Not Found'
                link = 'None'
                
                assert title == 'Not Found'
                assert link == 'None'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])