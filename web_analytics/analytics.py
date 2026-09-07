import sqlite3
from datetime import date, timedelta
from typing import Dict, List, Optional
import json


class WebAnalytics:
    """A simple web traffic analytics library using SQLite for count-based data storage."""
    
    # Country to continent mapping for anonymization
    CONTINENT_MAP = {
        # North America
        "United States": "North America", "Canada": "North America", "Mexico": "North America",
        # Europe
        "United Kingdom": "Europe", "Germany": "Europe", "France": "Europe", "Italy": "Europe",
        "Spain": "Europe", "Netherlands": "Europe", "Belgium": "Europe", "Switzerland": "Europe",
        "Austria": "Europe", "Sweden": "Europe", "Norway": "Europe", "Denmark": "Europe", "Finland": "Europe", "Poland": "Europe",
        # Asia
        "China": "Asia", "Japan": "Asia", "India": "Asia", "South Korea": "Asia",
        "Singapore": "Asia", "Thailand": "Asia", "Vietnam": "Asia", "Indonesia": "Asia",
        # Oceania
        "Australia": "Oceania", "New Zealand": "Oceania",
        # South America
        "Brazil": "South America", "Argentina": "South America", "Chile": "South America",
        # Africa
        "South Africa": "Africa", "Egypt": "Africa", "Nigeria": "Africa",
    }
    
    # Country to region mapping for less aggressive anonymization
    REGION_MAP = {
        "United States": "North America", "Canada": "North America", "Mexico": "North America",
        "United Kingdom": "Western Europe", "Germany": "Western Europe", "France": "Western Europe",
        "Italy": "Southern Europe", "Spain": "Southern Europe",
        "China": "East Asia", "Japan": "East Asia", "South Korea": "East Asia",
        "India": "South Asia", "Thailand": "Southeast Asia", "Vietnam": "Southeast Asia",
        "Australia": "Oceania", "Brazil": "South America",
    }
    
    def __init__(
        self,
        db_path: str = "web_analytics.db",
        track_country: bool = True,
        retention_days: Optional[int] = None,
        anonymize_country: bool = False,
        country_anonymization_level: str = "region"
    ):
        """
        Initialize the WebAnalytics instance.
        
        Args:
            db_path: Path to the SQLite database file. Defaults to 'web_analytics.db'.
            track_country: Whether to track visitor countries. Defaults to True.
            retention_days: Number of days to retain data. None means keep forever. Defaults to None.
            anonymize_country: Whether to anonymize country data. Defaults to False.
            country_anonymization_level: Level of anonymization ('region' or 'continent'). Defaults to 'region'.
        """
        self.db_path = db_path
        self.track_country = track_country
        self.retention_days = retention_days
        self.anonymize_country = anonymize_country
        self.country_anonymization_level = country_anonymization_level
        self._initialize_database()
        self._apply_retention_policy()
    
    def _initialize_database(self):
        """Create the necessary tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Daily visitor counts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_visitors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    visit_date DATE UNIQUE,
                    count INTEGER DEFAULT 0
                )
            """)
            
            # Country counts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS country_counts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    country TEXT UNIQUE,
                    count INTEGER DEFAULT 0
                )
            """)
            
            # Page view counts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS page_counts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    page_url TEXT UNIQUE,
                    count INTEGER DEFAULT 0
                )
            """)
            
            conn.commit()
    
    def _apply_retention_policy(self):
        """Apply data retention policy by deleting old data."""
        if self.retention_days is not None and self.retention_days > 0:
            cutoff_date = (date.today() - timedelta(days=self.retention_days)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Delete old daily visitor records
                cursor.execute(
                    "DELETE FROM daily_visitors WHERE visit_date < ?",
                    (cutoff_date,)
                )
                
                conn.commit()
    
    def apply_retention_policy_now(self):
        """
        Manually trigger the retention policy to delete old data.
        This can be called periodically to clean up data.
        """
        self._apply_retention_policy()
    
    def _anonymize_country(self, country: str) -> str:
        """
        Anonymize country name based on configured level.
        
        Args:
            country: Original country name
            
        Returns:
            Anonymized country/region name
        """
        if self.country_anonymization_level == "continent":
            return self.CONTINENT_MAP.get(country, "Other")
        elif self.country_anonymization_level == "region":
            return self.REGION_MAP.get(country, "Other")
        else:
            return country
    
    def increment_visitor(self, country: str = "Unknown"):
        """
        Increment the visitor count for today and for the specified country.
        
        Args:
            country: Country of the visitor (default: "Unknown")
        """
        today = date.today().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Increment daily count
            cursor.execute(
                """
                INSERT INTO daily_visitors (visit_date, count)
                VALUES (?, 1)
                ON CONFLICT(visit_date) DO UPDATE SET count = count + 1
                """,
                (today,)
            )
            
            # Increment country count if tracking is enabled
            if self.track_country:
                processed_country = country
                if self.anonymize_country:
                    processed_country = self._anonymize_country(country)
                
                cursor.execute(
                    """
                    INSERT INTO country_counts (country, count)
                    VALUES (?, 1)
                    ON CONFLICT(country) DO UPDATE SET count = count + 1
                    """,
                    (processed_country,)
                )
            
            conn.commit()
    
    def increment_page_view(self, page_url: str):
        """
        Increment the page view count for a specific page.
        
        Args:
            page_url: The URL of the page
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO page_counts (page_url, count)
                VALUES (?, 1)
                ON CONFLICT(page_url) DO UPDATE SET count = count + 1
                """,
                (page_url,)
            )
            conn.commit()
    
    def get_total_visitors(self) -> int:
        """
        Get the total number of visitors across all days.
        
        Returns:
            Total visitor count
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(count) FROM daily_visitors")
            result = cursor.fetchone()[0]
            return result if result is not None else 0
    
    def get_today_visitors(self) -> int:
        """
        Get the number of visitors today.
        
        Returns:
            Today's visitor count
        """
        today = date.today().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT count FROM daily_visitors WHERE visit_date = ?",
                (today,)
            )
            result = cursor.fetchone()
            return result[0] if result else 0
    
    def get_visitors_by_country(self) -> Dict[str, int]:
        """
        Get visitor counts grouped by country.
        
        Returns:
            Dictionary mapping country names to visitor counts
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT country, count 
                FROM country_counts 
                ORDER BY count DESC
                """
            )
            return dict(cursor.fetchall())
    
    def get_page_views_stats(self) -> Dict[str, int]:
        """
        Get page view statistics grouped by page URL.
        
        Returns:
            Dictionary mapping page URLs to view counts
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT page_url, count 
                FROM page_counts 
                ORDER BY count DESC
                """
            )
            return dict(cursor.fetchall())
    
    def get_visitor_stats_by_date(self, days: int = 30) -> List[Dict[str, any]]:
        """
        Get visitor statistics grouped by date.
        
        Args:
            days: Number of days to include (default: 30)
            
        Returns:
            List of dictionaries with date and visitor count
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT visit_date as date, count 
                FROM daily_visitors 
                WHERE visit_date >= date('now', '-' || ? || ' days')
                ORDER BY date DESC
                """,
                (days,)
            )
            return [{"date": row[0], "count": row[1]} for row in cursor.fetchall()]
    
    def get_top_pages(self, limit: int = 10) -> List[Dict[str, any]]:
        """
        Get the most visited pages.
        
        Args:
            limit: Number of top pages to return (default: 10)
            
        Returns:
            List of dictionaries with page_url and view count
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT page_url, count 
                FROM page_counts 
                ORDER BY count DESC 
                LIMIT ?
                """,
                (limit,)
            )
            return [{"page_url": row[0], "count": row[1]} for row in cursor.fetchall()]
    
    def get_analytics_summary(self) -> Dict[str, any]:
        """
        Get a comprehensive summary of all analytics.
        
        Returns:
            Dictionary containing all analytics metrics
        """
        return {
            "total_visitors": self.get_total_visitors(),
            "today_visitors": self.get_today_visitors(),
            "visitors_by_country": self.get_visitors_by_country(),
            "page_views_stats": self.get_page_views_stats(),
            "top_pages": self.get_top_pages(),
            "visitor_stats_by_date": self.get_visitor_stats_by_date()
        }
    
    def export_data(self, format: str = "json") -> str:
        """
        Export analytics data.
        
        Args:
            format: Export format ('json' or 'csv')
            
        Returns:
            Exported data as string
        """
        summary = self.get_analytics_summary()
        
        if format == "json":
            return json.dumps(summary, indent=2, default=str)
        elif format == "csv":
            lines = []
            # Visitors by country
            lines.append("Country,Visitor Count")
            for country, count in summary["visitors_by_country"].items():
                lines.append(f"{country},{count}")
            lines.append("")
            # Page views
            lines.append("Page URL,View Count")
            for page, count in summary["page_views_stats"].items():
                lines.append(f"{page},{count}")
            return "\n".join(lines)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def clear_data(self):
        """Clear all analytics data from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM page_counts")
            cursor.execute("DELETE FROM country_counts")
            cursor.execute("DELETE FROM daily_visitors")
            conn.commit()
