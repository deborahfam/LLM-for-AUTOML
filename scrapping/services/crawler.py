from typing import Set, List, Tuple
from bs4 import BeautifulSoup, Tag
import requests
import hashlib
import streamlit as st
from config import collection, db

class CrawlerService:
    def __init__(self, database_service, text_processor, max_links_per_page=2):
        self.visited: Set[str] = set()
        self.db_service = database_service
        self.text_processor = text_processor
        self.max_links_per_page = max_links_per_page
        self._init_ui()

    def _init_ui(self):
        st.header("Proceso de Web Crawling")
        self.status_bar = st.empty()
        self.progress_bar = st.progress(0)
        self.log_container = st.container()

    def crawl(self, start_url: str, max_depth: int):
        queue = [(start_url, 0)]
        total_processed = 0
        
        with st.expander("Detalles de Ejecución", expanded=True):
            while queue:
                url, depth = queue.pop(0)
                total_processed += 1
                self.progress_bar.progress(min(total_processed * 10, 100))
                self._process_url(url, depth, max_depth, queue)

    def _process_url(self, url: str, depth: int, max_depth: int, queue: list):
        try:
            self._update_status(f"Procesando: {url} (Profundidad {depth})")
            
            if self._should_skip_url(url, depth, max_depth):
                return

            response = self._fetch_url(url)
            soup = self._parse_html(response)
            raw_text = self._extract_main_content(soup)
            chunks, embeddings = self._process_text(raw_text)
            self._handle_chunks(url, chunks, embeddings)
            self._queue_child_links(soup, queue, depth)
            self.visited.add(url)
            st.success(f"Proceso completado: {url}")

        except Exception as e:
            self._handle_error(url, e)

    # Métodos auxiliares
    def _update_status(self, message: str, level: str = "info"):
        log_method = {
            "error": st.error,
            "warning": st.warning,
            "info": st.info
        }.get(level, st.info)
        
        with self.log_container:
            log_method(f"{'⛔' if level == 'error' else 'ℹ️'} {message}")

    def _should_skip_url(self, url: str, depth: int, max_depth: int) -> bool:
        if depth > max_depth:
            self._update_status(f"Profundidad máxima alcanzada", "warning")
            return True
        if url in self.visited:
            self._update_status(f"URL ya visitada", "warning")
            return True
        return False

    def _fetch_url(self, url: str) -> requests.Response:
        try:
            response = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
            self._update_status(f"Estado HTTP: {response.status_code}")
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise Exception(f"Error HTTP: {str(e)}") from e

    def _parse_html(self, response: requests.Response) -> BeautifulSoup:
        try:
            response.encoding = response.apparent_encoding or 'utf-8'
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            raise Exception(f"Error parseando HTML: {str(e)}") from e

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        try:
            main_content = soup.find('div', {'class': 'body'}) or soup
            elements_to_remove = ['script', 'style', 'noscript', 'meta', 'link', 'head', 'title']
            for tag in elements_to_remove:
                for element in main_content.find_all(tag):
                    element.decompose()
            return main_content.get_text(separator=' ', strip=True)
        except Exception as e:
            raise Exception(f"Error limpiando contenido: {str(e)}") from e

    def _process_text(self, raw_text: str) -> Tuple[List[str], List[List[float]]]:
        try:
            chunks, embeddings = self.text_processor.process_text(raw_text)
            self._update_status(f"Texto dividido en {len(chunks)} fragmentos")
            return chunks, embeddings
        except Exception as e:
            raise Exception(f"Error procesando texto: {str(e)}") from e

    def _handle_chunks(self, url: str, chunks: List[str], embeddings: List[List[float]]):
        saved = 0
        for chunk, embedding in zip(chunks, embeddings):
            try:
                # hash_code = hashlib.sha256(chunk.encode()).hexdigest()
                # if not self.db_service.is_duplicate(hash_code):
                self.db_service.save_document(
                        url=url,
                        chunk_text=chunk.page_content,
                        embedding=embedding,
                        # hash_code=hash_code
                    )
                saved += 1
            except Exception as e:
                self._update_status(f"Error guardando chunk: {str(e)}", "error")
        
        st.metric("Chunks guardados exitosamente", saved)

    def _queue_child_links(self, soup: BeautifulSoup, queue: list, depth: int) -> int:
        try:
            new_links = 0
            for link in soup.find_all('a', href=True):
                if new_links >= self.max_links_per_page:
                    break
                
                url = link['href']
                if url.startswith('http') and url not in self.visited:
                    queue.append((url, depth + 1))
                    new_links += 1
            return new_links
        except Exception as e:
            raise Exception(f"Error procesando enlaces: {str(e)}") from e

    def _handle_error(self, url: str, error: Exception):
        error_msg = f"{type(error).__name__}: {str(error)}"
        self._update_status(f"Error en {url}: {error_msg}", "error")
        self._log_error(url, error_msg)
        st.experimental_rerun()

    def _log_error(self, url: str, error: str):
        with open("crawler_errors.log", "a", encoding='utf-8') as f:
            f.write(f"{url} - {error}\n")