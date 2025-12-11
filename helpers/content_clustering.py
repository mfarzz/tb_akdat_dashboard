# -*- coding: utf-8 -*-
"""
Content Clustering Helper
Menggunakan embeddings dari Sentence-BERT untuk clustering artikel
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional, Dict, List
import logging
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


def get_embeddings_for_articles(
    df: pd.DataFrame,
    similarity_engine,
    text_column: str = 'content',
    batch_size: int = 32
) -> Optional[np.ndarray]:
    """
    Mendapatkan embeddings untuk artikel menggunakan similarity engine
    
    Args:
        df: DataFrame dengan artikel
        similarity_engine: SimilarityEngine dari DeepHoaxID
        text_column: Kolom yang berisi teks artikel
        batch_size: Ukuran batch untuk encoding
    
    Returns:
        numpy array dengan embeddings atau None jika error
    """
    if similarity_engine is None or not hasattr(similarity_engine, 'sbert_model'):
        logger.error("Similarity engine tidak tersedia atau belum diinisialisasi")
        return None
    
    try:
        # Ambil teks dari dataframe
        texts = df[text_column].fillna("").astype(str).tolist()
        
        # Encode menggunakan Sentence-BERT
        embeddings = similarity_engine.sbert_model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        
        logger.info(f"Berhasil mendapatkan embeddings untuk {len(texts)} artikel")
        return embeddings
    
    except Exception as e:
        logger.error(f"Error saat mendapatkan embeddings: {e}")
        return None


def perform_clustering(
    embeddings: np.ndarray,
    n_clusters: int = 5,
    random_state: int = 42
) -> Tuple[np.ndarray, KMeans]:
    """
    Melakukan clustering menggunakan KMeans
    
    Args:
        embeddings: Array embeddings
        n_clusters: Jumlah cluster
        random_state: Random state untuk reproducibility
    
    Returns:
        Tuple (cluster_labels, kmeans_model)
    """
    try:
        # Standardize embeddings
        scaler = StandardScaler()
        embeddings_scaled = scaler.fit_transform(embeddings)
        
        # KMeans clustering
        kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
            n_init=10,
            max_iter=300
        )
        cluster_labels = kmeans.fit_predict(embeddings_scaled)
        
        logger.info(f"Clustering selesai: {n_clusters} cluster, {len(cluster_labels)} artikel")
        return cluster_labels, kmeans
    
    except Exception as e:
        logger.error(f"Error saat clustering: {e}")
        raise


def reduce_dimensions(
    embeddings: np.ndarray,
    method: str = 'pca',
    n_components: int = 2,
    random_state: int = 42
) -> np.ndarray:
    """
    Reduksi dimensi untuk visualisasi
    
    Args:
        embeddings: Array embeddings
        method: 'pca' atau 'tsne'
        n_components: Jumlah komponen (2 untuk 2D)
        random_state: Random state
    
    Returns:
        Array 2D untuk visualisasi
    """
    try:
        if method == 'pca':
            reducer = PCA(n_components=n_components, random_state=random_state)
            reduced = reducer.fit_transform(embeddings)
            logger.info(f"PCA selesai: explained variance ratio = {reducer.explained_variance_ratio_.sum():.2%}")
            return reduced
        
        elif method == 'tsne':
            # t-SNE lebih lambat tapi lebih baik untuk visualisasi
            reducer = TSNE(
                n_components=n_components,
                random_state=random_state,
                perplexity=min(30, len(embeddings) - 1),
                n_iter=1000
            )
            reduced = reducer.fit_transform(embeddings)
            logger.info("t-SNE selesai")
            return reduced
        
        else:
            raise ValueError(f"Method tidak dikenal: {method}")
    
    except Exception as e:
        logger.error(f"Error saat reduksi dimensi: {e}")
        raise


def calculate_optimal_clusters(
    embeddings: np.ndarray,
    max_clusters: int = 10,
    random_state: int = 42
) -> int:
    """
    Menghitung jumlah cluster optimal menggunakan Elbow Method
    
    Args:
        embeddings: Array embeddings
        max_clusters: Maksimum jumlah cluster untuk dicoba
        random_state: Random state
    
    Returns:
        Jumlah cluster optimal
    """
    try:
        from sklearn.metrics import silhouette_score
        
        # Standardize
        scaler = StandardScaler()
        embeddings_scaled = scaler.fit_transform(embeddings)
        
        # Coba berbagai jumlah cluster
        n_samples = len(embeddings)
        max_k = min(max_clusters, n_samples // 2)  # Minimal 2 sample per cluster
        
        if max_k < 2:
            return 2
        
        inertias = []
        silhouette_scores = []
        k_range = range(2, max_k + 1)
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=10)
            labels = kmeans.fit_predict(embeddings_scaled)
            inertias.append(kmeans.inertia_)
            
            if k > 1:  # Silhouette score butuh minimal 2 cluster
                sil_score = silhouette_score(embeddings_scaled, labels)
                silhouette_scores.append(sil_score)
            else:
                silhouette_scores.append(0)
        
        # Pilih k dengan silhouette score tertinggi
        best_k_idx = np.argmax(silhouette_scores)
        optimal_k = k_range[best_k_idx]
        
        logger.info(f"Optimal clusters: {optimal_k} (silhouette score: {silhouette_scores[best_k_idx]:.3f})")
        return optimal_k
    
    except Exception as e:
        logger.warning(f"Error saat menghitung optimal clusters: {e}, menggunakan default 5")
        return 5


def get_cluster_statistics(
    df: pd.DataFrame,
    cluster_labels: np.ndarray
) -> pd.DataFrame:
    """
    Menghitung statistik untuk setiap cluster
    
    Args:
        df: DataFrame dengan artikel
        cluster_labels: Label cluster untuk setiap artikel
    
    Returns:
        DataFrame dengan statistik per cluster
    """
    try:
        df_clustered = df.copy()
        df_clustered['cluster'] = cluster_labels
        
        # Statistik per cluster
        stats = []
        for cluster_id in sorted(df_clustered['cluster'].unique()):
            cluster_df = df_clustered[df_clustered['cluster'] == cluster_id]
            
            stat = {
                'cluster': cluster_id,
                'jumlah_artikel': len(cluster_df),
                'persentase': len(cluster_df) / len(df_clustered) * 100
            }
            
            # Statistik kategori jika ada
            if 'categories' in cluster_df.columns:
                top_category = cluster_df['categories'].value_counts().head(1)
                if not top_category.empty:
                    stat['kategori_teratas'] = top_category.index[0]
                    stat['jumlah_kategori_teratas'] = top_category.values[0]
            
            # Statistik lokasi jika ada
            if 'relevant_province' in cluster_df.columns:
                top_province = cluster_df['relevant_province'].value_counts().head(1)
                if not top_province.empty:
                    stat['provinsi_teratas'] = top_province.index[0]
            
            # Statistik platform jika ada
            if 'platform' in cluster_df.columns:
                top_platform = cluster_df['platform'].value_counts().head(1)
                if not top_platform.empty:
                    stat['platform_teratas'] = top_platform.index[0]
            
            stats.append(stat)
        
        stats_df = pd.DataFrame(stats)
        return stats_df
    
    except Exception as e:
        logger.error(f"Error saat menghitung statistik cluster: {e}")
        return pd.DataFrame()


def get_cluster_keywords(
    df: pd.DataFrame,
    cluster_labels: np.ndarray,
    text_column: str = 'content',
    top_n: int = 10
) -> Dict[int, List[str]]:
    """
    Mendapatkan kata kunci untuk setiap cluster
    
    Args:
        df: DataFrame dengan artikel
        cluster_labels: Label cluster
        text_column: Kolom teks
        top_n: Jumlah kata kunci teratas
    
    Returns:
        Dictionary {cluster_id: [keywords]}
    """
    try:
        from collections import Counter
        import re
        
        df_clustered = df.copy()
        df_clustered['cluster'] = cluster_labels
        
        cluster_keywords = {}
        
        for cluster_id in sorted(df_clustered['cluster'].unique()):
            cluster_df = df_clustered[df_clustered['cluster'] == cluster_id]
            
            # Gabungkan semua teks
            all_text = " ".join(cluster_df[text_column].fillna("").astype(str))
            
            # Clean dan split
            all_text = all_text.lower()
            all_text = re.sub(r'[^\w\s]', ' ', all_text)
            words = all_text.split()
            
            # Filter stopwords sederhana
            stopwords = {
                'yang', 'di', 'ke', 'dari', 'dan', 'atau', 'untuk', 'pada', 'dengan', 'dalam',
                'adalah', 'ini', 'itu', 'tidak', 'akan', 'sudah', 'telah', 'juga', 'dapat', 'bisa',
                'ada', 'nya', 'oleh', 'kepada', 'terhadap', 'antara', 'karena', 'jika',
                'tersebut', 'tadi', 'demikian', 'begitu', 'saja', 'juga', 'pula'
            }
            
            words = [w for w in words if len(w) >= 4 and w not in stopwords]
            
            # Count dan ambil top N
            word_counts = Counter(words)
            top_words = [word for word, count in word_counts.most_common(top_n)]
            
            cluster_keywords[cluster_id] = top_words
        
        return cluster_keywords
    
    except Exception as e:
        logger.error(f"Error saat mendapatkan kata kunci cluster: {e}")
        return {}

