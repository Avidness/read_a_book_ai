from typing import List, Dict, Any, Optional
from app.services.pinecone.pinecone_adapter import PineconeAdapter
from app.models.chapter import Chapter
from dotenv import load_dotenv
import os

class ChapterAdapter(PineconeAdapter):
    def __init__(self, index_name: str = 'chapters-index', namespace: str = 'chapters') -> None:
        print("1. Loading environment variables...")
        load_dotenv()
        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        
        if not PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY not found in environment variables")
            
        super().__init__(index_name=index_name, namespace=namespace)
        self.create_index()

    def prepare_chapter_data(self, chapter: Chapter) -> Dict[str, Any]:
        """
        Prepares a chapter for insertion into Pinecone by converting it to the required format
        """
        return {
            'id': f'chapter_{chapter.chapter_id}',
            'text': chapter.chapter_summary,
            'metadata': {
                'name': chapter.chapter_name,
                'number': chapter.chapter_id,
                'summary': chapter.chapter_summary
            }
        }

    def upsert_chapters(self, chapters: List[Chapter]) -> None:
        """
        Upserts multiple chapters into the Pinecone index
        """
        prepared_data = [self.prepare_chapter_data(chapter) for chapter in chapters]
        self.upsert_data(prepared_data)

    def upsert_chapter(self, chapter: Chapter) -> None:
        """
        Upserts a single chapter into the Pinecone index
        """
        self.upsert_chapters([chapter])

    def search_chapters(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Searches for chapters based on their content
        Returns the top k most similar chapters
        """
        results = self.query_index(query, top_k=top_k)
        return results.matches

    def get_chapter_by_id(self, chapter_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves a specific chapter by its ID
        """
        index = self.get_index()
        results = index.fetch(ids=[f'chapter_{chapter_id}'], namespace=self.namespace)
        
        if not results.vectors:
            return None
            
        return next(iter(results.vectors.values()))
    
    def update_chapter(self, chapter: Chapter) -> None:
        """
        Updates an existing chapter in the index.
        This will overwrite the existing chapter data completely.
        """
        self.upsert_chapter(chapter)
        
    def update_chapter_partial(self, chapter_id: int, **updates: Dict[str, Any]) -> None:
        """
        Partially updates a chapter's metadata without changing the vector embedding
        if the summary hasn't changed.
        """
        existing_chapter = self.get_chapter_by_id(chapter_id)
        if not existing_chapter:
            raise ValueError(f"Chapter with ID {chapter_id} not found")
            
        current_metadata = existing_chapter['metadata']
        updated_chapter = Chapter(
            chapter_id=chapter_id,
            chapter_name=updates.get('chapter_name', current_metadata['name']),
            chapter_summary=updates.get('chapter_summary', current_metadata['summary'])
        )
        
        if 'chapter_summary' not in updates:
            index = self.get_index()
            prepared_data = self.prepare_chapter_data(updated_chapter)
            index.update(
                id=f'chapter_{chapter_id}',
                namespace=self.namespace,
                metadata=prepared_data['metadata']
            )
        else:
            self.upsert_chapter(updated_chapter)
            
    def delete_chapter(self, chapter_id: int) -> bool:
        """
        Deletes a single chapter from the index.
        """
        index = self.get_index()
        chapter_vector_id = f'chapter_{chapter_id}'
        
        if not self.get_chapter_by_id(chapter_id):
            return False
            
        index.delete(
            ids=[chapter_vector_id],
            namespace=self.namespace
        )
        return True
        
    def delete_chapters(self, chapter_ids: List[int]) -> Dict[int, bool]:
        """
        Deletes multiple chapters from the index.
        """
        index = self.get_index()
        vector_ids = [f'chapter_{chapter_id}' for chapter_id in chapter_ids]
        
        results = {}
        for chapter_id in chapter_ids:
            results[chapter_id] = self.get_chapter_by_id(chapter_id) is not None
            
        if any(results.values()):
            index.delete(
                ids=vector_ids,
                namespace=self.namespace
            )
            
        return results