# Rappy Scraper Solution
* This applicaiton is developed with the assistance of Gemini 2.5

### Dependencies: Python Requests
  
### My journey
Initially I tried to directly access Rappi's product API but encountered authentication issues.

![alt text](image-1.png)

 After updated instructions, I discovered another approach by analyzing the network requests during product searches.

I noticed that the Rappi's webpage uses Next.js to embeds all product data directly in the script id "__NEXT_DATA__". This allowed me to extract structured JSON data directly without HTML parsing.

![alt text](image.png)


# Steps
1.  **Fetch Webpage:** Makes an HTTP GET request to the Rappi search results page URL for the given store ID(Default to Express Lide) and search term
2.  **Extract Embedded JSON:** Uses a regular expression to find the `<script id="__NEXT_DATA__">` tag in the HTML response and extracts its JSON content.
3.  **Parse JSON:** Loads the extracted JSON string into a Python dictionary/list (`json.loads`).
4.  **Locate Products:** Traverses the potentially nested JSON structure using helper functions (`_find_products`, `_traverse_dict`) to  find the list containing product data.
5.  **Format Data:** Iterates through the found products, extracting the required fields (`name`, `price`, `image`, `promotions`.)
6.  **Output:** Returns a list of product dictionaries and saves to `results.json`.


### Proxy Note: 
Somehow I coudn't connect to the proxy, so I added the option to default with not using it. This allowed the script to run without issues.

