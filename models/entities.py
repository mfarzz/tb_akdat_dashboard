from sqlalchemy import Column, BigInteger, Integer, Text, String, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from .base import Base

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(BigInteger, primary_key=True)
    title = Column(Text, nullable=False)
    slug = Column(Text)
    description = Column(Text)
    content = Column(Text)
    author = Column(String(150))
    published_at = Column(DateTime)
    source_url = Column(Text)
    image_url = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    status = Column(String(50))
    fact = Column(Text)
    source_issue = Column(String(255))
    source_link = Column(Text)
    
    categories = relationship("Category", secondary="article_categories", back_populates="articles")
    tags = relationship("Tag", secondary="article_tags", back_populates="articles")
    classifications = relationship("Classification", secondary="article_classifications", back_populates="articles")
    references = relationship("ArticleReference", back_populates="article")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    
    articles = relationship("Article", secondary="article_categories", back_populates="categories")

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    
    articles = relationship("Article", secondary="article_tags", back_populates="tags")

class Classification(Base):
    __tablename__ = "classifications"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    
    articles = relationship("Article", secondary="article_classifications", back_populates="classifications")

class ArticleReference(Base):
    __tablename__ = "article_references"
    
    id = Column(Integer, primary_key=True)
    article_id = Column(BigInteger, ForeignKey("articles.id"))
    ref_url = Column(Text)
    
    article = relationship("Article", back_populates="references")

class ArticleCategory(Base):
    __tablename__ = "article_categories"
    
    article_id = Column(BigInteger, ForeignKey("articles.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    __table_args__ = (PrimaryKeyConstraint('article_id', 'category_id'),)

class ArticleTag(Base):
    __tablename__ = "article_tags"
    
    article_id = Column(BigInteger, ForeignKey("articles.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
    
    __table_args__ = (PrimaryKeyConstraint('article_id', 'tag_id'),)

class ArticleClassification(Base):
    __tablename__ = "article_classifications"
    
    article_id = Column(BigInteger, ForeignKey("articles.id"), nullable=False)
    classification_id = Column(Integer, ForeignKey("classifications.id"), nullable=False)
    
    __table_args__ = (PrimaryKeyConstraint('article_id', 'classification_id'),)