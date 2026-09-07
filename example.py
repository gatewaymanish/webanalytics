"""
Example usage of the web_analytics library.
This script demonstrates how to use the library to track visitors and page views.
"""

from web_analytics import WebAnalytics

def main():
    # Initialize the analytics instance
    analytics = WebAnalytics(db_path="example_analytics.db")
    
    print("=== Web Analytics Library Example ===\n")
    
    # Clear existing data for clean example
    analytics.clear_data()
    print("Cleared existing data.\n")
    
    # Track some visitors (count-based, no personal data)
    print("Tracking visitors...")
    
    # Visitor 1 from United States
    analytics.increment_visitor(country="United States")
    analytics.increment_page_view("/home")
    analytics.increment_page_view("/about")
    analytics.increment_page_view("/products")
    
    # Visitor 2 from United Kingdom
    analytics.increment_visitor(country="United Kingdom")
    analytics.increment_page_view("/home")
    analytics.increment_page_view("/contact")
    
    # Visitor 3 from United States
    analytics.increment_visitor(country="United States")
    analytics.increment_page_view("/home")
    analytics.increment_page_view("/about")
    
    # Visitor 4 from Germany
    analytics.increment_visitor(country="Germany")
    analytics.increment_page_view("/home")
    analytics.increment_page_view("/products")
    analytics.increment_page_view("/products/item1")
    
    # Visitor 5 from India
    analytics.increment_visitor(country="India")
    analytics.increment_page_view("/home")
    
    print("Tracked 5 visitors with page views.\n")
    
    # Get and display analytics
    print("=== Analytics Results ===\n")
    
    # Total visitors
    total = analytics.get_total_visitors()
    print(f"Total visitors: {total}")
    
    # Today's visitors
    today = analytics.get_today_visitors()
    print(f"Today's visitors: {today}")
    
    # Visitors by country
    print("\nVisitors by country:")
    for country, count in analytics.get_visitors_by_country().items():
        print(f"  {country}: {count}")
    
    # Page views statistics
    print("\nPage views statistics:")
    for page, count in analytics.get_page_views_stats().items():
        print(f"  {page}: {count} views")
    
    
    # Top pages
    print("\nTop 3 pages:")
    for page_data in analytics.get_top_pages(limit=3):
        print(f"  {page_data['page_url']}: {page_data['count']} views")
    
    # Get full summary
    print("\n=== Full Analytics Summary ===")
    summary = analytics.get_analytics_summary()
    import json
    print(json.dumps(summary, indent=2, default=str))
    
    # Export data
    print("\n=== Export Data (JSON) ===")
    json_export = analytics.export_data(format="json")
    print(json_export)
    
    print("\n=== Export Data (CSV) ===")
    csv_export = analytics.export_data(format="csv")
    print(csv_export)
    
    print("\n=== Example completed ===")
    
    print("\n" + "="*50)
    print("=== Privacy Features Examples ===")
    print("="*50 + "\n")
    
    # Example 1: Disable country tracking
    print("Example 1: Analytics with country tracking disabled")
    analytics_no_country = WebAnalytics(
        db_path="example_no_country.db",
        track_country=False
    )
    analytics_no_country.clear_data()
    
    analytics_no_country.increment_visitor(country="United States")
    analytics_no_country.increment_visitor(country="Germany")
    analytics_no_country.increment_page_view("/home")
    
    print(f"Total visitors: {analytics_no_country.get_total_visitors()}")
    print(f"Visitors by country: {analytics_no_country.get_visitors_by_country()}")
    print("(Country tracking disabled - no country data stored)\n")
    
    # Example 2: Country anonymization by region
    print("Example 2: Analytics with country anonymization (region level)")
    analytics_anon_region = WebAnalytics(
        db_path="example_anon_region.db",
        anonymize_country=True,
        country_anonymization_level="region"
    )
    analytics_anon_region.clear_data()
    
    analytics_anon_region.increment_visitor(country="United States")
    analytics_anon_region.increment_visitor(country="Canada")
    analytics_anon_region.increment_visitor(country="Germany")
    analytics_anon_region.increment_visitor(country="France")
    
    print(f"Visitors by anonymized region: {analytics_anon_region.get_visitors_by_country()}")
    print("(Countries grouped into regions)\n")
    
    # Example 3: Country anonymization by continent
    print("Example 3: Analytics with country anonymization (continent level)")
    analytics_anon_continent = WebAnalytics(
        db_path="example_anon_continent.db",
        anonymize_country=True,
        country_anonymization_level="continent"
    )
    analytics_anon_continent.clear_data()
    
    analytics_anon_continent.increment_visitor(country="United States")
    analytics_anon_continent.increment_visitor(country="Germany")
    analytics_anon_continent.increment_visitor(country="Japan")
    analytics_anon_continent.increment_visitor(country="Brazil")
    
    print(f"Visitors by anonymized continent: {analytics_anon_continent.get_visitors_by_country()}")
    print("(Countries grouped into continents)\n")
    
    # Example 4: Data retention policy
    print("Example 4: Analytics with 30-day data retention")
    analytics_retention = WebAnalytics(
        db_path="example_retention.db",
        retention_days=30
    )
    analytics_retention.clear_data()
    
    analytics_retention.increment_visitor(country="United States")
    analytics_retention.increment_page_view("/home")
    
    print(f"Total visitors: {analytics_retention.get_total_visitors()}")
    print(f"Retention policy: 30 days (data older than 30 days will be auto-deleted)")
    print("Call apply_retention_policy_now() to manually trigger cleanup\n")
    
    # Example 5: Maximum privacy configuration
    print("Example 5: Maximum privacy configuration")
    analytics_privacy = WebAnalytics(
        db_path="example_privacy.db",
        track_country=False,
        retention_days=90
    )
    analytics_privacy.clear_data()
    
    analytics_privacy.increment_visitor()
    analytics_privacy.increment_page_view("/home")
    
    print(f"Total visitors: {analytics_privacy.get_total_visitors()}")
    print(f"Visitors by country: {analytics_privacy.get_visitors_by_country()}")
    print("(No country tracking, 90-day retention - maximum privacy)\n")
    
    print("=== Privacy Examples completed ===")

if __name__ == "__main__":
    main()
