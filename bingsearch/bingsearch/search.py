from time import sleep
from bs4 import BeautifulSoup
from requests import get
from urllib.parse import unquote
from requests.exceptions import RequestException
from .user_agents import USER_AGENTS
import random
from .exceptions import BingSearchError

class SearchResult:
    """搜索结果容器"""
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url!r}, title={self.title!r}, description={self.description!r})"

def _random_ua():
    """随机获取User-Agent"""
    return random.choice(USER_AGENTS)

def _req(term, results, lang, start, proxies, timeout, ssl_verify):
    try:
        resp = get(
            url="https://www.bing.com/search",
            headers={"User-Agent": _random_ua()},
            params={
                "q": term,
                "count": results,
                "setlang": lang,
                "first": start,
            },
            proxies=proxies,
            timeout=timeout,
            verify=ssl_verify,
        )
        resp.raise_for_status()
        return resp
    except RequestException as e:
        raise BingSearchError(f"Request failed: {str(e)}") from e

def search(
    term: str,
    num_results: int = 10,
    lang: str = "en",
    proxy: str = None,
    sleep_interval: float = 0,
    timeout: int = 5,
    ssl_verify: bool = True,
    start_num: int = 0,
    unique: bool = False
) -> list[SearchResult]:
    """Bing搜索引擎查询
    
    Args:
        term: 搜索关键词
        num_results: 需要获取的结果数量
        lang: 语言设置 (默认en)
        proxy: 代理服务器地址 (例如 http://127.0.0.1:7890)
        sleep_interval: 请求间隔秒数 (防止被封禁)
        timeout: 请求超时秒数
        ssl_verify: 是否验证SSL证书
        start_num: 起始结果序号
        unique: 是否过滤重复链接
    
    Returns:
        SearchResult对象列表
    """
    proxies = {"http": proxy, "https": proxy} if proxy else None
    fetched_links = set()
    results = []
    
    while len(results) < num_results:
        try:
            resp = _req(term, num_results - len(results), lang, 
                       start_num, proxies, timeout, ssl_verify)
        except BingSearchError as e:
            if "429" in str(e):  # 处理速率限制
                sleep(5)
                continue
            raise
        
        soup = BeautifulSoup(resp.text, "html.parser")
        result_block = soup.find_all("li", class_="b_algo")
        
        for result in result_block:
            try:
                link = result.find("a")["href"]
                title = result.find("h2").get_text(strip=True)
                desc = result.find("p").get_text(strip=True) if result.find("p") else ""
                
                if unique and link in fetched_links:
                    continue
                
                fetched_links.add(link)
                results.append(SearchResult(
                    url=unquote(link),
                    title=title,
                    description=desc
                ))
                
                if len(results) >= num_results:
                    break
            
            except (AttributeError, KeyError):
                continue
        
        if not result_block:  # 没有更多结果
            break
        
        start_num += len(result_block)
        sleep(sleep_interval)
    
    return results[:num_results]
