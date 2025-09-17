"""Distributed cache implementation using Redis for multi-instance deployments.

This module provides a Redis-backed implementation of the ContactCache interface
to enable sharing of cached contact data across multiple application instances.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from .contact_cache import CachedContact, ContactCache

try:  # pragma: no cover - optional dependency
    from redis.exceptions import RedisError
except (ImportError, ModuleNotFoundError):  # pragma: no cover - redis not installed
    class RedisError(Exception):
        """Fallback Redis error type when the redis package is unavailable."""


_RECOVERABLE_ERRORS = (RedisError, ConnectionError, TimeoutError, OSError, AttributeError)

if TYPE_CHECKING:
    from pathlib import Path


class RedisContactCache(ContactCache):
    """Redis-backed cache for revealed contacts in multi-instance deployments."""

    def __init__(
        self,
        cache_path: Path | None = None,
        *,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        prefix: str = "signalhire_cache",
        redis_client: Any | None = None,
    ) -> None:
        """Initialize a Redis-backed contact cache.

        Args:
            cache_path: Local cache path for fallback persistence.
            redis_host: Redis server hostname when a client is not provided.
            redis_port: Redis server port when a client is not provided.
            prefix: Key prefix for namespacing cached entries.
            redis_client: Optional pre-configured Redis client for testing or
                dependency injection.
        """
        super().__init__(cache_path)
        self._validate_init_args(redis_host, redis_port, prefix)
        self._prefix = prefix
        self._redis_client: Any | None = None
        self._redis_config = {
            "host": redis_host,
            "port": redis_port,
            "decode_responses": True,
        }
        if redis_client is not None:
            self._redis_available = self._validate_client(redis_client)
            self._redis_client = redis_client if self._redis_available else None
        else:
            self._redis_available = self._initialize_redis()

    @staticmethod
    def _validate_init_args(
        redis_host: str,
        redis_port: int,
        prefix: str,
    ) -> None:
        if not isinstance(redis_host, str) or not redis_host:
            raise ValueError("redis_host must be a non-empty string")
        if not isinstance(redis_port, int) or redis_port <= 0:
            raise ValueError("redis_port must be a positive integer")
        if not isinstance(prefix, str) or not prefix:
            raise ValueError("prefix must be a non-empty string")

    @staticmethod
    def _validate_client(redis_client: Any) -> bool:
        required_methods = {"ping", "get", "set", "keys", "delete"}
        if not all(hasattr(redis_client, method) for method in required_methods):
            raise ValueError(
                "redis_client must provide ping, get, set, keys, and delete methods"
            )
        try:
            redis_client.ping()
        except _RECOVERABLE_ERRORS:
            return False
        return True

    def _initialize_redis(self) -> bool:
        """Initialize Redis connection and verify availability."""
        try:
            import redis  # type: ignore[import-not-found]
        except ModuleNotFoundError:
            self._redis_client = None
            return False

        try:
            client = redis.Redis(**self._redis_config)
            client.ping()
        except _RECOVERABLE_ERRORS:
            self._redis_client = None
            return False

        self._redis_client = client
        return True

    def _make_key(self, uid: str) -> str:
        """Create a Redis key with the configured prefix.

        Args:
            uid: The contact UID

        Returns:
            str: The full Redis key
        """
        self._validate_uid(uid)
        return f"{self._prefix}:{uid}"

    def _ensure_loaded(self) -> None:
        """Override to ensure data is loaded from Redis if available."""
        if self._loaded:
            return

        # Load from local cache as fallback
        super()._ensure_loaded()

        # If Redis is available, sync data from Redis
        if self._redis_available and self._redis_client:
            try:
                pattern = f"{self._prefix}:*"
                keys = self._redis_client.keys(pattern)

                prefix = f"{self._prefix}:"
                for key in keys:
                    raw_key = (
                        key.decode("utf-8") if isinstance(key, bytes) else str(key)
                    )
                    if not raw_key.startswith(prefix):
                        continue
                    uid = raw_key[len(prefix) :]
                    data_json = self._redis_client.get(key)
                    if data_json:
                        data = json.loads(data_json)
                        contact = CachedContact.from_dict(uid, data)
                        self._data[uid] = contact

            except _RECOVERABLE_ERRORS:
                pass

        self._loaded = True

    def get(self, uid: str) -> CachedContact | None:
        """Get cached contact data from Redis or local cache.

        Args:
            uid: The contact UID

        Returns:
            CachedContact | None: The cached contact or None if not found
        """
        self._validate_uid(uid)

        if self._redis_available and self._redis_client:
            try:
                key = self._make_key(uid)
                data_json = self._redis_client.get(key)
                if data_json:
                    data = json.loads(data_json)
                    contact = CachedContact.from_dict(uid, data)
                    self._data[uid] = contact
                    return contact
            except _RECOVERABLE_ERRORS:
                pass

        # Fall back to local cache
        self._ensure_loaded()
        return self._data.get(uid)

    def upsert(
        self,
        uid: str,
        *,
        contacts: Iterable[dict[str, Any]] | None = None,
        profile: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> CachedContact:
        """Upsert contact data to both Redis and local cache.

        Args:
            uid: The contact UID
            contacts: List of contact information
            profile: Profile data
            metadata: Additional metadata

        Returns:
            CachedContact: The updated cached contact
        """
        self._validate_uid(uid)
        processed_contacts: list[dict[str, Any]] | None = None
        if contacts is not None:
            if isinstance(contacts, (str, bytes)) or not isinstance(contacts, Iterable):
                raise TypeError("contacts must be an iterable of dictionaries")
            processed_contacts = list(contacts)
            if not all(isinstance(entry, dict) for entry in processed_contacts):
                raise TypeError("each contact entry must be a dictionary")

        if profile is not None and not isinstance(profile, dict):
            raise TypeError("profile must be a dictionary")
        if metadata is not None and not isinstance(metadata, dict):
            raise TypeError("metadata must be a dictionary")
        return super().upsert(
            uid,
            contacts=processed_contacts,
            profile=profile,
            metadata=metadata,
        )

    def save(self) -> None:
        """Save cached data to Redis and local storage.

        This method syncs the local cache data to Redis and saves to local storage.
        """
        if not self._dirty:
            return

        # Save to local storage
        super().save()

        # Sync to Redis if available
        if self._redis_available and self._redis_client:
            try:
                for uid, contact in self._data.items():
                    key = self._make_key(uid)
                    data_json = json.dumps(contact.to_dict())
                    self._redis_client.set(key, data_json)
            except _RECOVERABLE_ERRORS:
                pass

        self._dirty = False

    def clear(self) -> None:
        """Clear both Redis and local cache data."""
        # Clear local cache
        super().clear()

        # Clear Redis data if available
        if self._redis_available and self._redis_client:
            try:
                pattern = f"{self._prefix}:*"
                keys = self._redis_client.keys(pattern)
                if keys:
                    self._redis_client.delete(*keys)
            except _RECOVERABLE_ERRORS:
                pass

    @staticmethod
    def _validate_uid(uid: str) -> None:
        if not isinstance(uid, str) or not uid:
            raise ValueError("uid must be a non-empty string")


# For backward compatibility
DistributedContactCache = RedisContactCache

__all__ = ["DistributedContactCache", "RedisContactCache"]
