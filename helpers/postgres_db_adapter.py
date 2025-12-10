# -*- coding: utf-8 -*-
"""
PostgreSQL Database Adapter untuk DeepHoaxID
Adapter untuk menggantikan Firebase dengan PostgreSQL
"""

import pandas as pd
import logging
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.orm import joinedload

from db.connection import SessionLocal
from models.entities import Article, Category, Classification

# Setup logging
logger = logging.getLogger(__name__)

class PostgreSQLDatabaseAdapter:
    """
    Adapter untuk menggunakan PostgreSQL sebagai database untuk DeepHoaxID
    Menggantikan Firebase DatabaseManager
    """
    
    def __init__(self):
        """Initialize database adapter"""
        self.is_connected = True  # PostgreSQL connection handled by SessionLocal
        self.session = None
    
    def _get_session(self):
        """Get database session"""
        if self.session is None:
            self.session = SessionLocal()
        return self.session
    
    def load_hoax_articles(self) -> pd.DataFrame:
        """
        Load semua artikel hoax dari PostgreSQL
        
        Returns:
            pd.DataFrame: DataFrame berisi artikel hoax
        """
        try:
            session = self._get_session()
            logger.info("Loading articles from PostgreSQL...")
            
            # Load articles with relationships
            articles = (
                session.query(Article)
                .options(
                    joinedload(Article.categories),
                    joinedload(Article.classifications),
                    joinedload(Article.references)
                )
                .all()
            )
            
            # Convert to list of dicts
            raw_data = []
            for article in articles:
                # Get categories (use classifications as truth_category)
                categories = [c.name for c in article.categories] if article.categories else []
                classifications = [c.name for c in article.classifications] if article.classifications else []
                
                # Use first classification as truth_category, or first category as fallback
                truth_category = classifications[0] if classifications else (categories[0] if categories else 'UNKNOWN')
                
                # Combine title and content for text field
                text_content = ""
                if article.title:
                    text_content += str(article.title)
                if article.content:
                    text_content += " " + str(article.content)
                
                # Build article dict
                article_dict = {
                    'id': article.id,
                    'title': article.title or '',
                    'text': text_content.strip(),
                    'content': article.content or '',
                    'description': article.description or '',
                    'author': article.author or '',
                    'source_url': article.source_url or '',
                    'url': article.source_url or '',  # Alias for compatibility
                    'image_url': article.image_url or '',
                    'published_at': article.published_at.isoformat() if article.published_at else None,
                    'date': article.published_at.isoformat() if article.published_at else None,  # Alias
                    'created_at': article.created_at.isoformat() if article.created_at else None,
                    'updated_at': article.updated_at.isoformat() if article.updated_at else None,
                    'status': article.status or '',
                    'fact': article.fact or '',
                    'source_issue': article.source_issue or '',
                    'source_link': article.source_link or '',
                    'truth_category': truth_category,
                    'categories': ', '.join(categories),
                    'classifications': ', '.join(classifications),
                    'references': ', '.join([r.ref_url for r in article.references]) if article.references else ''
                }
                
                raw_data.append(article_dict)
            
            # Create DataFrame
            df = pd.DataFrame(raw_data)
            
            if not df.empty:
                logger.info(f"Loaded {len(df)} articles from PostgreSQL")
                logger.info(f"Columns: {list(df.columns)}")
                
                # Basic data validation
                self._validate_data(df)
            else:
                logger.warning("No articles found in database")
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading articles from PostgreSQL: {e}")
            return pd.DataFrame()
        finally:
            if self.session:
                self.session.close()
                self.session = None
    
    def _validate_data(self, df: pd.DataFrame) -> Dict:
        """
        Validate loaded data dan berikan statistik
        
        Args:
            df (pd.DataFrame): DataFrame untuk divalidasi
            
        Returns:
            Dict: Statistik validasi
        """
        stats = {
            'total_articles': len(df),
            'columns': list(df.columns),
            'completeness': {},
            'truth_categories': {},
            'date_range': None
        }
        
        # Check data completeness
        for col in df.columns:
            non_null = df[col].notna().sum()
            percentage = (non_null / len(df)) * 100 if len(df) > 0 else 0
            stats['completeness'][col] = {
                'count': non_null,
                'percentage': percentage
            }
            
            if percentage < 50 and len(df) > 0:
                logger.warning(f"⚠️ Column '{col}' has low completeness: {percentage:.1f}%")
        
        # Analyze truth categories
        if 'truth_category' in df.columns:
            stats['truth_categories'] = df['truth_category'].value_counts().to_dict()
            logger.info(f"🏷️ Truth categories: {stats['truth_categories']}")
        
        # Check date range
        if 'date' in df.columns and df['date'].notna().sum() > 0:
            try:
                date_series = pd.to_datetime(df['date'], errors='coerce')
                valid_dates = date_series.dropna()
                if len(valid_dates) > 0:
                    stats['date_range'] = {
                        'start': valid_dates.min(),
                        'end': valid_dates.max(),
                        'span_days': (valid_dates.max() - valid_dates.min()).days
                    }
                    logger.info(f"📅 Date range: {stats['date_range']['start']} to {stats['date_range']['end']}")
            except Exception as e:
                logger.warning(f"⚠️ Could not parse date information: {e}")
        
        return stats
    
    def health_check(self) -> Dict:
        """
        Perform database health check
        
        Returns:
            Dict: Health status
        """
        health = {
            'database_connected': self.is_connected,
            'timestamp': datetime.now().isoformat(),
            'status': 'unknown'
        }
        
        try:
            session = self._get_session()
            
            # Test query - count articles
            article_count = session.query(Article).count()
            
            if article_count > 0:
                health['status'] = 'healthy'
                health['message'] = 'Database accessible and contains data'
                health['stats'] = {
                    'total_articles': article_count
                }
            else:
                health['status'] = 'empty'
                health['message'] = 'Database accessible but no data found'
                health['stats'] = {
                    'total_articles': 0
                }
            
            session.close()
            return health
            
        except Exception as e:
            health['status'] = 'error'
            health['message'] = str(e)
            logger.error(f"Health check failed: {e}")
            return health
    
    def get_database_stats(self) -> Dict:
        """
        Get statistik database
        
        Returns:
            Dict: Database statistics
        """
        try:
            df = self.load_hoax_articles()
            
            if df.empty:
                return {'error': 'No data available'}
            
            stats = {
                'connection_status': 'connected',
                'total_articles': len(df),
                'truth_categories': df['truth_category'].value_counts().to_dict() if 'truth_category' in df.columns else {},
                'data_completeness': {},
                'last_updated': datetime.now().isoformat(),
                'source': 'PostgreSQL Database',
                'language': 'Indonesian'
            }
            
            # Data completeness
            for col in df.columns:
                non_null = df[col].notna().sum()
                stats['data_completeness'][col] = {
                    'count': non_null,
                    'percentage': (non_null / len(df)) * 100 if len(df) > 0 else 0
                }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {'error': str(e)}

