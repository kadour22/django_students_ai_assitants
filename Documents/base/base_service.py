"""
Base service class for all business logic services.

Provides common functionality and patterns that all services should follow.
"""

from typing import Optional, Any, Dict, List
from django.core.cache import cache
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class BaseService:
   
    def __init__(self):
        self.cache_timeout = getattr(settings, 'CACHE_TIMEOUTS', {})

    def get_cache_key(self, prefix: str, **kwargs) -> str:
        key_parts = [prefix]
        for k, v in sorted(kwargs.items()):
            if v is not None:
                key_parts.append(f"{k}:{v}")
        return "_".join(key_parts)

    def get_from_cache(self, cache_key: str) -> Optional[Any]:
        try:
            return cache.get(cache_key)
        except Exception as e:
            logger.warning(f"Cache get failed for key {cache_key}: {e}")
            return None

    def set_cache(self, cache_key: str, data: Any, timeout: Optional[int] = None) -> bool:
        try:
            cache.set(cache_key, data, timeout=timeout)
            return True
        except Exception as e:
            logger.warning(f"Cache set failed for key {cache_key}: {e}")
            return False

    def delete_cache(self, cache_key: str) -> bool:
        try:
            cache.delete(cache_key)
            return True
        except Exception as e:
            logger.warning(f"Cache delete failed for key {cache_key}: {e}")
            return False

    def delete_cache_pattern(self, pattern: str) -> bool:
        try:
            if hasattr(cache, 'delete_pattern'):
                cache.delete_pattern(pattern)
                return True
            else:
                logger.warning("Cache backend doesn't support pattern deletion")
                return False
        except Exception as e:
            logger.warning(f"Cache pattern delete failed for {pattern}: {e}")
            return False

    def log_operation(self, operation: str, details: Dict[str, Any]) -> None:
        logger.info(f"{self.__class__.__name__}.{operation}: {details}")

    def log_error(self, operation: str, error: Exception, details: Dict[str, Any] = None) -> None:
        error_details = {
            'error': str(error),
            'error_type': type(error).__name__
        }
        if details:
            error_details.update(details)

        logger.error(
            f"{self.__class__.__name__}.{operation} failed: {error_details}",
            exc_info=True
        )

    def get_queryset_optimized(self, model_class: models.Model) -> models.QuerySet:
        return model_class.objects.all()
