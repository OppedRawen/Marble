import requests
import json
import time
from typing import Dict, List, Optional, Union


class RappiScraper:
    """
    A class to search for products on Rappi from Líder or Líder Express stores.
    
    This scraper uses Rappi's search API to find products and returns formatted
    results according to the specified schema.
    """
    
    def __init__(self, proxy_settings: Dict[str, str] = None):
        """
        Initialize the RappiScraper with optional proxy settings.
        
        Args:
            proxy_settings: Dictionary containing proxy configuration.
        """
        self.base_url = "https://services.rappi.cl/api/cpgs/search/v2/store"
        self.session = requests.Session()
        
        # Default headers to mimic browser behavior
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://www.rappi.cl",
            "Referer": "https://www.rappi.cl/"
        }
        
        # Set up proxy if provided
        if proxy_settings:
            self.proxies = proxy_settings
        else:
            # Default proxy settings from the task
            proxy = 'geo.iproyal.com:12321'
            proxy_auth = 'Qp2YvQ9hRCyienEj:GVPXaVCFvaFoMgZc_country-us'
            self.proxies = {
                'http': f'http://{proxy_auth}@{proxy}',
                'https': f'http://{proxy_auth}@{proxy}'
            }
        
        # Initialize cookies
        self.cookies = self._get_cookies()
    
    def _get_cookies(self) -> Dict[str, str]:
        """
        Get initial cookies from Rappi's website.
        
        Returns:
            Dictionary of cookies.
        """
        try:
            response = self.session.get(
                "https://www.rappi.cl/",
                headers=self.headers,
                proxies=self.proxies
            )
            return self.session.cookies.get_dict()
        except Exception as e:
            print(f"Error getting cookies: {e}")
            return {}
    
    def refresh_cookies(self) -> None:
        """Refresh the session cookies."""
        self.cookies = self._get_cookies()
    
    def search_products(self, query: str, store_id: str = "900020469") -> List[Dict[str, Union[str, int, None]]]:
        """
        Search for products on Rappi.
        
        Args:
            query: Search term to look for.
            store_id: ID of the store to search in (default is Express Líder).
        
        Returns:
            List of product dictionaries formatted according to the schema.
        """
        url = f"{self.base_url}/{store_id}/products"
        
        # Payload for the search request
        payload = {
            "search": query,
            # Add any additional parameters if needed
        }
        
        try:
            response = self.session.post(
                url,
                headers=self.headers,
                json=payload,
                cookies=self.cookies,
                proxies=self.proxies
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_products(data)
            else:
                print(f"Error: Status code {response.status_code}")
                return []
        
        except Exception as e:
            print(f"Error during search: {e}")
            return []
    
    def _parse_products(self, data: Dict) -> List[Dict[str, Union[str, int, None]]]:
        """
        Parse the API response and extract product information.
        
        Args:
            data: JSON response from the API.
        
        Returns:
            List of products formatted according to the schema.
        """
        formatted_products = []
        
        # Extract products from the response
        products = data.get("products", [])
        
        for product in products:
            # Map product data to required schema
            formatted_product = {
                "name": product.get("name", ""),
                "product_link": f"https://www.rappi.cl/tiendas/{product.get('store_id')}/producto/{product.get('product_id')}",
                "image": f"https://images.rappi.cl/products/{product.get('image')}.jpg" if product.get("image") else None,
                "price": product.get("price", 0),
                "promotion_price": product.get("real_price", product.get("price", 0)) if product.get("have_discount", False) else None,
                "promotion_details": self._get_promotion_details(product)
            }
            
            formatted_products.append(formatted_product)
        
        return formatted_products
    
    def _get_promotion_details(self, product: Dict) -> Optional[str]:
        """
        Extract promotion details from a product.
        
        Args:
            product: Product data dictionary.
        
        Returns:
            String with promotion details or None if no promotion.
        """
        # Check various promotion fields to construct a detail string
        if product.get("have_discount", False):
            discount_type = product.get("discount_type", "")
            discount = product.get("discount", 0)
            
            if discount_type and discount:
                return f"{discount_type} {discount}% off"
            
        # Check for bundle discounts
        if product.get("discounts_bundle", {}).get("deal"):
            deal = product.get("discounts_bundle", {}).get("deal", {})
            return f"Buy {deal.get('min_units')} get {deal.get('discount')}% off"
            
        # Check for step discounts
        if product.get("discount_step", {}).get("type"):
            step = product.get("discount_step", {})
            return f"Buy {step.get('min_units')} or more for {step.get('discount')}% off"
        
        return None
    
    def estimate_cookie_expiration(self, max_requests: int = 100, delay: int = 5) -> int:
        """
        Estimate how many requests can be made before cookies expire.
        
        Args:
            max_requests: Maximum number of requests to try.
            delay: Delay between requests in seconds.
        
        Returns:
            Number of successful requests before failure.
        """
        successful_requests = 0
        
        for i in range(max_requests):
            try:
                # Make a simple search request
                result = self.search_products("pan", "900020469")
                
                if not result:
                    print(f"Cookies expired after {successful_requests} requests")
                    return successful_requests
                
                successful_requests += 1
                print(f"Successfully made {successful_requests} requests")
                
                # Add delay to be respectful
                time.sleep(delay)
                
            except Exception as e:
                print(f"Error at request {successful_requests + 1}: {e}")
                return successful_requests
        
        return successful_requests


def main():
    """Main function to demonstrate the scraper."""
    # Initialize the proxy settings
    proxy = 'geo.iproyal.com:12321'
    proxy_auth = 'Qp2YvQ9hRCyienEj:GVPXaVCFvaFoMgZc_country-us'
    proxies = {
        'http': f'http://{proxy_auth}@{proxy}',
        'https': f'http://{proxy_auth}@{proxy}'
    }
    
    # Initialize the scraper
    scraper = RappiScraper(proxies)
    
    # Get user input for search term and store
    search_term = input("Enter search term: ")
    store_id = input("Enter store ID (default: 900020469 for Express Líder): ") or "900020469"
    
    # Search for products
    print(f"Searching for '{search_term}' in store {store_id}...")
    products = scraper.search_products(search_term, store_id)
    
    # Display results
    if products:
        print(f"Found {len(products)} products:")
        print(json.dumps(products, indent=2, ensure_ascii=False))
    else:
        print("No products found")


if __name__ == "__main__":
    main()