import os
import json
import aiohttp
from typing import Optional, Dict, Any

MAX_CONTENT_LENGTH = 5000

class WebTools:
    def __init__(self):
        self.search_cache = {}
    
    async def search_web(self, query: str) -> str:
        """Search the web for information using DuckDuckGo"""
        try:
            search_url = f"https://duckduckgo.com/?q={query}&format=json"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        
                        results = data.get("Results", [])
                        if not results:
                            results = data.get("RelatedTopics", [])[:5]
                        
                        if results:
                            formatted = [f"{i+1}. {r.get('Text', r.get('Name', ''))} - {r.get('FirstURL', '')}" 
                                        for i, r in enumerate(results[:5])]
                            return f"Search results for '{query}':\n" + "\n".join(formatted)
                        
                        return f"No results found for '{query}'"
                    
        except Exception as e:
            return f"Search for '{query}' - Note: Search functionality limited. Try using fetch_content with specific URLs."
    
    async def fetch_content(self, url: str, max_length: int = MAX_CONTENT_LENGTH) -> str:
        """Fetch content from a URL"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    if resp.status == 200:
                        content = await resp.text()
                        
                        if len(content) > max_length:
                            content = content[:max_length] + f"\n\n... [truncated, total {len(content)} chars]"
                        
                        try:
                            json_data = json.loads(content)
                            return f"JSON Response:\n{json.dumps(json_data, indent=2)[:max_length]}"
                        except:
                            import re
                            content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
                            content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
                            content = re.sub(r'<[^>]+>', '', content)
                            content = re.sub(r'\s+', ' ', content).strip()
                            
                            return f"Content from {url}:\n{content[:max_length]}"
                    
                    else:
                        return f"Error fetching {url}: HTTP {resp.status}"
                        
        except Exception as e:
            return f"Error fetching {url}: {str(e)}"
    
    async def call_api(self, url: str, method: str = "GET", headers: Optional[Dict] = None, body: Optional[Dict] = None) -> str:
        """Call any REST API endpoint"""
        try:
            default_headers = {
                "User-Agent": "DevMate/1.0",
                "Accept": "application/json"
            }
            
            if headers:
                default_headers.update(headers)
            
            async with aiohttp.ClientSession() as session:
                if method.upper() == "GET":
                    async with session.get(url, headers=default_headers, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                        content = await resp.text()
                elif method.upper() == "POST":
                    async with session.post(url, json=body, headers=default_headers, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                        content = await resp.text()
                else:
                    return f"Unsupported method: {method}"
                
                try:
                    json_data = json.loads(content)
                    return f"API Response:\n{json.dumps(json_data, indent=2)[:5000]}"
                except:
                    return f"Response:\n{content[:5000]}"
                    
        except Exception as e:
            return f"API Error: {str(e)}"


web_tools = WebTools()
