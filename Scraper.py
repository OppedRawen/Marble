import requests
import json
import re
from typing import Dict, List

class RappiScraper:
    def __init__(self, use_proxy=False):
       
        self.base_url = "https://www.rappi.cl/tiendas"
        self.session = requests.Session()
        
        # Basic headers
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        }
        
        # Proxy setup
        if use_proxy:
            proxy = 'geo.iproyal.com:12321'
            proxy_auth = 'Qp2YvQ9hRCyienEj:GVPXaVCFvaFoMgZc_country-us'
            self.proxies = {
                'http': f'http://{proxy_auth}@{proxy}',
                'https': f'http://{proxy_auth}@{proxy}'
            }
        else:
            self.proxies = None
    
    def search_products(self, query, store_id="900020469"):
        # Create search URL
        url = f"{self.base_url}/{store_id}-expresslider/s?term={query}"
        
        print(f"Searching for '{query}'...")
        
        try:
            # Get the search page
            response = self.session.get(
                url,
                headers=self.headers,
                proxies=self.proxies,
                timeout=15
            )
            
            if response.status_code != 200:
                print(f"Error: Status code {response.status_code}")
                return []
            
            # Extract the Next.js data - this is the key part that works
            next_data_match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', 
                                        response.text, re.DOTALL)
            if not next_data_match:
                print("No Next.js data found")
                return []
            
            # Parse the JSON data
            json_data = json.loads(next_data_match.group(1))
            
            # Find the products - using the traversal approach from the working version
            products = self._find_products(json_data)
            
            if not products:
                print("Could not find products in data")
                return []
            
            # Format products (simplified)
            result = []
            for product in products:
                if not product.get("name"):
                    continue
                
                # Extract the product ID
                product_id = product.get("id", "")
                
                # Extract the image URL
                image_url = product.get("image", "")
                
                # Extract prices
                price = product.get("price", 0)
                
                # Extract promotion details
                promo_price = None
                promo_details = None
                if product.get("have_discount", False):
                    promo_price = product.get("discountPrice")
                    discount = product.get("discount", 0)
                    if discount:
                        promo_details = f"{discount}% off"
                
                result.append({
                    "name": product.get("name", ""),
                    "product_link": f"https://www.rappi.cl/tiendas/{store_id}/producto/{product_id}",
                    "image": image_url,
                    "price": price,
                    "promotion_price": promo_price,
                    "promotion_details": promo_details
                })
            
            return result
                
        except requests.exceptions.ProxyError:
            # Try again without proxy if proxy fails
            if self.proxies:
                print("Proxy error. Retrying without proxy...")
                self.proxies = None
                return self.search_products(query, store_id)
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def _find_products(self, data):
        """
        Find products array in the JSON data by trying various paths
        and traversing nested structures.
        """
        products = None
        
        # Try common paths first
        if "pageProps" in data and "props" in data["pageProps"]:
            props = data["pageProps"]["props"]
            products = props.get("products") or props.get("items") or props.get("results")
        
        if not products and "products" in data:
            products = data["products"]
            
        if not products and "state" in data:
            state = data["state"]
            products = state.get("products") or state.get("searchResults")
            
        # If no products found yet, try recursive traversal (simplified)
        if not products:
            for path, value in self._traverse_dict(data):
                if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                    # Check if this looks like a product array
                    if "name" in value[0] and ("price" in value[0] or "prices" in value[0]):
                        products = value
                        print(f"Found products at: {path}")
                        break
        
        return products
    
    def _traverse_dict(self, d, path=""):
        """
        Simplified dictionary traversal to find nested values
        """
        if isinstance(d, dict):
            for key, value in d.items():
                new_path = f"{path}.{key}" if path else key
                yield (new_path, value)
                
                # Recursively traverse nested structures
                if isinstance(value, (dict, list)):
                    yield from self._traverse_dict(value, new_path)
        
        elif isinstance(d, list):
            for i, item in enumerate(d):
                new_path = f"{path}[{i}]"
                if isinstance(item, (dict, list)):
                    yield from self._traverse_dict(item, new_path)

def main():
    # Simple menu
    use_proxy = input("Use proxy? (y/n): ").lower() == 'y'
    scraper = RappiScraper(use_proxy=use_proxy)
    
    # Get search term
    search_term = input("Enter search term: ")
    store_id = input("Enter store ID (default: 900020469): ") or "900020469"
    
    # Do the search
    products = scraper.search_products(search_term, store_id)
    
    # Show results
    if products:
        print(f"Found {len(products)} products")
        # Show first 3 only
        print(json.dumps(products[:3], indent=2))
        
        # Save all to file
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        print(f"All results saved to results.json")
    else:
        print("No products found")

if __name__ == "__main__":
    main()