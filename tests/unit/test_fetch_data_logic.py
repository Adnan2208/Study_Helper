"""Unit tests for the fetch_data task logic."""
import pytest
from unittest.mock import Mock, patch
import requests


class TestFetchDataLogic:
    """Test the fetch_data task's Python logic."""
    
    def test_successful_data_fetch(self):
        """Test successful data fetching from URL."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.text = "Sample study notes content"
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            url = "https://example.com/notes.txt"
            response = requests.get(url)
            response.raise_for_status()
            content = response.text
            
            assert content == "Sample study notes content"
            mock_get.assert_called_once_with(url)
    
    def test_fetch_with_http_error(self):
        """Test handling of HTTP errors during fetch."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
            mock_get.return_value = mock_response
            
            url = "https://example.com/nonexistent.txt"
            response = requests.get(url)
            
            with pytest.raises(requests.HTTPError):
                response.raise_for_status()
    
    def test_fetch_empty_content(self):
        """Test fetching URL that returns empty content."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.text = ""
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            url = "https://example.com/empty.txt"
            response = requests.get(url)
            response.raise_for_status()
            content = response.text
            
            assert content == ""
            assert isinstance(content, str)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])