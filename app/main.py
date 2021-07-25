import uvicorn

from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI

from routers import root, auth
from databases.database import engine, Base

app = FastAPI(
    title='py-auth',
    description='Authentication service made by Python'
)

# database
Base.metadata.create_all(bind=engine)

# routers
app.include_router(root.router)
app.include_router(auth.router)

# Versioned_FastAPI
app = VersionedFastAPI(app,
                       prefix_format='/v{major}',
                       version_format='{major}')


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)