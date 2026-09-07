# Web Analytics Library

A simple and lightweight Python library for tracking web traffic analytics using SQLite for data storage.

## Features

- Track visitor counts by country (no personal data stored)
- Track page view counts for each page
- Get total visitors count
- Get today's visitors count
- Get visitor counts grouped by country
- Get page view statistics
- Get visitor statistics by date
- Export data in JSON or CSV format
- **Privacy-focused: only stores counts, no IP addresses or personal data**
- **Privacy controls: disable country tracking, data retention policies, country anonymization**
- No external dependencies - uses only Python standard library

## Installation

### Install from PyPI

```bash
pip install webanalytics
```

### Install from source

```bash
pip install .
```

### Install in development mode

```bash
pip install -e .
```

## Usage

### Basic Example

```python
from web_analytics import WebAnalytics

# Initialize the analytics instance
analytics = WebAnalytics(db_path="my_analytics.db")

# Track a visitor (only country is stored, no personal data)
analytics.increment_visitor(country="United States")

# Track page views
analytics.increment_page_view("/home")
analytics.increment_page_view("/about")
analytics.increment_page_view("/contact")

# Get analytics data
total_visitors = analytics.get_total_visitors()
today_visitors = analytics.get_today_visitors()
visitors_by_country = analytics.get_visitors_by_country()
page_views_stats = analytics.get_page_views_stats()

print(f"Total visitors: {total_visitors}")
print(f"Today's visitors: {today_visitors}")
print(f"Visitors by country: {visitors_by_country}")
print(f"Page views: {page_views_stats}")
```

### Getting Analytics Summary

```python
from web_analytics import WebAnalytics

analytics = WebAnalytics()

# Get a comprehensive summary
summary = analytics.get_analytics_summary()

print(summary)
# Output:
# {
#     "total_visitors": 150,
#     "today_visitors": 25,
#     "visitors_by_country": {"United States": 80, "United Kingdom": 30, ...},
#     "page_views_stats": {"/home": 200, "/about": 150, ...},
#     "top_pages": [...],
#     "visitor_stats_by_date": [...]
# }
```

### Export Data

```python
from web_analytics import WebAnalytics

analytics = WebAnalytics()

# Export as JSON
json_data = analytics.export_data(format="json")
print(json_data)

# Export as CSV
csv_data = analytics.export_data(format="csv")
print(csv_data)
```

### Privacy Features

The library includes several privacy-focused features to help with compliance:

#### Disable Country Tracking

```python
from web_analytics import WebAnalytics

# Disable country tracking entirely
analytics = WebAnalytics(
    db_path="my_analytics.db",
    track_country=False
)

analytics.increment_visitor()  # Country parameter ignored
analytics.increment_page_view("/home")
```

#### Country Anonymization

Anonymize country data by grouping countries into regions or continents:

```python
from web_analytics import WebAnalytics

# Anonymize by region (less aggressive)
analytics = WebAnalytics(
    db_path="my_analytics.db",
    anonymize_country=True,
    country_anonymization_level="region"
)
# "United States" → "North America"
# "Germany" → "Western Europe"

# Anonymize by continent (more aggressive)
analytics = WebAnalytics(
    db_path="my_analytics.db",
    anonymize_country=True,
    country_anonymization_level="continent"
)
# "United States" → "North America"
# "Germany" → "Europe"
# "Japan" → "Asia"
```

#### Data Retention Policy

Automatically delete old data after a specified number of days:

```python
from web_analytics import WebAnalytics

# Keep data for 90 days only
analytics = WebAnalytics(
    db_path="my_analytics.db",
    retention_days=90
)

# Data older than 90 days is automatically deleted on initialization
# You can also manually trigger cleanup:
analytics.apply_retention_policy_now()
```

#### Maximum Privacy Configuration

Combine all privacy features for maximum compliance:

```python
from web_analytics import WebAnalytics

analytics = WebAnalytics(
    db_path="my_analytics.db",
    track_country=False,        # No country tracking
    retention_days=90           # Auto-delete after 90 days
)

analytics.increment_visitor()
analytics.increment_page_view("/home")
```

### API Reference

#### `WebAnalytics(db_path: str = "web_analytics.db", track_country: bool = True, retention_days: Optional[int] = None, anonymize_country: bool = False, country_anonymization_level: str = "region")`

Initialize the WebAnalytics instance.

**Parameters:**
- `db_path`: Path to the SQLite database file (default: "web_analytics.db")
- `track_country`: Whether to track visitor countries (default: True)
- `retention_days`: Number of days to retain data. None means keep forever (default: None)
- `anonymize_country`: Whether to anonymize country data (default: False)
- `country_anonymization_level`: Level of anonymization - 'region' or 'continent' (default: "region")

#### `increment_visitor(country="Unknown")`

Increment the visitor count for today and for the specified country.

**Parameters:**
- `country`: Country of the visitor (default: "Unknown")

#### `increment_page_view(page_url)`

Increment the page view count for a specific page.

**Parameters:**
- `page_url`: The URL of the page

#### `get_total_visitors()`

Get the total number of unique visitors.

**Returns:** Total visitor count

#### `get_today_visitors()`

Get the number of visitors today.

**Returns:** Today's visitor count

#### `get_visitors_by_country()`

Get visitor counts grouped by country.

**Returns:** Dictionary mapping country names to visitor counts

#### `get_page_views_stats()`

Get page view statistics grouped by page URL.

**Returns:** Dictionary mapping page URLs to view counts

#### `get_visitor_stats_by_date(days=30)`

Get visitor statistics grouped by date.

**Parameters:**
- `days`: Number of days to include (default: 30)

**Returns:** List of dictionaries with date and visitor count

#### `get_top_pages(limit=10)`

Get the most visited pages.

**Parameters:**
- `limit`: Number of top pages to return (default: 10)

**Returns:** List of dictionaries with page_url and view count

#### `get_analytics_summary()`

Get a comprehensive summary of all analytics.

**Returns:** Dictionary containing all analytics metrics

#### `export_data(format="json")`

Export analytics data.

**Parameters:**
- `format`: Export format ('json' or 'csv')

**Returns:** Exported data as string

#### `clear_data()`

Clear all analytics data from the database.

#### `apply_retention_policy_now()`

Manually trigger the retention policy to delete old data immediately.

## Privacy & Compliance

This library is designed with privacy in mind:

- **No personal data stored**: Only aggregate counts are stored, no IP addresses, user agents, or session IDs
- **Country tracking optional**: Can be completely disabled for maximum privacy
- **Data anonymization**: Country data can be anonymized at region or continent level
- **Data retention**: Automatic deletion of old data based on configurable retention policies
- **GDPR-friendly**: Since no personal data is stored, GDPR requirements are minimized
- **CCPA-compliant**: No personal information is collected or stored

**Note**: While this library is designed to be privacy-friendly, you should consult with legal counsel to ensure compliance with applicable laws in your jurisdiction, especially regarding how you obtain country data (e.g., from IP geolocation).

## Database Schema

The library uses SQLite with three simple count-based tables:

### daily_visitors
- `id`: Primary key
- `visit_date`: Date of the visit (unique)
- `count`: Number of visitors on that date

### country_counts
- `id`: Primary key
- `country`: Country name (unique)
- `count`: Total number of visitors from that country

### page_counts
- `id`: Primary key
- `page_url`: Page URL (unique)
- `count`: Total number of page views for that URL

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
