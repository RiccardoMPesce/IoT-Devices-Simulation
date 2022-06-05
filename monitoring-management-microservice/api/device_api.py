from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from db.database_manager import DeviceDatabaseManager, get_database
from api.models.generic import Error
from api.public.user.models import User
from api.utils.logger import logger_config

logger = logger_config(__name__)

router = APIRouter()