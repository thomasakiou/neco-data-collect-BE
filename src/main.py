from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.endpoints import auth, ssce, bece, lga
from src.core.config import settings
from src.infrastructure.db.session import SessionLocal
from src.infrastructure.repositories.user_repository_impl import SQLAlchemyUserRepository
from src.application.users.services import AuthService

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Seed admin user
    db = SessionLocal()
    try:
        repo = SQLAlchemyUserRepository(db)
        auth_service = AuthService(repo)
        
        admin_email = "thomas.akiou@gmail.com"
        if not repo.get_by_email(admin_email):
            auth_service.register_user(
                email=admin_email,
                password="123456",
                state_code="000",
                state_name="HQ"
            )
            print(f"Admin user {admin_email} created.")
    except Exception as e:
        print(f"Error seeding admin: {e}")
    finally:
        db.close()
    yield
    # Shutdown logic (if any) can go here

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:5174", 
        "http://localhost:5175",
        "https://necodata.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(ssce.router, prefix="/api/v1/ssce", tags=["ssce"])
app.include_router(bece.router, prefix="/api/v1/bece", tags=["bece"])
app.include_router(lga.router, prefix="/api/v1/lga", tags=["lga"])

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8001, reload=True)
