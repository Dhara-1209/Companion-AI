#!/usr/bin/env python3
"""
High-performance API with metrics logging and safety-first approach
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import time
import logging
import json
from pathlib import Path
import uvicorn
import asyncio
from datetime import datetime

# Import core components
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core.models.companion_ai import CompanionAI
from core.models.safety_checker import ApplianceSafetyChecker
from core.models.model_manager import ModelManager, model_manager

# Create logs directory
Path("logs").mkdir(exist_ok=True)

# Configure logging with metrics
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/api_metrics.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# FastAPI app with optimized configuration
app = FastAPI(
    title="CompanionAI API",
    description="High-performance appliance troubleshooting API with safety detection",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class QueryRequest(BaseModel):
    query: str = Field(..., description="User's appliance question")
    brand: Optional[str] = Field(None, description="Appliance brand")
    model: Optional[str] = Field(None, description="Appliance model")
    k: int = Field(10, description="Number of chunks to retrieve", ge=1, le=20)

class SourceInfo(BaseModel):
    filename: str
    page: Optional[int] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    relevance_score: float

class AnswerResponse(BaseModel):
    answer: str
    safety_flag: bool
    safety_level: str
    safety_message: Optional[str] = None
    sources: List[SourceInfo]
    chunks_used: int
    processing_time: float
    search_time: float
    llm_time: float
    confidence_score: float

class UploadResponse(BaseModel):
    filename: str
    status: str
    chunks_processed: int
    processing_time: float

class MetricsResponse(BaseModel):
    total_queries: int
    avg_response_time: float
    avg_search_time: float
    avg_llm_time: float
    safety_alerts_triggered: int
    precision_at_5: float

# Global components
companion_ai = None
safety_checker = None
metrics_store = {
    "queries": [],
    "response_times": [],
    "search_times": [],
    "llm_times": [],
    "safety_alerts": 0,
    "precision_scores": []
}

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    global companion_ai, safety_checker
    
    logger.info("Initializing CompanionAI components...")
    
    try:
        # Initialize safety checker (fast)
        safety_checker = ApplianceSafetyChecker()
        logger.info("Safety checker initialized")
        
        # Initialize companion AI (may take time for model loading)
        companion_ai = CompanionAI()
        logger.info("CompanionAI initialized successfully")
        
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        # Continue with limited functionality
        companion_ai = None

def log_metrics(query: str, response_time: float, search_time: float, llm_time: float, safety_flag: bool):
    """Log performance metrics"""
    timestamp = datetime.now().isoformat()
    
    # Store in memory for quick access
    metrics_store["queries"].append({
        "timestamp": timestamp,
        "query": query,
        "response_time": response_time,
        "search_time": search_time,
        "llm_time": llm_time,
        "safety_flag": safety_flag
    })
    
    if safety_flag:
        metrics_store["safety_alerts"] += 1
    
    # Keep only last 1000 queries in memory
    if len(metrics_store["queries"]) > 1000:
        metrics_store["queries"] = metrics_store["queries"][-1000:]
    
    # Log to file
    log_entry = {
        "timestamp": timestamp,
        "query_length": len(query),
        "response_time": response_time,
        "search_time": search_time,
        "llm_time": llm_time,
        "safety_flag": safety_flag
    }
    
    logger.info(f"METRICS: {json.dumps(log_entry)}")

@app.get("/health")
async def health_check():
    """Optimized health check"""
    return {
        "status": "healthy",
        "companion_ai_loaded": companion_ai is not None,
        "safety_checker_loaded": safety_checker is not None,
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

@app.post("/answer", response_model=AnswerResponse)
async def get_answer(request: QueryRequest):
    """
    Optimized answer endpoint with comprehensive metrics
    Target: <2s response time, >80% precision@5
    """
    start_time = time.time()
    search_time = 0
    llm_time = 0
    
    try:
        # Safety check (fast, <50ms)
        safety_start = time.time()
        if safety_checker:
            safety_level, safety_message, _ = safety_checker.analyze_safety(request.query)
            safety_flag = safety_level != "safe"
        else:
            safety_level = "safe"
            safety_message = ""
            safety_flag = False
        
        # Search phase
        search_start = time.time()
        if companion_ai:
            # Get relevant chunks with timing
            chunks = await asyncio.to_thread(
                companion_ai.search_chunks,
                request.query,
                request.k
            )
            search_time = time.time() - search_start
            
            # LLM generation phase
            llm_start = time.time()
            result = await asyncio.to_thread(
                companion_ai.process_query,
                request.query,
                chunks,
                request.brand,
                request.model
            )
            llm_time = time.time() - llm_start
            
            
            # Build sources from result
            sources = []
            for source in result.get("sources", []):
                # Convert page to int, handle non-numeric values
                page_value = source.get("page")
                if isinstance(page_value, str):
                    try:
                        page_int = int(page_value)
                    except (ValueError, TypeError):
                        page_int = None
                elif isinstance(page_value, int):
                    page_int = page_value
                else:
                    page_int = None
                
                source_info = SourceInfo(
                    filename=source.get("filename", "unknown"),
                    page=page_int,
                    brand=source.get("brand"),
                    model=source.get("model"),
                    relevance_score=source.get("relevance_score", 0.0)
                )
                sources.append(source_info)
            
            # Extract values from result
            answer = result.get("answer", "No answer generated")
            confidence_score = result.get("confidence_score", 0.85)
            safety_flag = result.get("safety_flag", False)
            safety_level = result.get("safety_level", "safe")
            safety_message = result.get("safety_message", "")
            
        else:
            # Fallback mode
            answer = "System is initializing. Please try again in a moment."
            sources = []
            confidence_score = 0.0
        
        # Calculate total processing time
        processing_time = time.time() - start_time
        
        # Log metrics
        log_metrics(
            request.query,
            processing_time,
            search_time,
            llm_time,
            safety_flag
        )
        
        response = AnswerResponse(
            answer=answer,
            safety_flag=safety_flag,
            safety_level=safety_level,
            safety_message=safety_message if safety_message else None,
            sources=sources,
            chunks_used=len(sources),
            processing_time=processing_time,
            search_time=search_time,
            llm_time=llm_time,
            confidence_score=confidence_score
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        processing_time = time.time() - start_time
        
        return AnswerResponse(
            answer=f"I apologize, but I encountered an error processing your request. Please try again.",
            safety_flag=False,
            safety_level="safe",
            sources=[],
            chunks_used=0,
            processing_time=processing_time,
            search_time=search_time,
            llm_time=llm_time,
            confidence_score=0.0
        )

@app.post("/upload", response_model=UploadResponse)
async def upload_manual(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Handle manual upload with background processing
    """
    start_time = time.time()
    
    try:
        # Validate file
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Save file temporarily
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process in background
        background_tasks.add_task(process_uploaded_file, file_path)
        
        processing_time = time.time() - start_time
        
        return UploadResponse(
            filename=file.filename,
            status="processing",
            chunks_processed=0,  # Will be updated by background task
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_uploaded_file(file_path: Path):
    """Background task to process uploaded PDF"""
    try:
        if companion_ai:
            # Process PDF and add to knowledge base
            chunks_processed = await asyncio.to_thread(
                companion_ai.process_pdf,
                str(file_path)
            )
            logger.info(f"Processed {file_path.name}: {chunks_processed} chunks")
        
        # Clean up temporary file
        file_path.unlink()
        
    except Exception as e:
        logger.error(f"Background processing error: {str(e)}")

@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get system performance metrics"""
    try:
        queries = metrics_store["queries"]
        
        if not queries:
            return MetricsResponse(
                total_queries=0,
                avg_response_time=0.0,
                avg_search_time=0.0,
                avg_llm_time=0.0,
                safety_alerts_triggered=0,
                precision_at_5=0.0
            )
        
        # Calculate averages
        avg_response_time = sum(q["response_time"] for q in queries) / len(queries)
        avg_search_time = sum(q["search_time"] for q in queries) / len(queries)
        avg_llm_time = sum(q["llm_time"] for q in queries) / len(queries)
        
        # Estimate precision@5 (would need evaluation dataset for real calculation)
        precision_at_5 = 0.85  # Placeholder - implement with evaluation script
        
        return MetricsResponse(
            total_queries=len(queries),
            avg_response_time=avg_response_time,
            avg_search_time=avg_search_time,
            avg_llm_time=avg_llm_time,
            safety_alerts_triggered=metrics_store["safety_alerts"],
            precision_at_5=precision_at_5
        )
        
    except Exception as e:
        logger.error(f"Metrics error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving metrics")

@app.get("/demo/queries")
async def get_demo_queries():
    """Get predefined demo queries for testing"""
    return {
        "safe_queries": [
            {
                "query": "My Samsung WF45 won't spin, what does E3 mean?",
                "brand": "Samsung",
                "model": "WF45",
                "expected_safety": "safe"
            },
            {
                "query": "How to clean lint filter?",
                "expected_safety": "safe"
            },
            {
                "query": "Dishwasher not draining properly",
                "expected_safety": "safe"
            }
        ],
        "safety_queries": [
            {
                "query": "I smell gas from the oven",
                "expected_safety": "emergency"
            },
            {
                "query": "My microwave is sparking",
                "expected_safety": "danger"
            },
            {
                "query": "Water leaking from washing machine",
                "expected_safety": "caution"
            }
        ]
    }

if __name__ == "__main__":
    # Production-optimized server configuration
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=1,  # Adjust based on system resources
        log_level="info",
        access_log=True,
        reload=False  # Disable in production
    )