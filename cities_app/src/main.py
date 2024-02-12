from fastapi import FastAPI


from .geo.router import geo_router


app = FastAPI(
    title="file_sharing"
)
app.include_router(geo_router)
