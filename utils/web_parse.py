import asyncio
import aiohttp
import trafilatura
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

"""
add more package for web parsing
in case of trafilatura is not working
which seems failed a lot of times
"""
async def fetch_html(session, url):
    """
    Fetch HTML content from a URL.
    
    Args:
        session: aiohttp client session
        url: Target URL to fetch
        
    Returns:
        HTML content as string or None if failed
    """
    try:
        async with session.get(url, timeout=30) as response:
            if response.status != 200:
                logger.error(f"Failed to fetch {url}: HTTP {response.status}")
                return None
                
            logger.debug(f"Successfully fetched {url}")
            html = await response.text()
            return html
    except aiohttp.ClientError as e:
        logger.error(f"Connection error for {url}: {str(e)}")
        return None
    except asyncio.TimeoutError:
        logger.error(f"Request timed out for {url}")
        return None
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {str(e)}")
        return None

async def fetch_and_extract(urls):
    """
    Fetch HTML from multiple URLs and extract main text content.
    
    Args:
        urls: List of URLs to process
        
    Returns:
        List of extracted text contents, None for failed extractions
    """
    if not urls:
        logger.warning("No URLs provided for extraction")
        return []
        
    logger.info(f"Starting to fetch and extract content from {len(urls)} URLs")
    
    async with aiohttp.ClientSession() as session:
        # Concurrently execute all URL fetch tasks
        tasks = [fetch_html(session, url) for url in urls if url != "" and url != None]
        html_contents = await asyncio.gather(*tasks)
    
    extracted_texts = []
    success_count = 0
    
    for url, html in zip(urls, html_contents):
        if html is None:
            logger.warning(f"No HTML content available for {url}")
            extracted_texts.append(None)
            continue
            
        # Use trafilatura.extract to extract main text content
        try:
            text = trafilatura.extract(html)
            if text is None:
                logger.warning(f"Content extraction failed for {url}")
                extracted_texts.append(None)
            else:
                success_count += 1
                logger.debug(f"Successfully extracted {len(text)} characters from {url}")
                extracted_texts.append(text)
        except Exception as e:
            logger.error(f"Error during content extraction for {url}: {str(e)}")
            extracted_texts.append(None)
    
    logger.info(f"Completed extraction: {success_count} successful, {len(urls) - success_count} failed")
    return extracted_texts

