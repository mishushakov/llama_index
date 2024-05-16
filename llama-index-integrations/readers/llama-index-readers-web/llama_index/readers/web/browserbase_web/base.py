import os
import logging
from typing import List
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document


logger = logging.getLogger(__name__)


class BrowserbaseWebReader(BaseReader):
    """Browserbase Web Reader"""

    def __init__(
        self, api_key: Optional[str] = None, project_id: Optional[str] = None
    ) -> None:
        try:
            from browserbase import Browserbase
        except ImportError:
            raise ImportError(
                "`browserbase` package not found, please run `pip install browserbase`"
            )

        self.browserbase = Browserbase(api_key, project_id)

    def load_data(
        self,
        urls: Sequence[str],
        text_content: bool = False,
        session_id: Optional[str] = None,
        proxy: Optional[bool] = None,
    ) -> List[Document]:
        """Load pages using Browserbase Web Reader"""

        pages = self.browserbase.load_urls(
            urls,
            text_content,
            session_id,
            proxy,
        )

        documents = []
        for i, page in enumerate(pages):
            documents.append(
                Document(
                    text=page,
                    metadata={
                        "url": urls[i],
                    },
                )
            )

        return documents


if __name__ == "__main__":
    reader = BrowserbaseWebReader()
    logger.info(reader.load_data(urls=["https://example.com"]))
