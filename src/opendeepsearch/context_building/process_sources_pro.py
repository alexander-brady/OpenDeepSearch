from dataclasses import dataclass
from typing import List, Optional, Tuple
from src.opendeepsearch.context_scraping.crawl4ai_scraper import WebScraper
from src.opendeepsearch.ranking_models.infinity_rerank import SemanticSearcher
from src.opendeepsearch.ranking_models.chunker import Chunker 

@dataclass
class Source:
    link: str
    html: str = ""
    # Add other relevant fields here

class SourceProcessor:
    def __init__(
        self, 
        top_results: int = 5,
        strategies: List[str] = ["no_extraction"],
        filter_content: bool = True,
    ):
        self.strategies = strategies
        self.filter_content = filter_content
        self.scraper = WebScraper(
            strategies=self.strategies, 
            filter_content=self.filter_content
        )
        self.top_results = top_results
        self.chunker = Chunker()
        self.semantic_searcher = SemanticSearcher()

    async def process_sources(self, sources: List[dict], num_elements: int, query: str) -> List[dict]:
        try:
            valid_sources = self._get_valid_sources(sources, num_elements)
            if not valid_sources:
                return sources

            html_contents = await self._fetch_html_contents([s[1]['link'] for s in valid_sources])
            return self._update_sources_with_content(sources.data, valid_sources, html_contents, query)
        except Exception as e:
            print(f"Error in process_sources: {e}")
            return sources

    def _get_valid_sources(self, sources: List[dict], num_elements: int) -> List[Tuple[int, dict]]:
        return [(i, source) for i, source in enumerate(sources.data['organic'][:num_elements]) if source]

    async def _fetch_html_contents(self, links: List[str]) -> List[str]:
        raw_contents = await self.scraper.scrape_many(links)
        return [x['no_extraction'].content for x in raw_contents.values()]

    def _process_html_content(self, html: str, query: str) -> str:
        if not html:
            return ""
        try:
            # Split the HTML content into chunks
            documents = self.chunker.split_text(html)
            
            # Rerank the chunks based on the query
            reranked_content = self.semantic_searcher.get_reranked_documents(
                query,
                documents,
                top_k=self.top_results
            )
            
            return reranked_content
        
        except Exception as e:
            print(f"Error in content processing: {e}")
            return ""

    def _update_sources_with_content(
        self, 
        sources: List[dict],
        valid_sources: List[Tuple[int, dict]], 
        html_contents: List[str],
        query: str
    ) -> List[dict]:
        for (i, source), html in zip(valid_sources, html_contents):
            source['html'] = self._process_html_content(html, query)
            # sources[i] = source
        return sources