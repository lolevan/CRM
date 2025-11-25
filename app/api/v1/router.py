from fastapi import APIRouter
from .operators import router as operators_router
from .sources import router as sources_router
from .contacts import router as contacts_router
from .leads import router as leads_router
from .stats import router as stats_router

router = APIRouter()
router.include_router(operators_router, tags=["operators"])
router.include_router(sources_router, tags=["sources"])
router.include_router(contacts_router, tags=["contacts"])
router.include_router(leads_router, tags=["leads"])
router.include_router(stats_router, tags=["stats"])
