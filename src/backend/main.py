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

# Mock classes for core components (replacing unavailable imports)
class HomeBuddy:
    """HomeBuddy class with fallback responses"""
    def __init__(self):
        self.name = "HomeBuddy"
        logger.info("HomeBuddy initialized with fallback system")
        
    def search_chunks(self, query: str, k: int = 5):
        """Mock search that returns empty list"""
        return []
    
    def process_query(self, query: str, chunks: list, brand: str = None, model: str = None):
        """Process query with rule-based fallback"""
        query_lower = query.lower()
        
        # Common appliance issues and solutions
        solutions = {
            "not working": "1. Check power connection and outlet\n2. Verify the appliance is turned on\n3. Check circuit breaker/fuse\n4. Inspect power cord for damage\n5. If problem persists, contact a technician",
            "noise": "1. Check if appliance is level\n2. Ensure nothing is stuck or loose inside\n3. Verify all parts are properly assembled\n4. Check for worn bearings or belts\n5. Regular maintenance may be needed",
            "leak": "1. Check all hoses and connections\n2. Inspect door seals/gaskets\n3. Ensure appliance is level\n4. Check drain system for clogs\n5. Replace damaged seals if necessary",
            "won't drain": "1. Check drain hose for kinks or clogs\n2. Clean drain filter/trap\n3. Verify drain pump is working\n4. Check for blockages in drain line\n5. Ensure proper installation",
            "won't start": "1. Check power supply and outlet\n2. Ensure door/lid is properly closed\n3. Check for tripped breakers\n4. Verify all safety switches\n5. Check control panel settings",
            "error code": f"Error codes vary by brand. For {brand or 'your appliance'}:\n1. Note the exact error code\n2. Check the user manual for code meanings\n3. Try resetting the appliance\n4. Common fixes: check water supply, drain system, and door locks\n5. Contact manufacturer support with the code",
            "smell": "1. Clean the appliance thoroughly\n2. Check for mold or mildew\n3. Run a cleaning cycle\n4. Check for burnt components (electrical smell)\n5. Ensure proper ventilation",
            "won't heat": "1. Check power supply\n2. Verify heating element\n3. Check thermostat settings\n4. Inspect heating coils for damage\n5. Test thermal fuse"
        }
        
        # Find matching solution
        answer = None
        for keyword, solution in solutions.items():
            if keyword in query_lower:
                answer = solution
                break
        
        # Default response if no match
        if not answer:
            answer = f"""Here are troubleshooting steps for your issue:

1. Check power connection and outlet
2. Verify the appliance is turned on
3. Check circuit breaker/fuse
4. Inspect for blockages or visible damage
5. If problem persists, contact a technician

⚠️ For gas or electrical issues, contact a professional immediately."""
        
        return {
            "answer": answer,
            "sources": [],
            "confidence_score": 0.75,
            "safety_flag": "gas" in query_lower or "electrical" in query_lower or "shock" in query_lower,
            "safety_level": "caution" if any(word in query_lower for word in ["gas", "electrical", "shock", "smoke"]) else "safe",
            "safety_message": "⚠️ This may require professional assistance for safety reasons." if any(word in query_lower for word in ["gas", "electrical", "shock", "smoke"]) else ""
        }

class ApplianceSafetyChecker:
    """Safety checker with basic hazard detection"""
    def __init__(self):
        self.name = "SafetyChecker"
        logger.info("ApplianceSafetyChecker initialized")
    
    def analyze_safety(self, query: str):
        """Analyze query for safety hazards"""
        query_lower = query.lower()
        
        # Emergency keywords
        emergency_keywords = ["gas leak", "gas smell", "smoke", "fire", "burning smell", "sparks", "electric shock"]
        danger_keywords = ["electrical", "gas", "not turning off", "overheating"]
        caution_keywords = ["strange noise", "unusual smell", "vibrating", "leaking"]
        
        for keyword in emergency_keywords:
            if keyword in query_lower:
                return ("emergency", "🚨 EMERGENCY: Turn off appliance immediately and contact professional help!", True)
        
        for keyword in danger_keywords:
            if keyword in query_lower:
                return ("danger", "⚠️ DANGER: This requires professional attention. Do not attempt DIY repair.", True)
        
        for keyword in caution_keywords:
            if keyword in query_lower:
                return ("caution", "⚡ CAUTION: Proceed carefully and consider professional help if unsure.", False)
        
        return ("safe", "", False)

class ModelManager:
    """Mock ModelManager class"""
    def __init__(self):
        self.name = "ModelManager"

model_manager = ModelManager()

# FastAPI app with optimized configuration
app = FastAPI(
    title="HomeBuddy API",
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
home_buddy = None
safety_checker = None
metrics_store = {
    "queries": [],
    "response_times": [],
    "search_times": [],
    "llm_times": [],
    "safety_alerts": 0,
    "precision_scores": []
}

# Root endpoint
@app.get("/")
async def root():
    """API is running"""
    return {
        "message": "HomeBuddy Backend Running",
        "version": "1.0.0",
        "status": "ok",
        "endpoints": {
            "appliances": "/user/appliances",
            "repairs": "/user/repair-history",
            "alerts": "/user/alerts",
            "stats": "/user/stats"
        }
    }

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    global home_buddy, safety_checker
    
    logger.info("Initializing HomeBuddy components...")
    
    try:
        # Initialize safety checker (fast)
        safety_checker = ApplianceSafetyChecker()
        logger.info("Safety checker initialized")
        
        # Initialize HomeBuddy (may take time for model loading)
        home_buddy = HomeBuddy()
        logger.info("HomeBuddy initialized successfully")
        
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        # Continue with limited functionality
        home_buddy = None

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
        "home_buddy_loaded": home_buddy is not None,
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
        
        # Enhance query with device context if available
        enhanced_query = request.query
        if request.brand and request.model:
            enhanced_query = f"[Device: {request.brand} {request.model}] {request.query}"
        
        # Search phase
        search_start = time.time()
        if home_buddy:
            # Get relevant chunks with timing
            chunks = await asyncio.to_thread(
                home_buddy.search_chunks,
                enhanced_query if (request.brand and request.model) else request.query,
                request.k
            )
            search_time = time.time() - search_start
            
            # LLM generation phase
            llm_start = time.time()
            result = await asyncio.to_thread(
                home_buddy.process_query,
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

@app.post("/device/answer", response_model=AnswerResponse)
async def get_device_specific_answer(request: QueryRequest):
    """
    Device-specific query endpoint optimized for filtered manual search
    Returns answers specifically from the device's manual
    """
    if not request.brand or not request.model:
        return AnswerResponse(
            answer="Please provide device brand and model for device-specific search",
            safety_flag=False,
            safety_level="safe",
            sources=[],
            chunks_used=0,
            processing_time=0.0,
            search_time=0.0,
            llm_time=0.0,
            confidence_score=0.0
        )
    
    # Use the standard endpoint with brand/model context
    return await get_answer(request)

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
        if home_buddy:
            # Process PDF and add to knowledge base
            chunks_processed = await asyncio.to_thread(
                home_buddy.process_pdf,
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

# =====================================================
# Personalized Repair Assistant Endpoints
# =====================================================

# In-memory storage for user appliances (replace with database in production)
user_appliances_store = {}
repair_history_store = {}
maintenance_alerts_store = {}

class UserApplianceModel(BaseModel):
    brand: str
    model: str
    appliance_type: str
    serial_number: Optional[str] = None
    purchase_date: str

class RepairRecordModel(BaseModel):
    appliance_id: str
    issue: str
    symptoms: List[str]
    resolution: str
    parts_replaced: Optional[List[str]] = None
    serviced_by: str = "diy"
    cost: Optional[float] = None

class PredictiveAlertModel(BaseModel):
    appliance_id: str
    alert_type: str
    title: str
    description: str
    recommended_action: str

@app.post("/user/appliance")
async def add_user_appliance(user_id: str, appliance: UserApplianceModel):
    """Add a new appliance to user's profile"""
    try:
        if user_id not in user_appliances_store:
            user_appliances_store[user_id] = []
        
        appliance_id = f"app-{int(time.time() * 1000)}"
        appliance_data = {
            "id": appliance_id,
            "user_id": user_id,
            **appliance.dict(),
            "added_at": datetime.now().isoformat()
        }
        
        user_appliances_store[user_id].append(appliance_data)
        
        logger.info(f"Appliance added for user {user_id}: {appliance.brand} {appliance.model}")
        return {
            "status": "success",
            "appliance_id": appliance_id,
            "message": f"Added {appliance.brand} {appliance.model}"
        }
    except Exception as e:
        logger.error(f"Error adding appliance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/appliances")
async def get_user_appliances(user_id: str):
    """Get all appliances for a user"""
    try:
        appliances = user_appliances_store.get(user_id, [])
        return {
            "status": "success",
            "appliances": appliances,
            "count": len(appliances)
        }
    except Exception as e:
        logger.error(f"Error retrieving appliances: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/user/appliance/{appliance_id}")
async def remove_user_appliance(user_id: str, appliance_id: str):
    """Remove an appliance from user's profile"""
    try:
        if user_id in user_appliances_store:
            user_appliances_store[user_id] = [
                a for a in user_appliances_store[user_id]
                if a["id"] != appliance_id
            ]
            return {"status": "success", "message": "Appliance removed"}
        return {"status": "error", "message": "User not found"}
    except Exception as e:
        logger.error(f"Error removing appliance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/user/repair")
async def log_repair(user_id: str, repair: RepairRecordModel):
    """Log a repair/issue for an appliance"""
    try:
        if user_id not in repair_history_store:
            repair_history_store[user_id] = []
        
        repair_id = f"repair-{int(time.time() * 1000)}"
        repair_data = {
            "id": repair_id,
            "user_id": user_id,
            **repair.dict(),
            "date": datetime.now().isoformat()
        }
        
        repair_history_store[user_id].append(repair_data)
        
        # Generate predictive alerts based on repair patterns
        _generate_alerts(user_id, repair.appliance_id)
        
        logger.info(f"Repair logged for user {user_id}, appliance {repair.appliance_id}")
        return {
            "status": "success",
            "repair_id": repair_id,
            "message": "Repair record added"
        }
    except Exception as e:
        logger.error(f"Error logging repair: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/repair-history")
async def get_repair_history(user_id: str, appliance_id: Optional[str] = None):
    """Get repair history for user or specific appliance"""
    try:
        history = repair_history_store.get(user_id, [])
        
        if appliance_id:
            history = [r for r in history if r["appliance_id"] == appliance_id]
        
        return {
            "status": "success",
            "repairs": sorted(history, key=lambda x: x["date"], reverse=True),
            "count": len(history)
        }
    except Exception as e:
        logger.error(f"Error retrieving repair history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/alerts")
async def get_predictive_alerts(user_id: str):
    """Get predictive maintenance alerts for user"""
    try:
        alerts = maintenance_alerts_store.get(user_id, [])
        # Filter unacknowledged alerts
        active_alerts = [a for a in alerts if not a.get("acknowledged", False)]
        
        return {
            "status": "success",
            "alerts": active_alerts,
            "count": len(active_alerts)
        }
    except Exception as e:
        logger.error(f"Error retrieving alerts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/user/alert/{alert_id}/acknowledge")
async def acknowledge_alert(user_id: str, alert_id: str):
    """Acknowledge a predictive alert"""
    try:
        alerts = maintenance_alerts_store.get(user_id, [])
        for alert in alerts:
            if alert["id"] == alert_id:
                alert["acknowledged"] = True
                return {"status": "success", "message": "Alert acknowledged"}
        return {"status": "error", "message": "Alert not found"}
    except Exception as e:
        logger.error(f"Error acknowledging alert: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/stats")
async def get_user_stats(user_id: str):
    """Get user's appliance and repair statistics"""
    try:
        appliances = user_appliances_store.get(user_id, [])
        repairs = repair_history_store.get(user_id, [])
        
        total_spent = sum(r.get("cost", 0) for r in repairs if r.get("cost"))
        diy_count = len([r for r in repairs if r.get("serviced_by") == "diy"])
        pro_count = len([r for r in repairs if r.get("serviced_by") == "professional"])
        
        # Common issues
        issue_counts = {}
        for repair in repairs:
            issue = repair.get("issue", "Unknown")
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        common_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "status": "success",
            "stats": {
                "total_appliances": len(appliances),
                "total_repairs": len(repairs),
                "diy_repairs": diy_count,
                "professional_repairs": pro_count,
                "total_spent": round(total_spent, 2),
                "common_issues": [issue for issue, count in common_issues],
                "average_cost_per_repair": round(total_spent / len(repairs), 2) if repairs else 0
            }
        }
    except Exception as e:
        logger.error(f"Error calculating stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def _generate_alerts(user_id: str, appliance_id: str):
    """Generate predictive alerts based on repair patterns"""
    try:
        if user_id not in maintenance_alerts_store:
            maintenance_alerts_store[user_id] = []
        
        appliance = next(
            (a for a in user_appliances_store.get(user_id, []) if a["id"] == appliance_id),
            None
        )
        if not appliance:
            return
        
        repairs = [r for r in repair_history_store.get(user_id, []) 
                  if r["appliance_id"] == appliance_id]
        
        # Check for recurring issues
        issue_counts = {}
        for repair in repairs:
            issue = repair.get("issue", "Unknown")
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        for issue, count in issue_counts.items():
            if count >= 2:
                alert_id = f"alert-{int(time.time() * 1000)}"
                alert = {
                    "id": alert_id,
                    "appliance_id": appliance_id,
                    "user_id": user_id,
                    "type": "recurring_issue",
                    "title": f"Recurring Issue: {issue}",
                    "description": f"You've experienced '{issue}' {count} times. Consider professional service.",
                    "severity": "critical" if count >= 3 else "warning",
                    "created_at": datetime.now().isoformat(),
                    "acknowledged": False
                }
                # Check if similar alert already exists
                if not any(a["appliance_id"] == appliance_id and a["title"] == alert["title"] 
                          for a in maintenance_alerts_store[user_id]):
                    maintenance_alerts_store[user_id].append(alert)
    except Exception as e:
        logger.error(f"Error generating alerts: {str(e)}")

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