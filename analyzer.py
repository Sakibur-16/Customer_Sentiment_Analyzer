"""
Core sentiment analysis module using OpenAI API.
"""

import openai
import json
from typing import List, Dict
from collections import Counter


class ReviewAnalyzer:
    """
    Analyzes customer reviews for sentiment and generates comprehensive reports.
    
    Attributes:
        client: OpenAI API client
        model: Model name to use for analysis
        temperature: Temperature setting for API calls
    """
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", temperature: float = 0.3):
        """
        Initialize the ReviewAnalyzer.
        
        Args:
            api_key: OpenAI API key
            model: Model to use for analysis
            temperature: Temperature for API responses (0.0-1.0)
        """
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
    
    def analyze_sentiment(self, review: str) -> Dict:
        """
        Analyze sentiment of a single review.
        
        Args:
            review: The review text to analyze
            
        Returns:
            Dictionary containing sentiment, score, key_points, and emotions
        """
        prompt = f"""Analyze the sentiment of this customer review. Provide your response in JSON format with:
- sentiment: "positive", "negative", or "neutral"
- score: a number from 1-5 (1=very negative, 5=very positive)
- key_points: list of main points mentioned
- emotions: list of emotions detected (e.g., satisfied, frustrated, excited)

Review: {review}

Respond with valid JSON only."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis expert. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            
            result = json.loads(response.choices[0].message.content)
            result['review'] = review
            return result
            
        except Exception as e:
            print(f"⚠ Error analyzing sentiment: {e}")
            return {
                "sentiment": "neutral",
                "score": 3,
                "key_points": [],
                "emotions": [],
                "review": review,
                "error": str(e)
            }
    
    def analyze_batch(self, reviews: List[str], verbose: bool = True) -> List[Dict]:
        """
        Analyze multiple reviews.
        
        Args:
            reviews: List of review texts
            verbose: Whether to print progress
            
        Returns:
            List of analysis results
        """
        results = []
        for i, review in enumerate(reviews, 1):
            if verbose:
                print(f"Analyzing review {i}/{len(reviews)}...")
            result = self.analyze_sentiment(review)
            results.append(result)
        return results
    
    def generate_summary(self, analysis_results: List[Dict]) -> str:
        """
        Generate an executive summary from analyzed reviews.
        
        Args:
            analysis_results: List of analysis result dictionaries
            
        Returns:
            Executive summary text
        """
        # Prepare data for summary
        sentiments = [r['sentiment'] for r in analysis_results]
        scores = [r['score'] for r in analysis_results]
        all_key_points = []
        all_emotions = []
        
        for r in analysis_results:
            all_key_points.extend(r.get('key_points', []))
            all_emotions.extend(r.get('emotions', []))
        
        summary_data = {
            "total_reviews": len(analysis_results),
            "sentiment_breakdown": dict(Counter(sentiments)),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "common_points": [item for item, count in Counter(all_key_points).most_common(10)],
            "common_emotions": [item for item, count in Counter(all_emotions).most_common(5)]
        }
        
        prompt = f"""Based on the following customer review analysis data, generate a concise executive summary:

Data:
{json.dumps(summary_data, indent=2)}

Sample reviews:
{json.dumps([r['review'][:200] + '...' if len(r['review']) > 200 else r['review'] for r in analysis_results[:5]], indent=2)}

Generate a professional summary that includes:
1. Overall sentiment overview
2. Key themes and patterns
3. Main customer concerns or praises
4. Actionable insights for business improvement

Keep it under 300 words."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a business analyst expert at summarizing customer feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating summary: {e}"
    
    def generate_report(self, analysis_results: List[Dict]) -> Dict:
        """
        Generate a complete analysis report.
        
        Args:
            analysis_results: List of analysis result dictionaries
            
        Returns:
            Complete report dictionary
        """
        sentiments = [r['sentiment'] for r in analysis_results]
        scores = [r['score'] for r in analysis_results]
        
        report = {
            "total_reviews": len(analysis_results),
            "sentiment_distribution": dict(Counter(sentiments)),
            "average_rating": round(sum(scores) / len(scores), 2) if scores else 0,
            "positive_percentage": round((sentiments.count('positive') / len(sentiments)) * 100, 1),
            "negative_percentage": round((sentiments.count('negative') / len(sentiments)) * 100, 1),
            "neutral_percentage": round((sentiments.count('neutral') / len(sentiments)) * 100, 1),
            "summary": self.generate_summary(analysis_results),
            "detailed_results": analysis_results
        }
        
        return report