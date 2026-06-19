"""
Main FastAPI application entry point.
Configures CORS, mounts all routers, and initializes the database.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import init_db
from backend.seeder import seed

# Import all models so SQLModel registers them
import backend.models  # noqa: F401

from backend.auth import router as auth_router
from backend.routers.accounts import router as accounts_router
from backend.routers.admin import router as admin_router
from backend.routers.atm import router as atm_router

from backend.routers.dashboard import router as dashboard_router
from backend.routers.limits import router as limits_router
from backend.routers.loans import router as loans_router
from backend.routers.notifications import router as notifications_router
from backend.routers.profile import router as profile_router
from backend.routers.recipients import router as recipients_router
from backend.routers.savings_goals import router as savings_goals_router
from backend.routers.standing_orders import router as standing_orders_router
from backend.routers.transfers import router as transfers_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and seed data on startup."""
    init_db()
    seed()
    yield


app = FastAPI(
    title="IO Bank API",
    description="Banking system API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(accounts_router)
app.include_router(transfers_router)
app.include_router(atm_router)
app.include_router(recipients_router)
app.include_router(loans_router)

app.include_router(profile_router)
app.include_router(limits_router)
app.include_router(notifications_router)
app.include_router(savings_goals_router)
app.include_router(standing_orders_router)
app.include_router(admin_router)


@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}
