import pandas as pd
from sqlalchemy.orm import joinedload
from helpers.date_extractor import extract_all_dates, extract_relevant_date
import swifter

from db.connection import SessionLocal
from models.entities import Article


def load_articles_df():
    session = SessionLocal()
    articles = (
        session.query(Article)
        .options(
            joinedload(Article.categories),
            joinedload(Article.tags),
            joinedload(Article.classifications),
            joinedload(Article.references)
        )
        .all()
    )
    session.close()

    rows = []
    for a in articles:
        row = {col.name: getattr(a, col.name) for col in Article.__table__.columns}
        row["categories"] = ", ".join(f"{c.name}" for c in a.categories) if a.categories else ""
        row["classifications"] = ", ".join(f"{cl.name}" for cl in a.classifications) if a.classifications else ""
        row["references"] = ", ".join(f"{r.ref_url}" for r in a.references) if a.references else ""
        rows.append(row)

    df = pd.DataFrame(rows)

    return df

def enrich_with_dates(df):
    df["all_dates"] = df["content"].swifter.apply(extract_all_dates)
    df["relevant_date"] = df["content"].swifter.apply(extract_relevant_date)
    return df
