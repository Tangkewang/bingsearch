"""Bing Search API Client"""
from .search import search, SearchResult
from .exceptions import BingSearchError

__version__ = "1.0.0"
__all__ = ['search', 'SearchResult', 'BingSearchError']
