# Customer Sentiment Analyzer 🎯

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5%20%7C%20GPT--4-412991.svg)](https://openai.com/)

> **AI-Powered Customer Review Sentiment Analysis System**  
> Analyze customer reviews, extract insights, and generate comprehensive reports using OpenAI's GPT models.

![Demo](https://via.placeholder.com/800x400/1a1a2e/ffffff?text=Customer+Sentiment+Analyzer+Demo)

---

## ✨ Features

- 🤖 **AI-Powered Analysis**: Leverages OpenAI GPT models for accurate sentiment detection
- 📊 **Comprehensive Reports**: Generates detailed analysis with:
  - Sentiment classification (Positive, Negative, Neutral)
  - Rating scores (1-5 scale)
  - Key points extraction
  - Emotion detection
  - Executive summary with actionable insights
- 📁 **Multiple Input Methods**: 
  - 🖱️ GUI file browser for easy file selection
  - 📄 Load from JSON/TXT files
  - 📋 Copy-paste multiple reviews
  - ⌨️ Manual entry one-by-one
  - 🧪 Sample data for testing
- 💾 **Export Capabilities**: Save reports in JSON format
- 🎨 **Beautiful Console Output**: Formatted, emoji-enhanced terminal display
- 🔒 **Secure Configuration**: Environment-based API key management

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** ([Download here](https://www.python.org/downloads/))
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Customer_Sentiment_Analyzer.git
cd Customer_Sentiment_Analyzer

# 2. Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Unix/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-api-key-here

# 5. Run the application
python main.py
```

---

## 📖 Usage

### Command Line Interface

```bash
python main.py
```

Follow the interactive prompts:

1. **Choose Input Method** (1-4):
   - Option 1: Use sample reviews for testing
   - Option 2: Load from file (with GUI browser or manual path)
   - Option 3: Enter reviews manually
   - Option 4: Paste multiple reviews at once

2. **View Analysis Results**: 
   - Sentiment distribution
   - Average ratings
   - Executive summary
   - Detailed review breakdown

3. **Export Report** (Optional):
   - Save as JSON for further analysis

### Programmatic Usage

```python
from src.analyzer import ReviewAnalyzer
from src.config import Config

# Initialize
config = Config()
analyzer = ReviewAnalyzer(config.openai_api_key)

# Analyze reviews
reviews = [
    "Amazing product! Exceeded expectations.",
    "Terrible quality. Very disappointed.",
    "It's okay, nothing special."
]

# Get results
results = analyzer.analyze_batch(reviews)
report = analyzer.generate_report(results)

# Access data
print(f"Average Rating: {report['average_rating']}/5.0")
print(f"Positive: {report['positive_percentage']}%")
print(f"\nSummary:\n{report['summary']}")
```

---

## 📁 Input Formats

### JSON File Format

**Option 1: Simple Array**
```json
[
  "Review text 1",
  "Review text 2",
  "Review text 3"
]
```

**Option 2: Object with Reviews Key**
```json
{
  "reviews": [
    "Review text 1",
    "Review text 2",
    "Review text 3"
  ]
}
```

### Text File Format

```text
Review text 1
Review text 2
Review text 3
```

### Paste Format

Supports multiple separators:
- **Double newline** (paragraph separation)
- **Dash separator** (`---`)
- **Asterisk separator** (`***`)
- **Numbered** (`Review 1:`, `Review 2:`)
- **Line-by-line** (one review per line)

---

## 📊 Output Example

```
============================================================
CUSTOMER REVIEW ANALYSIS REPORT
============================================================

Total Reviews Analyzed: 8
Average Rating: 3.6/5.0

📊 Sentiment Distribution:
  ✅ Positive: 4 (50.0%)
  ❌ Negative: 2 (25.0%)
  ➖ Neutral: 2 (25.0%)

------------------------------------------------------------
📝 EXECUTIVE SUMMARY
------------------------------------------------------------
The overall sentiment is moderately positive with an average
rating of 3.6/5. Customers particularly appreciate the quality
and customer service. Main concerns include pricing and
delivery times. Key recommendation: Focus on improving
logistics while maintaining product quality standards.

------------------------------------------------------------
🔍 DETAILED REVIEW ANALYSIS
------------------------------------------------------------

[Review 1]
✅ Sentiment: POSITIVE | Score: 5/5
📄 Text: Amazing product! Exceeded expectations...
🔑 Key Points: quality, delivery, reliability
💭 Emotions: satisfied, excited, happy
```

---

## 🔧 Configuration

Create a `.env` file in the project root:

```env
# Required
OPENAI_API_KEY=sk-your-api-key-here

# Optional
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.3
MAX_TOKENS=1000
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | (required) | Your OpenAI API key |
| `MODEL_NAME` | `gpt-3.5-turbo` | Model to use (gpt-3.5-turbo or gpt-4) |
| `TEMPERATURE` | `0.3` | Response randomness (0.0-1.0) |
| `MAX_TOKENS` | `1000` | Maximum tokens per request |

---

## 📂 Project Structure

```
Customer_Sentiment_Analyzer/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .env                         # Your configuration (create this)
├── README.md                    # This file
│
├── src/                         # Source code
│   ├── __init__.py
│   ├── analyzer.py              # Core sentiment analysis
│   ├── config.py                # Configuration management
│   └── utils/                   # Utility modules
│       ├── __init__.py
│       ├── file_handler.py      # File I/O operations
│       ├── display.py           # Console output formatting
│       └── input_handler.py     # User input processing
│
├── data/                        # Sample data (optional)
│   ├── sample_reviews.json
│   └── sample_reviews.txt
│
├── outputs/                     # Generated reports
│   └── analysis_report.json
│
└── tests/                       # Unit tests
    ├── __init__.py
    └── test_analyzer.py
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_analyzer.py -v
```

---

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Format code
black src/ tests/

# Run linter
flake8 src/ tests/
```

### Adding New Features

1. Create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make changes and add tests

3. Run tests
   ```bash
   pytest
   ```

4. Commit and push
   ```bash
   git add .
   git commit -m "Add: your feature description"
   git push origin feature/your-feature-name
   ```

5. Create a Pull Request

---

## 📝 Examples

### Example 1: Analyze Product Reviews

```bash
python main.py
# Choose option 2 (Load from file)
# Select your reviews.json file
# View comprehensive analysis
```

### Example 2: Quick Test with Samples

```bash
python main.py
# Choose option 1 (Sample reviews)
# Instantly see how the system works
```

### Example 3: Batch Processing

```python
from src.analyzer import ReviewAnalyzer
from src.config import Config

config = Config()
analyzer = ReviewAnalyzer(config.openai_api_key)

# Load your reviews
with open('data/reviews.json', 'r') as f:
    reviews = json.load(f)

# Analyze
results = analyzer.analyze_batch(reviews)
report = analyzer.generate_report(results)

# Save
with open('outputs/report.json', 'w') as f:
    json.dump(report, f, indent=2)
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError: No module named 'src'`**
```bash
# Solution: Ensure __init__.py files exist
New-Item -Path "src\__init__.py" -ItemType File -Force
New-Item -Path "src\utils\__init__.py" -ItemType File -Force
```

**Issue: `API Key Not Found`**
```bash
# Solution: Check .env file
# 1. Ensure .env exists in project root
# 2. Verify it contains: OPENAI_API_KEY=sk-...
# 3. No spaces around the = sign
```

**Issue: `Rate limit exceeded`**
```bash
# Solution: 
# - Wait a few seconds between requests
# - Check your OpenAI account usage/limits
# - Consider upgrading your OpenAI plan
```

**Issue: Import errors in VS Code**
```bash
# Solution: Add to .vscode/settings.json
{
    "python.analysis.extraPaths": ["${workspaceFolder}/src"]
}
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** your feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

Please ensure:
- Code follows PEP 8 style guide
- All tests pass
- New features include tests
- Documentation is updated

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 👤 Author

**Your Name**
- GitHub: [@Sakibur-16](https://github.com/yourusername)

- Email: sakibursrrahman@gmail.com
---

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for providing the GPT API
- [Python](https://www.python.org/) community for excellent libraries
- All contributors who help improve this project

---

## 🗺️ Roadmap

- [ ] Add support for multiple languages
- [ ] Implement sentiment trend analysis over time
- [ ] Add visualization dashboard (web interface)
- [ ] Support for analyzing reviews from APIs (Amazon, Yelp, etc.)
- [ ] Batch processing for large datasets
- [ ] Export to CSV/Excel formats
- [ ] Integration with popular e-commerce platforms
- [ ] Real-time streaming analysis

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/Customer_Sentiment_Analyzer&type=Date)](https://star-history.com/#yourusername/Customer_Sentiment_Analyzer&Date)

---

## 📊 Stats

![GitHub repo size](https://img.shields.io/github/repo-size/yourusername/Customer_Sentiment_Analyzer)
![GitHub contributors](https://img.shields.io/github/contributors/yourusername/Customer_Sentiment_Analyzer)
![GitHub stars](https://img.shields.io/github/stars/yourusername/Customer_Sentiment_Analyzer?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/Customer_Sentiment_Analyzer?style=social)

---

<div align="center">

**Made with ❤️ and ☕ by developers, for developers**

[⬆ Back to Top](#customer-sentiment-analyzer-)

</div>