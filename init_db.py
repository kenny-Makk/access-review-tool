from sqlalchemy import create_engine
from models import Base


engine = create_engine("sqlite:///review.db")
Base.metadata.create_all(engine)
print("done")