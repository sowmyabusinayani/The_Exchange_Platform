import hashlib
import string
from datetime import datetime


class URLShortener:
    """
    Generates shortened URLs for sharing long tracking/catalog links.

    Algorithm:
    1. Hash the original URL using MD5
    2. Convert hash to Base62 (a-z, A-Z, 0-9)
    3. Take first 7 characters as short code
    4. Store mapping in memory
    """

    def __init__(self):
        """Initialize storage for URL mappings"""
        # In-memory storage: {short_code: url_data}
        self.url_map = {}

        # Base62 characters (URL-safe, no special chars)
        self.base62_chars = string.ascii_letters + string.digits  # a-z, A-Z, 0-9

    def shorten(self, original_url, purpose="general"):
        """
        Generate a shortened URL code.

        Args:
            original_url (str): The full URL to shorten
            purpose (str): Business context - helps with tracking
                          Options: "order_tracking", "catalog_share", "invoice_link"

        Returns:
            str: The short code (6-7 characters)

        Example:
            >>> shortener = URLShortener()
            >>> code = shortener.shorten("http://localhost:5000/orders/details?id=123", "order_tracking")
            >>> print(code)  # "aB3xK9"
        """
        # STEP 1: Generate hash from URL
        # MD5 creates consistent hash - same URL always gets same code
        url_hash = hashlib.md5(original_url.encode()).hexdigest()
        # STEP 2: Take first 8 hex characters
        hash_segment = url_hash[:8]

        # STEP 3: Convert hex to integer
        hash_int = int(hash_segment, 16)

        # STEP 4: Convert to Base62 (compact representation)
        short_code = self._encode_base62(hash_int)[:7]  # Keep only 7 chars

        # STEP 5: Store the mapping
        self.url_map[short_code] = {
            'url': original_url,
            'purpose': purpose,
            'created_at': datetime.now(),
            'click_count': 0  # Track how many times link is accessed
        }

        return short_code

    def expand(self, short_code):
        """
        Retrieve the original URL from a short code.
        Also increments the click counter.

        Args:
            short_code (str): The shortened code (e.g., "aB3xK9")

        Returns:
            str or None: Original URL if found, None if not found

        Example:
            >>> shortener = URLShortener()
            >>> url = shortener.expand("aB3xK9")
            >>> print(url)  # "http://localhost:5000/orders/details?id=123"
        """
        if short_code in self.url_map:
            # Increment click counter (analytics)
            self.url_map[short_code]['click_count'] += 1

            # Return the original URL
            return self.url_map[short_code]['url']

        return None  # Short code not found

    def get_stats(self, short_code):
        """
        Get analytics for a shortened URL.
        Useful for tracking link engagement.

        Args:
            short_code (str): The shortened code

        Returns:
            dict or None: Statistics about the link

        Example:
            >>> stats = shortener.get_stats("aB3xK9")
            >>> print(stats['click_count'])  # 5
        """
        return self.url_map.get(short_code)

    def _encode_base62(self, num):
        """
        Convert an integer to Base62 string.
        Base62 uses: a-z (26) + A-Z (26) + 0-9 (10) = 62 characters

        This is similar to how YouTube generates video IDs.

        Args:
            num (int): The number to encode

        Returns:
            str: Base62 encoded string

        Example:
            >>> shortener = URLShortener()
            >>> encoded = shortener._encode_base62(123456)
            >>> print(encoded)  # "w7e"
        """
        if num == 0:
            return self.base62_chars[0]

        result = []
        while num > 0:
            # Get remainder when dividing by 62
            remainder = num % 62

            # Map remainder to corresponding character
            result.append(self.base62_chars[remainder])

            # Integer division
            num //= 62

        # Reverse because we built the string backwards
        return ''.join(reversed(result))


# Example Usage (for testing)
if __name__ == "__main__":
    # Create shortener instance
    shortener = URLShortener()

    # Test Case 1: Shorten an order tracking URL
    long_url = "http://localhost:5000/orders/details?order_id=10492&customer=102&date=2024-12-06"
    short_code = shortener.shorten(long_url, purpose="order_tracking")
    print(f"Original: {long_url}")
    print(f"Shortened: /t/{short_code}")
    print()

    # Test Case 2: Expand the short code
    expanded = shortener.expand(short_code)
    print(f"Expanded: {expanded}")
    print(f"Match: {expanded == long_url}")
    print()

    # Test Case 3: Check statistics
    stats = shortener.get_stats(short_code)
    print(f"Stats: {stats}")
    print()

    # Test Case 4: Same URL = Same code (consistency)
    short_code_2 = shortener.shorten(long_url, purpose="order_tracking")
    print(f"Same URL shortened again: /t/{short_code_2}")
    print(f"Codes match: {short_code == short_code_2}")
