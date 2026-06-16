"""File AI service — extract text from files and process with LLM."""

from pathlib import Path
from typing import Optional

import litellm
from loguru import logger


class FileService:

    @classmethod
    async def process(
        cls,
        file_path: Path,
        action: str,
        target_language: Optional[str] = None,
        output_format: Optional[str] = None,
        custom_prompt: Optional[str] = None,
    ) -> dict:
        """Extract text from file, then apply AI action."""
        text = cls._extract_text(file_path)
        if not text:
            return {"error": "Could not extract text from file", "tokens_used": 0}

        # Truncate to ~8000 chars to stay within token limits
        if len(text) > 8000:
            text = text[:8000] + "\n\n[... content truncated ...]"

        prompt = cls._build_prompt(action, text, target_language, output_format, custom_prompt)

        try:
            resp = await litellm.acompletion(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048,
            )
            result_text = resp.choices[0].message.content or ""
            tokens = getattr(resp.usage, "total_tokens", 0) if resp.usage else 0
            return {"output": result_text, "tokens_used": tokens, "chars_processed": len(text)}
        except Exception as e:
            logger.warning(f"File AI processing failed: {e}")
            return {"output": f"Processing error: {e}", "tokens_used": 0}

    @staticmethod
    def _extract_text(file_path: Path) -> str:
        """Extract plain text from various file formats."""
        ext = file_path.suffix.lower()

        if ext == ".txt" or ext == ".md":
            return file_path.read_text(encoding="utf-8", errors="ignore")

        elif ext == ".pdf":
            try:
                import PyPDF2
                reader = PyPDF2.PdfReader(str(file_path))
                return "\n".join(p.extract_text() or "" for p in reader.pages)
            except ImportError:
                return "[PDF processing requires PyPDF2]"

        elif ext == ".docx":
            try:
                from docx import Document
                doc = Document(str(file_path))
                return "\n".join(p.text for p in doc.paragraphs)
            except ImportError:
                return "[DOCX processing requires python-docx]"

        elif ext == ".csv":
            try:
                import pandas as pd
                df = pd.read_csv(file_path)
                return df.head(100).to_string()
            except ImportError:
                return file_path.read_text(encoding="utf-8", errors="ignore")

        elif ext in (".xlsx", ".xls"):
            try:
                import pandas as pd
                df = pd.read_excel(file_path)
                return df.head(100).to_string()
            except ImportError:
                return "[Excel processing requires openpyxl + pandas]"

        elif ext == ".json":
            return file_path.read_text(encoding="utf-8", errors="ignore")

        return file_path.read_text(encoding="utf-8", errors="ignore")

    @staticmethod
    def _build_prompt(
        action: str,
        text: str,
        target_language: Optional[str],
        output_format: Optional[str],
        custom_prompt: Optional[str],
    ) -> str:
        if custom_prompt:
            return f"{custom_prompt}\n\nDocument content:\n{text}"

        prompts = {
            "summarize": f"Provide a concise, well-structured summary of the following document:\n\n{text}",
            "analyze": f"Analyze the following document. Identify key themes, insights, and important points:\n\n{text}",
            "extract": f"Extract all key information, facts, figures, names, and data from this document. Format as structured bullet points:\n\n{text}",
            "translate": f"Translate the following document to {target_language or 'English'}:\n\n{text}",
            "convert": f"Convert the following content to {output_format or 'Markdown'} format:\n\n{text}",
        }
        return prompts.get(action, f"Process this document:\n\n{text}")
