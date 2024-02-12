from setuptools import setup, find_packages

setup(
    name="src",
    packages=["src","src.geo"],
    version="0.0.1",
    install_requires=["fastapi", "pydantic", "SQLAlchemy", "uvicorn", "gunicorn",
                      "python-dotenv", "asyncpg",
                      "aiohttp", "alembic"],
)