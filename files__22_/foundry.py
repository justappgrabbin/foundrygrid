"""
FOUNDRY - The Component Registry & Knowledge Base

Central repository for:
- All 64 gates (complete data)
- All consciousness components
- User-uploaded knowledge (books, PDFs, documents)
- Generated content (glyphs)
- Pack definitions
- Community content

This is the REFLECTION LAYER - everything that EXISTS.
The Projector shows what's REFLECTED from here.
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
import shutil


class Foundry:
    """
    The central repository - holds all possible states and knowledge
    
    Structure:
    - Components (gates, dimensions, lines, etc.)
    - Knowledge (uploaded books, PDFs, documents)
    - Content (generated articles, meditations, etc.)
    - Packs (feature packs, upgrades)
    - Glyphs (cryptographic IDs for all content)
    """
    
    def __init__(self, base_path: str = "/home/claude/synthai/foundry"):
        self.base_path = base_path
        self.components_path = os.path.join(base_path, "components")
        self.knowledge_path = os.path.join(base_path, "knowledge")
        self.content_path = os.path.join(base_path, "content")
        self.packs_path = os.path.join(base_path, "packs")
        self.glyphs_path = os.path.join(base_path, "glyphs")
        
        # Initialize directories
        self._init_structure()
        
        # Load component registry
        self.components = self._load_components()
    
    def _init_structure(self):
        """Create foundry directory structure"""
        directories = [
            self.base_path,
            self.components_path,
            os.path.join(self.knowledge_path, "books"),
            os.path.join(self.knowledge_path, "pdfs"),
            os.path.join(self.knowledge_path, "documents"),
            os.path.join(self.knowledge_path, "user_uploads"),
            os.path.join(self.content_path, "generated"),
            os.path.join(self.content_path, "user_created"),
            os.path.join(self.packs_path, "official"),
            os.path.join(self.packs_path, "community"),
            self.glyphs_path
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def _load_components(self) -> Dict:
        """Load component registry"""
        components_file = os.path.join(self.components_path, "registry.json")
        
        if os.path.exists(components_file):
            with open(components_file, 'r') as f:
                return json.load(f)
        
        # Initialize with basic structure
        return {
            'gates': {},
            'dimensions': {},
            'lines': {},
            'colors': {},
            'tones': {},
            'bases': {}
        }
    
    def _save_components(self):
        """Save component registry"""
        components_file = os.path.join(self.components_path, "registry.json")
        with open(components_file, 'w') as f:
            json.dump(self.components, f, indent=2)
    
    def generate_glyph(self, content: str, metadata: Dict = None) -> str:
        """
        Generate cryptographic glyph ID for content
        
        Uses SHA256 hash of content + metadata
        Returns 16-character hex string
        """
        glyph_input = content
        if metadata:
            glyph_input += json.dumps(metadata, sort_keys=True)
        
        hash_obj = hashlib.sha256(glyph_input.encode())
        glyph = hash_obj.hexdigest()[:16]
        
        return glyph
    
    def store_knowledge(self, file_path: str, category: str = "books",
                       metadata: Dict = None) -> Dict:
        """
        Store uploaded knowledge file
        
        Args:
            file_path: Path to file to upload
            category: 'books', 'pdfs', 'documents', 'user_uploads'
            metadata: Optional metadata (title, author, tags, etc.)
            
        Returns:
            {
                'glyph': str,
                'path': str,
                'category': str,
                'metadata': dict,
                'timestamp': str
            }
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read file content for glyph
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Generate glyph
        glyph = self.generate_glyph(content.hex(), metadata)
        
        # Determine storage path
        filename = os.path.basename(file_path)
        storage_dir = os.path.join(self.knowledge_path, category)
        storage_path = os.path.join(storage_dir, f"{glyph}_{filename}")
        
        # Copy file
        shutil.copy2(file_path, storage_path)
        
        # Create metadata file
        meta_path = storage_path + ".meta.json"
        full_metadata = {
            'glyph': glyph,
            'original_filename': filename,
            'category': category,
            'size_bytes': os.path.getsize(storage_path),
            'uploaded': datetime.now().isoformat(),
            'user_metadata': metadata or {}
        }
        
        with open(meta_path, 'w') as f:
            json.dump(full_metadata, f, indent=2)
        
        # Register glyph
        self._register_glyph(glyph, 'knowledge', storage_path, full_metadata)
        
        return full_metadata
    
    def store_generated_content(self, content: str, content_type: str,
                                coordinate: str = None, 
                                metadata: Dict = None) -> Dict:
        """
        Store AI-generated content with glyph
        
        Args:
            content: The generated content (text, markdown, etc.)
            content_type: 'article', 'meditation', 'workout', etc.
            coordinate: Optional consciousness coordinate
            metadata: Optional metadata
            
        Returns:
            {
                'glyph': str,
                'path': str,
                'content_type': str,
                'coordinate': str,
                'metadata': dict
            }
        """
        # Generate glyph
        meta = metadata or {}
        if coordinate:
            meta['coordinate'] = coordinate
        meta['content_type'] = content_type
        
        glyph = self.generate_glyph(content, meta)
        
        # Storage path
        storage_dir = os.path.join(self.content_path, "generated", content_type)
        os.makedirs(storage_dir, exist_ok=True)
        
        storage_path = os.path.join(storage_dir, f"{glyph}.txt")
        
        # Save content
        with open(storage_path, 'w') as f:
            f.write(content)
        
        # Save metadata
        meta_path = storage_path + ".meta.json"
        full_metadata = {
            'glyph': glyph,
            'content_type': content_type,
            'coordinate': coordinate,
            'generated': datetime.now().isoformat(),
            'user_metadata': meta
        }
        
        with open(meta_path, 'w') as f:
            json.dump(full_metadata, f, indent=2)
        
        # Register glyph
        self._register_glyph(glyph, 'content', storage_path, full_metadata)
        
        return full_metadata
    
    def store_pack(self, pack_definition: Dict, pack_type: str = "community") -> Dict:
        """
        Store a pack definition
        
        Args:
            pack_definition: {
                'name': str,
                'version': str,
                'description': str,
                'author': str,
                'price': float (0 for free),
                'files': [list of file paths],
                'dependencies': [list of required packs],
                'features': [list of features]
            }
            pack_type: 'official' or 'community'
            
        Returns:
            Pack metadata with glyph
        """
        # Generate glyph from pack definition
        glyph = self.generate_glyph(json.dumps(pack_definition, sort_keys=True))
        
        # Storage directory
        storage_dir = os.path.join(self.packs_path, pack_type)
        pack_dir = os.path.join(storage_dir, glyph)
        os.makedirs(pack_dir, exist_ok=True)
        
        # Save pack definition
        definition_path = os.path.join(pack_dir, "pack.json")
        full_definition = {
            **pack_definition,
            'glyph': glyph,
            'pack_type': pack_type,
            'created': datetime.now().isoformat()
        }
        
        with open(definition_path, 'w') as f:
            json.dump(full_definition, f, indent=2)
        
        # Copy pack files if provided
        if 'files' in pack_definition:
            files_dir = os.path.join(pack_dir, "files")
            os.makedirs(files_dir, exist_ok=True)
            
            for file_path in pack_definition['files']:
                if os.path.exists(file_path):
                    filename = os.path.basename(file_path)
                    shutil.copy2(file_path, os.path.join(files_dir, filename))
        
        # Register glyph
        self._register_glyph(glyph, 'pack', definition_path, full_definition)
        
        return full_definition
    
    def _register_glyph(self, glyph: str, content_type: str, 
                       path: str, metadata: Dict):
        """Register glyph in central index"""
        index_path = os.path.join(self.glyphs_path, "index.json")
        
        # Load existing index
        if os.path.exists(index_path):
            with open(index_path, 'r') as f:
                index = json.load(f)
        else:
            index = {}
        
        # Add entry
        index[glyph] = {
            'type': content_type,
            'path': path,
            'metadata': metadata,
            'registered': datetime.now().isoformat()
        }
        
        # Save index
        with open(index_path, 'w') as f:
            json.dump(index, f, indent=2)
    
    def retrieve_by_glyph(self, glyph: str) -> Optional[Dict]:
        """Retrieve content by glyph ID"""
        index_path = os.path.join(self.glyphs_path, "index.json")
        
        if not os.path.exists(index_path):
            return None
        
        with open(index_path, 'r') as f:
            index = json.load(f)
        
        if glyph not in index:
            return None
        
        entry = index[glyph]
        
        # Load content
        if os.path.exists(entry['path']):
            with open(entry['path'], 'r') as f:
                content = f.read()
            
            return {
                **entry,
                'content': content
            }
        
        return entry
    
    def search_knowledge(self, query: str = None, category: str = None,
                        tags: List[str] = None) -> List[Dict]:
        """
        Search knowledge base
        
        Args:
            query: Text search query
            category: Filter by category
            tags: Filter by tags
            
        Returns:
            List of matching items with metadata
        """
        results = []
        
        # Search directory
        search_dirs = []
        if category:
            search_dirs.append(os.path.join(self.knowledge_path, category))
        else:
            for cat in ['books', 'pdfs', 'documents', 'user_uploads']:
                search_dirs.append(os.path.join(self.knowledge_path, cat))
        
        # Find all metadata files
        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue
            
            for filename in os.listdir(search_dir):
                if filename.endswith('.meta.json'):
                    meta_path = os.path.join(search_dir, filename)
                    
                    with open(meta_path, 'r') as f:
                        metadata = json.load(f)
                    
                    # Apply filters
                    if query:
                        # Simple text matching
                        search_text = json.dumps(metadata).lower()
                        if query.lower() not in search_text:
                            continue
                    
                    if tags:
                        item_tags = metadata.get('user_metadata', {}).get('tags', [])
                        if not any(tag in item_tags for tag in tags):
                            continue
                    
                    results.append(metadata)
        
        return results
    
    def list_packs(self, pack_type: str = None) -> List[Dict]:
        """
        List available packs
        
        Args:
            pack_type: Filter by 'official' or 'community'
            
        Returns:
            List of pack definitions
        """
        packs = []
        
        # Search directories
        search_dirs = []
        if pack_type:
            search_dirs.append(os.path.join(self.packs_path, pack_type))
        else:
            search_dirs.append(os.path.join(self.packs_path, "official"))
            search_dirs.append(os.path.join(self.packs_path, "community"))
        
        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue
            
            for pack_glyph in os.listdir(search_dir):
                pack_file = os.path.join(search_dir, pack_glyph, "pack.json")
                
                if os.path.exists(pack_file):
                    with open(pack_file, 'r') as f:
                        pack_def = json.load(f)
                    packs.append(pack_def)
        
        return packs
    
    def reflect(self, coordinate: str) -> Dict:
        """
        Reflect all components for a consciousness coordinate
        
        This is the main query method - given a coordinate,
        return all relevant gates, dimensions, content, etc.
        """
        parts = coordinate.split('.')
        gate = int(parts[0])
        line = int(parts[1]) if len(parts) > 1 else 1
        color = int(parts[2]) if len(parts) > 2 else 1
        tone = int(parts[3]) if len(parts) > 3 else 1
        base = int(parts[4]) if len(parts) > 4 else 1
        
        reflection = {
            'coordinate': coordinate,
            'gate': self.components['gates'].get(str(gate), {}),
            'line': self.components['lines'].get(str(line), {}),
            'color': self.components['colors'].get(str(color), {}),
            'tone': self.components['tones'].get(str(tone), {}),
            'base': self.components['bases'].get(str(base), {}),
            'related_content': self._find_related_content(coordinate),
            'related_knowledge': self._find_related_knowledge(coordinate)
        }
        
        return reflection
    
    def _find_related_content(self, coordinate: str) -> List[Dict]:
        """Find generated content for this coordinate"""
        results = []
        
        content_dir = os.path.join(self.content_path, "generated")
        
        for content_type in os.listdir(content_dir):
            type_dir = os.path.join(content_dir, content_type)
            
            if not os.path.isdir(type_dir):
                continue
            
            for filename in os.listdir(type_dir):
                if filename.endswith('.meta.json'):
                    meta_path = os.path.join(type_dir, filename)
                    
                    with open(meta_path, 'r') as f:
                        metadata = json.load(f)
                    
                    if metadata.get('coordinate') == coordinate:
                        results.append(metadata)
        
        return results
    
    def _find_related_knowledge(self, coordinate: str) -> List[Dict]:
        """Find knowledge tagged with this coordinate"""
        # For now, return empty - can add coordinate tagging later
        return []


# Helper functions
def upload_knowledge(file_path: str, title: str = None, 
                    author: str = None, tags: List[str] = None,
                    category: str = "user_uploads") -> Dict:
    """
    Quick function to upload knowledge to Foundry
    
    Example:
        result = upload_knowledge(
            "path/to/book.pdf",
            title="Human Design: The Definitive Book",
            author="Ra Uru Hu",
            tags=["human design", "gates", "centers"]
        )
        
        print(f"Uploaded with glyph: {result['glyph']}")
    """
    foundry = Foundry()
    
    metadata = {}
    if title:
        metadata['title'] = title
    if author:
        metadata['author'] = author
    if tags:
        metadata['tags'] = tags
    
    return foundry.store_knowledge(file_path, category, metadata)


def create_pack(name: str, description: str, author: str,
               files: List[str] = None, price: float = 0.0) -> Dict:
    """
    Quick function to create a pack
    
    Example:
        pack = create_pack(
            name="Meditation Pack",
            description="10 guided meditations for each gate",
            author="Your Name",
            files=["meditation1.mp3", "meditation2.mp3"],
            price=4.99
        )
    """
    foundry = Foundry()
    
    pack_def = {
        'name': name,
        'version': '1.0.0',
        'description': description,
        'author': author,
        'price': price,
        'files': files or [],
        'dependencies': [],
        'features': []
    }
    
    return foundry.store_pack(pack_def, 'community')
