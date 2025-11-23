"""
Customer Review Sentiment Analyzer - Main Entry Point

A professional sentiment analysis system for customer reviews using OpenAI's GPT models.
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import analyzer module robustly: try direct import, otherwise load by file path or fall back to importlib
try:
    from src.analyzer import ReviewAnalyzer
except Exception:
    # Fallback: try loading the analyzer module directly from src/analyzer.py by file path
    project_root = os.path.dirname(os.path.abspath(__file__))
    analyzer_path = os.path.join(project_root, "src", "analyzer.py")
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("src.analyzer", analyzer_path)
        analyzer_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(analyzer_module)
        ReviewAnalyzer = analyzer_module.ReviewAnalyzer
    except Exception:
        # Final fallback: try standard import (covers environments where src is a proper package)
        import importlib
        analyzer_module = importlib.import_module("src.analyzer")
        ReviewAnalyzer = analyzer_module.ReviewAnalyzer
from src.config import Config
from src.utils.file_handler import (
    browse_file,
    load_reviews_from_file,
    save_report_to_file,
    get_sample_reviews
)
from src.utils.display import (
    print_header,
    print_section,
    display_menu,
    display_report,
    print_success,
    print_error,
    print_warning
)
from src.utils.input_handler import (
    get_multiline_input,
    parse_pasted_reviews,
    get_manual_reviews,
    confirm_action
)


def main():
    """Main application entry point."""
    
    # Print welcome banner
    print_header("CUSTOMER REVIEW SENTIMENT ANALYZER", 60)
    print("\n💡 AI-Powered Review Analysis using OpenAI GPT")
    print("📊 Generate comprehensive sentiment reports with actionable insights\n")
    
    # Load configuration
    try:
        config = Config()
        print_success("Configuration loaded successfully")
    except ValueError as e:
        print_error(str(e))
        print("\n📝 Setup Instructions:")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenAI API key: OPENAI_API_KEY=sk-your-key-here")
        print("3. Run the application again")
        return 1
    
    # Initialize analyzer
    try:
        print_success("Initializing analyzer...")
        analyzer = ReviewAnalyzer(
            api_key=config.openai_api_key,
            model=config.model_name,
            temperature=config.temperature
        )
        print_success(f"Connected to OpenAI API (Model: {config.model_name})")
    except Exception as e:
        print_error(f"Failed to initialize analyzer: {e}")
        return 1
    
    # Input method selection
    display_menu(
        "CHOOSE INPUT METHOD",
        [
            "Use sample reviews (for testing)",
            "Load reviews from file (JSON or TXT)",
            "Enter reviews manually (one by one)",
            "Paste reviews (copy-paste multiple reviews at once)"
        ]
    )
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Goodbye!")
        return 0
    
    reviews = []
    
    # Process based on choice
    if choice == '1':
        # Sample reviews
        reviews = get_sample_reviews()
        print_success(f"Using {len(reviews)} sample reviews")
    
    elif choice == '2':
        # Load from file
        print("\nFile input options:")
        print("  a. Browse with file dialog (GUI)")
        print("  b. Type filename manually")
        
        try:
            file_choice = input("\nEnter choice (a/b): ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n")
            file_choice = 'b'
        
        if file_choice == 'a':
            print_success("Opening file browser...")
            filename = browse_file()
            if not filename:
                print_warning("No file selected. Using sample reviews.")
                reviews = get_sample_reviews()
            else:
                print(f"📂 Selected: {filename}")
                reviews = load_reviews_from_file(filename)
                if not reviews:
                    print_warning("No reviews loaded. Using sample reviews.")
                    reviews = get_sample_reviews()
                else:
                    print_success(f"Loaded {len(reviews)} reviews")
        else:
            filename = input("Enter filename (e.g., data/reviews.txt): ").strip()
            reviews = load_reviews_from_file(filename)
            if not reviews:
                print_warning("No reviews loaded. Using sample reviews.")
                reviews = get_sample_reviews()
            else:
                print_success(f"Loaded {len(reviews)} reviews")
    
    elif choice == '3':
        # Manual entry
        reviews = get_manual_reviews()
        if not reviews:
            print_warning("No reviews entered. Using sample reviews.")
            reviews = get_sample_reviews()
        else:
            print_success(f"Collected {len(reviews)} reviews")
    
    elif choice == '4':
        # Paste reviews
        pasted_text = get_multiline_input()
        reviews = parse_pasted_reviews(pasted_text)
        
        if not reviews:
            print_warning("No reviews detected. Using sample reviews.")
            reviews = get_sample_reviews()
        else:
            print_success(f"Parsed {len(reviews)} reviews from pasted content")
            print("\n📋 Detected reviews:")
            for i, rev in enumerate(reviews[:5], 1):  # Show first 5
                preview = rev[:80] + "..." if len(rev) > 80 else rev
                print(f"  {i}. {preview}")
            if len(reviews) > 5:
                print(f"  ... and {len(reviews) - 5} more")
            
            if not confirm_action("\nProceed with these reviews?"):
                print("Using sample reviews instead.")
                reviews = get_sample_reviews()
    
    else:
        print_warning("Invalid choice. Using sample reviews.")
        reviews = get_sample_reviews()
    
    # Analyze reviews
    print_header("STARTING ANALYSIS")
    print(f"📊 Analyzing {len(reviews)} reviews...\n")
    
    try:
        results = analyzer.analyze_batch(reviews, verbose=True)
        
        # Generate comprehensive report
        print("\n📝 Generating comprehensive report...")
        report = analyzer.generate_report(results)
        
        # Display report
        display_report(report)
        
        # Save report option
        print("\n")
        if confirm_action("Would you like to save the report?"):
            filename = input("Enter filename (default: analysis_report.json): ").strip()
            if not filename:
                filename = "analysis_report.json"
            
            if save_report_to_file(report, filename):
                print_success("Report saved successfully!")
        
        print_header("ANALYSIS COMPLETE!")
        print("\n✨ Thank you for using Customer Review Sentiment Analyzer!")
        print("⭐ Star us on GitHub if you found this helpful!\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠ Analysis interrupted by user")
        return 1
    except Exception as e:
        print_error(f"Error during analysis: {e}")
        print("\n🔍 Troubleshooting:")
        print("- Check your internet connection")
        print("- Verify your OpenAI API key is valid")
        print("- Ensure you have sufficient API credits")
        return 1


if __name__ == "__main__":
    sys.exit(main())