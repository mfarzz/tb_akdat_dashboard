# -*- coding: utf-8 -*-
"""
DeepHoaxID Wrapper untuk PostgreSQL
Wrapper untuk menggantikan Firebase dengan PostgreSQL
"""

import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Add deephoaxid_detection to path
current_file = Path(__file__).resolve()
dashboard_root = current_file.parent.parent
project_root = dashboard_root.parent
deephoaxid_path = project_root / "tb_scrapping" / "deephoaxid_detection"

if deephoaxid_path.exists():
    sys.path.insert(0, str(deephoaxid_path))

# Import akan dilakukan secara lazy di dalam method untuk menghindari import firebase_admin
# Import hanya yang tidak memerlukan firebase_admin
try:
    # Import config dengan try-except untuk menghindari error jika ada masalah
    import importlib.util
    config_path = deephoaxid_path / "config.py"
    if config_path.exists():
        spec = importlib.util.spec_from_file_location("config", config_path)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)
        # Copy constants yang diperlukan
        SYSTEM_VERSION = getattr(config_module, 'SYSTEM_VERSION', '1.0.0')
        DEFAULT_TOP_K = getattr(config_module, 'DEFAULT_TOP_K', 3)
        DEFAULT_MIN_SIMILARITY = getattr(config_module, 'DEFAULT_MIN_SIMILARITY', 0.5)
        HIGH_CONFIDENCE_THRESHOLD = getattr(config_module, 'HIGH_CONFIDENCE_THRESHOLD', 0.8)
        MEDIUM_CONFIDENCE_THRESHOLD = getattr(config_module, 'MEDIUM_CONFIDENCE_THRESHOLD', 0.6)
        EMBEDDING_BATCH_SIZE = getattr(config_module, 'EMBEDDING_BATCH_SIZE', 32)
        MAX_TEXT_LENGTH = getattr(config_module, 'MAX_TEXT_LENGTH', 512)
        MODELS_DIR = getattr(config_module, 'MODELS_DIR', 'models')
        FAISS_INDEX_PATH = getattr(config_module, 'FAISS_INDEX_PATH', None)
        FAISS_METADATA_PATH = getattr(config_module, 'FAISS_METADATA_PATH', None)
    else:
        # Fallback values
        SYSTEM_VERSION = '1.0.0'
        DEFAULT_TOP_K = 3
        DEFAULT_MIN_SIMILARITY = 0.5
        HIGH_CONFIDENCE_THRESHOLD = 0.8
        MEDIUM_CONFIDENCE_THRESHOLD = 0.6
        EMBEDDING_BATCH_SIZE = 32
        MAX_TEXT_LENGTH = 512
        MODELS_DIR = 'models'
        FAISS_INDEX_PATH = None
        FAISS_METADATA_PATH = None
except Exception as e:
    logger.warning(f"Could not load config: {e}, using defaults")
    SYSTEM_VERSION = '1.0.0'
    DEFAULT_TOP_K = 3
    DEFAULT_MIN_SIMILARITY = 0.5
    HIGH_CONFIDENCE_THRESHOLD = 0.8
    MEDIUM_CONFIDENCE_THRESHOLD = 0.6
    EMBEDDING_BATCH_SIZE = 32
    MAX_TEXT_LENGTH = 512
    MODELS_DIR = 'models'
    FAISS_INDEX_PATH = None
    FAISS_METADATA_PATH = None

from helpers.postgres_db_adapter import PostgreSQLDatabaseAdapter

# Setup logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

class DeepHoaxIDPostgreSQLWrapper:
    """
    Wrapper untuk DeepHoaxIDSystem yang menggunakan PostgreSQL
    menggantikan Firebase DatabaseManager
    """
    
    def __init__(self):
        """Initialize sistem"""
        
        self.system_info = {
            'name': 'DeepHoaxID',
            'version': SYSTEM_VERSION,
            'competition': 'Gemastik 2025',
            'initialized': False,
            'components': {},
            'stats': {
                'messages_processed': 0,
                'hoax_detected': 0,
                'clean_detected': 0,
                'errors': 0
            }
        }
        
        # Components
        self.db_manager = None
        self.preprocessor = None
        self.similarity_engine = None
        self.chat_filter = None
        self.response_generator = None

        logger.info(f"🔧 Initializing {self.system_info['name']} v{self.system_info['version']} (PostgreSQL)")

    def initialize(self) -> bool:
        """
        Initialize sistem dengan PostgreSQL adapter
        Override method untuk menggunakan PostgreSQL
        """
        try:
            logger.info("🔧 Initializing system components with PostgreSQL...")
            
            # 1. Database Manager - Gunakan PostgreSQL adapter
            logger.info("📊 Initializing PostgreSQL Database Adapter...")
            self.db_manager = PostgreSQLDatabaseAdapter()
            health = self.db_manager.health_check()
            if not health['status'] == 'healthy':
                logger.error(f"❌ Database not healthy: {health}")
                return False
            self.system_info['components']['database'] = '✅ Connected (PostgreSQL)'
            logger.info(f"✅ PostgreSQL connected: {health.get('stats', {}).get('total_articles', 'unknown')} articles")
            
            # 2. Text Preprocessor (lazy import)
            logger.info("🔤 Initializing Text Preprocessor...")
            from text_preprocessor import TextPreprocessor
            self.preprocessor = TextPreprocessor()
            self.system_info['components']['preprocessor'] = '✅ Ready'
            logger.info("✅ Text Preprocessor ready")
            
            # 3. Chat Filter (lazy import)
            logger.info("🔍 Initializing Chat Filter...")
            from chat_filter import ChatFilter
            self.chat_filter = ChatFilter()
            filter_stats = self.chat_filter.get_filter_stats()
            self.system_info['components']['chat_filter'] = f"✅ Ready ({filter_stats['total_patterns']} patterns)"
            logger.info(f"✅ Chat Filter ready: {filter_stats['total_patterns']} patterns")
            
            # 4. Response Generator (lazy import)
            logger.info("💬 Initializing Response Generator...")
            from response_generator import ResponseGenerator
            self.response_generator = ResponseGenerator()
            resp_stats = self.response_generator.get_response_stats()
            self.system_info['components']['response_generator'] = f"✅ Ready ({resp_stats['total_templates']} templates)"
            logger.info(f"✅ Response Generator ready: {resp_stats['total_templates']} templates")
            
            # 5. Similarity Engine (lazy import)
            logger.info("🧠 Initializing Similarity Engine...")
            from similarity_engine import SimilarityEngine
            self.similarity_engine = SimilarityEngine()
            
            # Load atau create embeddings
            if self.similarity_engine.index_exists():
                logger.info("📂 Loading existing embeddings...")
                success = self.similarity_engine.load_index()
                if success:
                    stats = self.similarity_engine.get_index_stats()
                    self.system_info['components']['similarity_engine'] = f"✅ Loaded ({stats['total_embeddings']} embeddings)"
                    logger.info(f"✅ Similarity Engine loaded: {stats['total_embeddings']} embeddings")
                else:
                    logger.error("❌ Failed to load existing index")
                    return False
            else:
                logger.info("🏗️ Building new embeddings index...")
                df = self.db_manager.load_hoax_articles()
                if df.empty:
                    logger.error("❌ No articles found for building index")
                    return False
                
                # Convert DataFrame to list of dicts
                articles = df.to_dict('records')
                
                success = self.similarity_engine.build_index(articles)
                if success:
                    stats = self.similarity_engine.get_index_stats()
                    self.system_info['components']['similarity_engine'] = f"✅ Built ({stats['total_embeddings']} embeddings)"
                    logger.info(f"✅ Similarity Engine built: {stats['total_embeddings']} embeddings")
                else:
                    logger.error("❌ Failed to build similarity index")
                    return False
            
            self.system_info['initialized'] = True
            logger.info("🎉 System initialization completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def analyze_message(self, message_text: str, sender_info: Dict = None) -> Dict[str, any]:
        """
        Analyze single message untuk hoax detection
        
        Args:
            message_text: Text pesan yang akan dianalisis
            sender_info: Info pengirim (optional)
            
        Returns:
            Dict: Complete analysis result
        """
        start_time = time.time()
        
        try:
            if not self.system_info['initialized']:
                raise Exception("System not initialized. Call initialize() first.")
            
            logger.info(f"🔍 Analyzing message: {message_text[:50]}...")
            
            # 1. Chat Filter - Should we analyze?
            filter_result = self.chat_filter.should_analyze_message(message_text, sender_info)
            
            if not filter_result['should_analyze']:
                # Skip analysis
                result = {
                    'should_analyze': False,
                    'filter_result': filter_result,
                    'analysis_result': None,
                    'response': {
                        'text': "💬 Sepertinya ini chat biasa, tidak perlu dianalisis ya! 😊",
                        'category': 'CHAT_BIASA',
                        'confidence': 0.0
                    },
                    'processing_time': time.time() - start_time,
                    'timestamp': datetime.now().isoformat()
                }
                
                logger.info(f"⏭️ Skipped analysis: {filter_result['reason']}")
                return result
            
            # 2. Preprocessing
            processed_text = self.preprocessor.preprocess_for_similarity(message_text)
            if not processed_text:
                raise Exception("Preprocessed text is empty")
            
            # 3. Similarity Analysis
            similarity_result = self.similarity_engine.find_similar_articles(
                processed_text, 
                top_k=DEFAULT_TOP_K
            )
            
            # 4. Generate Response
            response = self.response_generator.generate_response(similarity_result)
            
            # 5. Compile results
            result = {
                'should_analyze': True,
                'filter_result': filter_result,
                'processed_text': processed_text[:200] + '...' if len(processed_text) > 200 else processed_text,
                'analysis_result': similarity_result,
                'response': response,
                'processing_time': time.time() - start_time,
                'timestamp': datetime.now().isoformat()
            }
            
            # Update stats
            self.system_info['stats']['messages_processed'] += 1
            if similarity_result['category'] in ['HOAX', 'SUSPICIOUS']:
                self.system_info['stats']['hoax_detected'] += 1
            else:
                self.system_info['stats']['clean_detected'] += 1
            
            logger.info(f"✅ Analysis completed: {similarity_result['category']} ({similarity_result['confidence']:.2f}) in {result['processing_time']:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"❌ Analysis error: {e}")
            
            # Error response
            error_result = {
                'should_analyze': True,
                'filter_result': {'should_analyze': True, 'reason': 'Error occurred'},
                'analysis_result': {'category': 'ERROR', 'confidence': 0.0, 'error': str(e)},
                'response': self.response_generator.generate_response({
                    'category': 'ERROR', 
                    'confidence': 0.0, 
                    'error': str(e)
                }) if self.response_generator else {
                    'text': f"❌ Error: {str(e)[:100]}",
                    'category': 'ERROR'
                },
                'processing_time': time.time() - start_time,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
            
            self.system_info['stats']['errors'] += 1
            return error_result
    
    def analyze_batch_messages(self, messages: List[str]) -> List[Dict]:
        """
        Analyze multiple messages
        
        Args:
            messages: List of message texts
            
        Returns:
            List[Dict]: Analysis results
        """
        logger.info(f"🔍 Analyzing batch of {len(messages)} messages...")
        
        results = []
        for i, message in enumerate(messages):
            logger.info(f"Processing message {i+1}/{len(messages)}")
            result = self.analyze_message(message)
            result['batch_index'] = i
            results.append(result)
        
        logger.info(f"✅ Batch analysis completed: {len(results)} results")
        return results
    
    def get_system_status(self) -> Dict[str, any]:
        """
        Get status sistem lengkap
        
        Returns:
            Dict: System status
        """
        status = {
            'system_info': self.system_info,
            'components_status': {},
            'performance': {},
            'timestamp': datetime.now().isoformat()
        }
        
        if self.system_info['initialized']:
            # Database status
            if self.db_manager:
                db_health = self.db_manager.health_check()
                status['components_status']['database'] = db_health
            
            # Similarity engine status
            if self.similarity_engine:
                engine_stats = self.similarity_engine.get_index_stats()
                status['components_status']['similarity_engine'] = engine_stats
            
            # Filter stats
            if self.chat_filter:
                filter_stats = self.chat_filter.get_filter_stats()
                status['components_status']['chat_filter'] = filter_stats
            
            # Response generator stats
            if self.response_generator:
                resp_stats = self.response_generator.get_response_stats()
                status['components_status']['response_generator'] = resp_stats
        
        return status

