from fastapi import FastAPI

app = FastAPI(
    title="CareerPilot API",
    description="Backend API for the CareerPilot job search platform.",
    version="0.1.0",
)

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "CareerPilot is running"}

    @app.get("/heath")
    def health_check() -> dict[str, str]:
        return {"status": "healthy"}