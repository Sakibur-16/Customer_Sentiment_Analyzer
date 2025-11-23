"""
Unit tests for ReviewAnalyzer class.
"""

import pytest
from unittest.mock import Mock, patch
from src.analyzer import ReviewAnalyzer


@pytest.fixture
def mock_api_key():
    """Provide a mock API key for testing."""
    return "sk-test-key-12345"


@pytest.fixture
def analyzer(mock_api_key):
    """Create a ReviewAnalyzer instance with mocked API."""
    with patch('openai.OpenAI'):
        return ReviewAnalyzer(api_key=mock_api_key)


def test_analyzer_initialization(mock_api_key):
    """Test analyzer initializes correctly."""
    with patch('openai.OpenAI'):
        analyzer = ReviewAnalyzer(api_key=mock_api_key)
        assert analyzer.model == "gpt-3.5-turbo"
        assert analyzer.temperature == 0.3


def test_analyzer_custom_settings(mock_api_key):
    """Test analyzer accepts custom settings."""
    with patch('openai.OpenAI'):
        analyzer = ReviewAnalyzer(
            api_key=mock_api_key,
            model="gpt-4",
            temperature=0.5
        )
        assert analyzer.model == "gpt-4"
        assert analyzer.temperature == 0.5


def test_analyze_sentiment_error_handling(analyzer):
    """Test sentiment analysis handles errors gracefully."""
    result = analyzer.analyze_sentiment("Test review")
    
    # Should return default values on error
    assert 'sentiment' in result
    assert 'score' in result
    assert 'review' in result
    assert result['review'] == "Test review"


def test_analyze_batch(analyzer):
    """Test batch analysis."""
    reviews = ["Good product", "Bad quality", "Average"]
    results = analyzer.analyze_batch(reviews, verbose=False)
    
    assert len(results) == 3
    assert all('sentiment' in r for r in results)
    assert all('score' in r for r in results)


def test_generate_report_structure(analyzer):
    """Test report generation has correct structure."""
    mock_results = [
        {
            'sentiment': 'positive',
            'score': 5,
            'review': 'Great!',
            'key_points': ['quality'],
            'emotions': ['happy']
        },
        {
            'sentiment': 'negative',
            'score': 2,
            'review': 'Bad',
            'key_points': ['poor quality'],
            'emotions': ['frustrated']
        }
    ]
    
    with patch.object(analyzer, 'generate_summary', return_value="Test summary"):
        report = analyzer.generate_report(mock_results)
    
    assert 'total_reviews' in report
    assert report['total_reviews'] == 2
    assert 'sentiment_distribution' in report
    assert 'average_rating' in report
    assert 'positive_percentage' in report
    assert 'negative_percentage' in report
    assert 'summary' in report
    assert 'detailed_results' in report


def test_sentiment_percentages(analyzer):
    """Test sentiment percentage calculations."""
    mock_results = [
        {'sentiment': 'positive', 'score': 5, 'review': 'Great!'},
        {'sentiment': 'positive', 'score': 4, 'review': 'Good'},
        {'sentiment': 'negative', 'score': 2, 'review': 'Bad'},
        {'sentiment': 'neutral', 'score': 3, 'review': 'OK'}
    ]
    
    with patch.object(analyzer, 'generate_summary', return_value="Test"):
        report = analyzer.generate_report(mock_results)
    
    assert report['positive_percentage'] == 50.0
    assert report['negative_percentage'] == 25.0
    assert report['neutral_percentage'] == 25.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])