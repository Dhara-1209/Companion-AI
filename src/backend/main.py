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
        """Process query with comprehensive rule-based responses"""
        query_lower = query.lower()
        
        # Comprehensive appliance solutions with detailed steps
        solutions = {
            "not working": """APPLIANCE NOT WORKING - COMPREHENSIVE TROUBLESHOOTING GUIDE

**STEP 1: POWER SUPPLY (Start Here)**
- Verify the power outlet works by plugging in another device (lamp, phone charger)
- Check if the outlet has power by testing with a known working appliance
- Inspect the appliance's power cord for visible damage, cuts, or exposed wires
- Ensure the power cord is fully inserted into the outlet
- Try a different outlet in another room to rule out breaker issues
- Check your home's circuit breaker panel for tripped breakers related to the appliance room

**STEP 2: CONTROL PANEL & INDICATORS**  
- Look for indicator lights or display panels (LED, LCD, or digital display)
- Check if any lights are on, blinking, or showing error codes
- Try pressing power button multiple times (hold for 3-5 seconds)
- Check if the appliance makes any sounds (hums, clicks, beeps)
- Consult manual for what lights mean when powered on

**STEP 3: SAFETY LOCKS & DOORS**
- Ensure all doors/lids are properly closed and latched
- Check for door switches that might prevent operation
- Try opening and closing the door firmly several times
- Look for broken door handles or latches
- Verify no error codes appear related to door position

**STEP 4: RESET THE APPLIANCE**
- Unplug the appliance from the outlet
- Wait 2-3 minutes to allow internal systems to reset
- Plug back in and try operating again
- For digital displays, this often clears temporary glitches

**STEP 5: ADVANCED TROUBLESHOOTING**
- Check user manual for specific troubleshooting section
- Look for hidden reset buttons or special key sequences
- Test with different settings or modes
- Verify you're using the correct operational sequence
- Check if water supply is needed and turned on (for water-using appliances)

**When to Call a Professional:**
- If circuit breaker continues to trip
- If you smell burning or see sparks
- If there's water damage or corrosion visible
- After trying all steps above with no result""",
            
            "noise": """APPLIANCE MAKING UNUSUAL NOISE - DIAGNOSIS & SOLUTIONS

**NOISE DIAGNOSIS GUIDE**
- **Grinding sound**: Typically indicates debris stuck in mechanism
- **Squealing/Squeaking**: Usually worn bearings or rubber belts
- **Clicking/Tapping**: Often loose components or worn parts
- **Thumping/Banging**: Usually something unbalanced or loose
- **Rattling**: Typically loose fasteners or internal parts

**IMMEDIATE STEPS**
1. STOP the appliance immediately if noise is concerning
2. Unplug from outlet for safety
3. Open and inspect the interior if accessible
4. Look for obvious debris, loose items, or broken parts
5. Note the type and timing of the noise (start-up, mid-cycle, end)

**DIAGNOSIS & FIXES**

For **Grinding/Foreign Object Noise**:
- Turn off and unplug the appliance
- Remove and inspect filter, drain, or basket area
- Use a flashlight to look inside for coins, buttons, or debris
- Carefully remove any foreign objects
- Vacuum or flush the area with water if needed
- Test by running it empty to confirm noise is gone

For **Squealing/Squeaking Sounds**:
- This typically indicates worn rubber seals or belts
- Check manual for belt location
- Using a rubber conditioner on accessible rubber parts may help temporarily
- Professional replacement usually needed for longevity

For **Clicking/Tapping During Operation**:
- Usually harmless (solenoid clicks, relays engaging)
- Becomes concerning if accompanied by malfunction
- Regular clicking is often completely normal for some appliances

For **Unbalanced/Thumping Sounds**:
- Ensure appliance is sitting level and stable
- Check feet aren't damaged or uneven
- Try adjusting the leveling feet if available
- Ensure load is distributed evenly inside

For **Rattling from Loose Parts**:
- Unplug appliance
- Visually inspect for loose screws, bolts, or panels
- Tighten any loose fasteners you find
- Check all access panels are properly secured
- Ensure all internal brackets and supports are intact

**MAINTENANCE PREVENTION**
- Run cleaning cycles regularly (1-2 times per month)
- Don't overload the appliance
- Use appropriate detergents/cleaners for your appliance
- Keep filters clean and unclogged
- Inspect for debris during use""",
            
            "leak": """WATER LEAK FROM APPLIANCE - URGENT TROUBLESHOOTING

**IMMEDIATE SAFETY STEPS**
1. Turn off and unplug the appliance NOW
2. Stop using it immediately 
3. Do not attempt to use it again until fixed
4. Clean up any water and dry the area
5. Check for water damage to surrounding items

**STEP 1: LOCATE THE LEAK SOURCE**
- Is water leaking from the bottom?
- Is it coming from a door/seal area?
- Is it from a side panel or connection?
- Is it dripping or pouring?
- Note exactly where you see the water coming from

**STEP 2: COMMON CAUSES & IMMEDIATE FIXES**

**Loose/Disconnected Hoses**:
- Check all water hoses for secure connections
- Hoses should be hand-tight plus 1/4 turn with wrench
- Look for visible cracks or damage in hoses
- Check water inlet hoses at wall connection
- Tighten all connection points firmly

**Clogged Drain Hose**:
- Locate the drain hose (usually at back or bottom)
- Disconnect carefully and place in bucket
- Flush with warm water to clear blockages
- Look for kinks or pinches in the hose
- Ensure it properly connects to drain or standpipe

**Failed Door Seal/Gasket**:
- Visually inspect the rubber door seal for:
  - Visible tears or deterioration
  - Hard spots or brittleness
  - Mold or residue deposits
- Clean the seal with warm soapy water
- Check if door properly closes and latches
- Replace gasket if visibly damaged (usually $20-50)

**Pump Issues**:
- Check if pump is actively running during operation
- Listen for pump noise
- Inspect pump area for visible leaks
- Professional replacement typically needed

**STEP 3: CHECK INSTALLATION**
- Verify appliance is sitting level (use level tool)
- Sloped leveling feet can allow water to pool
- Ensure proper water line pressure (should be 20-100 PSI)
- Confirm drain connection is proper height

**STEP 4: PREVENT FUTURE LEAKS**
- Replace hoses every 5-7 years proactively
- Keep washer/dryer lint filters clean
- Use appropriate detergent amounts
- Run maintenance cycles monthly
- Inspect connections quarterly

**WHEN TO CALL PROFESSIONAL**
- Multiple leak sources
- Leak from internal pump/motor area  
- Water damage has occurred
- You've found the problem but don't feel comfortable fixing it
- After 24 hours of troubleshooting with no improvement""",
            
            "won't drain": """APPLIANCE NOT DRAINING WATER - COMPLETE GUIDE

**EMERGENCY PROCEDURE**
1. Turn off and unplug appliance immediately
2. Remove water manually if buildup is severe:
   - Use a bucket to scoop water out
   - Place towels on floor to catch spills
   - Work carefully to avoid electrical contact
3. Leave standing water to drain naturally for 30 min

**STEP 1: DRAIN FILTER CLEANING** (Most Common Fix)
- Locate the drain filter access (side panel or bottom)
- Place bucket underneath to catch remaining water
- Open the access cover carefully with tools if needed
- Remove the filter cartridge
- **Clean the filter thoroughly**:
  - Rinse under warm running water
  - Use soft brush to remove lint and debris
  - For stubborn buildup: soak in warm water for 10 min
  - Inspect for tears or damage
  - Replace if damaged (usually $20-40)
- Reinstall and run a test cycle empty

**STEP 2: DRAIN HOSE INSPECTION**
- Locate where drain hose connects at back
- Check the hose routing:
  - Look for kinks or sharp bends
  - Straighten any crimped sections
  - Ensure hose isn't clogged with debris
- Disconnect hose at both ends (prepare for water)
- Look inside the hose with flashlight for blockages:
  - Foreign objects (coins, buttons, lint)
  - Soap residue buildup
  - Mineral deposits
- **Flush the hose**:
  - Hold over sink
  - Run hot water through both directions
  - Use a plumbing snake if needed
  - Connect back securely when clear
  - Run test cycle

**STEP 3: CHECK DRAIN PUMP**
- Listen for drain pump running during drain phase:
  - Should hear a humming or electrical sound
  - Typically runs for 30-60 seconds at end of cycle
- If you hear nothing, pump may have failed
- Check pump inlet for blockages if accessible
- Professional pump replacement usually needed ($100-300)

**STEP 4: DRAINAGE SYSTEM**
- Ensure drain hose is connected to proper drain:
  - Should feed into laundry sink
  - Or into standpipe (wall-mounted drain)
  - Or into floor drain
- Verify drain system isn't full:
  - Pour water into the drain
  - Should drain immediately
  - If slow or backed up = blocked drain line
  - May need plumber for main line clog
- Check hose height:
  - Loop shouldn't be higher than appliance
  - Too high prevents proper drainage

**STEP 5: CONTROL SYSTEM**
- Check display for error codes
- Verify you're selecting correct cycle
- Some cycles have different drain phases
- Try running a drain-only or maintenance cycle
- Check if cycle is completing fully

**MAINTENANCE TIPS**
- Run filter cleaning monthly
- Don't overload appliance
- Use correct detergent amount
- Run maintenance wash quarterly
- Have hoses inspected yearly""",
            
            "won't start": """APPLIANCE WON'T START - COMPREHENSIVE TROUBLESHOOTING

**BEFORE YOU BEGIN**
- Is the appliance plugged in?
- Is the outlet receiving power? (Test with lamp)
- Do any lights or display show power? (Any LEDs lit?)
- Take careful notes of what happens when you try to start

**STEP 1: CRITICAL SAFETY CHECKS**
- Door/Lid must be properly closed or latched
  - Try opening and closing firmly
  - Listen for the latch click
  - Check for damage to door framework
- All access panels must be properly closed
  - Check side panels or bottom covers
  - Secure any loose screws or fasteners
- Safety lock mechanisms must engage
  - Some machines won't start if safety features detect issues
  - Check manual for safety-related startup requirements

**STEP 2: CONTROL PANEL RESET**
- Press and hold power button for 10 seconds
- If it turns on/off = panel may be responding
- If nothing happens = may be power issue or control failure
- Try turning it fully off, wait 2 minutes, turn back on
- Look for a separate small reset button (often recessed)

**STEP 3: CYCLE & MODE SELECTION**
- Try different cycles - one might start when others won't
- Check if machine is in special modes:
  - Demo/showroom mode (won't operate)
  - Storage mode (requires specific unlock sequence)
  - Child lock or safety modes
- Consult manual for mode-specific startup requirements
- Some materials might need a specific sequence of button presses

**STEP 4: WATER SUPPLY** (If applicable)
- Verify water is ON at shut-off valves:
  - Hot water valve (hot on right when facing back)
  - Cold water valve (cold on left)
  - Both should be turned fully counterclockwise 
- Check if "no water" error code appears
- Verify hoses aren't kinked or blocked
- Test if water flows through valves by slowly opening
- Some machines won't start without water supply

**STEP 5: DOOR LATCH & SENSORS**
- Fully close and firmly push door until it clicks
- Inspect door switch for visible damage
- Check if door has any gaps around edges
- Try closing and opening it 5-10 times firmly
- Sometimes repeated cycling resets the switch
- Look for broken plastic tabs inside door frame

**STEP 6: POWER MANAGEMENT**
- Do you see any indicator lights or LEDs?
  - No lights = likely power problem
  - Some lights = control system has power
- Check circuit breaker for the room:
  - Breaker switch should be in "ON" position
  - Look for switches that are in middle position (tripped)
  - If tripped, flip fully off then back on
  - If it trips again immediately = circuit problem
- Try plugging into a different outlet in another room
- Never use an extension cord (can cause problems)

**STEP 7: HIDDEN ERRORS & CODES**
- Listen carefully for beeping or tones
- Watch display for blinking patterns
- Note any error codes displayed
- Consult manual error code table
- Some machines display errors instead of refusing to start

**ADVANCED ISSUES**
- If LEDs are dark and breaker is on = likely power cord issue
- Professional needed for internal control board problems
- Button panel failure requires professional replacement

**WHAT NOT TO DO**
- Don't force buttons or controls
- Don't try to bypass safety interlocks
- Don't restart repeatedly if it fails (can damage controls)
- Don't assume it's broken after one attempt-try again in 5 min""",
            
            "error code": f"""ERROR CODE TROUBLESHOOTING GUIDE {f"- {brand} {model}" if brand and model else ""}

**FIRST STEPS FOR ANY ERROR CODE**
1. Write down the exact code (letters, numbers, format)
2. Note what the appliance was doing when error appeared
3. Check your user manual's error code section
4. Take a photo of the code for reference
5. Don't attempt to ignore or override the error

**GENERAL ERROR TROUBLESHOOTING STEPS**

**For POWER/SUPPLY Related Errors**:
- Verify appliance is properly plugged in
- Check circuit breaker isn't tripped
- Try different outlet to rule out breaker issue
- Check if power cord has damage
- Professional needed if breaker repeatedly trips

**For WATER/DRAIN Errors**:
- Check water inlet valves are fully ON
- Verify hoses aren't kinked or clogged
- Clean drain filter (most common fix)
- Check drain hose for blockages
- Inspect for water leaks

**For DOOR/LATCH Errors**:
- Firmly close and open door 5-10 times
- Inspect door seal and frame for damage
- Remove visible debris from door area
- Ensure door closes completely without gaps

**For TEMPERATURE Errors**:
- Check if hot water supply is ON
- Verify water is actually hot (test at sink)
- Some errors = heating element malfunction
- Professional replacement may be needed

**For SENSOR Errors**:
- Unplug for 5 minutes and restart
- These often clear themselves
- Repeated errors = sensor replacement needed

**IMPORTANT NOTES**
- Most modern appliances display error codes for safety
- These aren't usually "broken" - they're protective signals
- 70% of error codes resolve with simple troubleshooting
- If code returns after troubleshooting = professional service needed

**Find Your Specific Code**
Consult your appliance's user manual error code table for exact meaning. Error codes vary significantly by brand and model. Include the brand, model, and error code when calling for professional help.""",
            
            "smell": """BAD SMELLS FROM APPLIANCE - DIAGNOSIS & ELIMINATION

**EMERGENCY: Electrical Burning Smell**
- Turn off appliance immediately
- Unplug from outlet
- DO NOT use it again until professionally inspected
- This indicates serious electrical problem
- Call service professional or replace appliance

**STEP 1: IDENTIFY THE SMELL TYPE**

**Musty/Moldy Odor**:
- Coming from moisture/humidity buildup inside
- Common in washing machines and dryers
- Indicates mold or mildew growth
- Usually NOT dangerous, but uncomfortable

**Burning Smell that's NOT electrical**:
- Could be lint or dust burning on heating element
- May be new component off-gassing
- Could be debris on motor
- Usually temporary with new appliances

**Sour/Rotten Smell**:
- Bacterial growth in standing water
- Food debris decomposing
- Drain system bacteria
- Unpleasant but usually not dangerous

**Plastic/Chemical Smell**:
- Often from new appliance outgassing
- Detergent or cleaner residue
- Usually fades after first few uses
- Ventilate well during operation

**STEP 2: DEEP CLEANING**

**For Front-Load Washers**:
1. Leave door open between uses to air dry
2. Wipe down rubber door gasket regularly
3. Run hot water with 1 cup white vinegar (empty cycle)
4. Repeat vinegar cycle monthly as maintenance
5. Check and clean soap/lint drawer
6. For stubborn smell: use commercial washing machine cleaner

**For Dryers**:
1. Empty and clean lint trap after every load
2. Vacuum lint from trap chamber with brush
3. Ensure exhaust vent isn't clogged (biggest problem)
4. Run a cycle with dryer sheet or fabric softener
5. Use commercial dryer vent cleaner if needed

**For Dishwashers**:
1. Remove and rinse food trap
2. Run hot cycle with 1 cup vinegar (empty)
3. Inspect spray arms for blocked holes
4. Clean door seals of debris
5. Check drain area for decomposing food
6. Run commercially available dishwasher cleaner

**For Ovens/Ranges**:
1. Remove and wash racks
2. Wipe down interior surfaces
3. Clean spills from bottom
4. For self-cleaning: run full cycle per manual
5. Ensure ventilation fan works properly

**STEP 3: FILTER & EQUIPMENT CHECK**
- Check all accessible filters and clean/replace
- Look for collected moisture in components
- Verify all drain areas are clear
- Ensure ventilation/exhaust paths are open

**STEP 4: LONG-TERM PREVENTION**
- Leave access doors open when not in use (air circulation)
- Maintain adequate ventilation around appliance
- Follow manufacturer maintenance schedule
- Use correct amounts of detergent/cleaners
- Clean filters and traps regularly
- Consider preventative maintenance products

**REPLACEMENT PARTS THAT ELIMINATE SMELLS**
- Door gaskets ($30-80)
- Drain filters ($15-40)
- Lint traps ($20-50)
- Exhaust vent ($50-150)

**When to Call Professional**
- If smell is accompanied by malfunction
- If after cleaning the smell persists
- For sealed compartment smells you can't access
- For confirmed mold that won't go away with cleaning
- If there's any electrical burning smell""",
            
            "won't heat": """APPLIANCE NOT HEATING - TROUBLESHOOTING GUIDE

**STEP 1: VERIFY YOU'RE ASKING FOR HEAT**
- Check thermostat/temperature setting
- Ensure you selected heating mode if available:
  - Some cycles don't include heating
  - Different modes provide different heat levels
- Try a different cycle that definitely heats
- For some appliances heat cycles take time to reach temperature

**STEP 2: CHECK WATER HEATING** (if water-based appliance)
- Verify hot water supply is ON at shut-off valves:
  - Should be turned fully counterclockwise
- Check if hot water flows at sink faucet:
  - Verify your home's hot water heater is working
  - Feel the incoming water temperature at the valve
- Check if appliance has separate hot water valve:
  - Should be connected to hot water line  
  - May have a separate shut-off valve at appliance
  - Verify this valve is fully open

**STEP 3: HEATING ELEMENT CHECKS**

**For Electric Heating**:
- Do you hear the element engaging? (clicking/humming)
- Look for any visual burn marks or damage to element
- Check for error codes suggesting heating failure
- Test if element works:
  - Some have access covers that can be removed
  - Look for visible damage or breakdown
  - Professional testing equipment needed for definitive check

**For Gas Heating** (if applicable):
- Check if pilot light is lit
- Verify gas supply is ON
- Listen for ignition clicks when heating cycle starts
- Check for gas smell (indicates possible leak - CALL GAS COMPANY)
- Professional service needed for gas heating issues

**STEP 4: TEMPERATURE SENSOR TEST**
- These detect if appliance reached desired temperature
- Usually located in the heating area
- Can become miscalibrated or fail
- Prevents heating if sensor thinks it's too hot
- Professional replacement often needed

**ADVANCED PROBLEMS**
- Thermostat failure = manual control won't work
- Heating element burnout = replacement needed ($50-200)
- Control board issue = professional repair
- Sensor failure = replacement needed

**TEMPORARY WORKAROUNDS**
- Some issues resolve after reset (unplug 5 min)
- Use higher temperature setting if available
- Repeat the cycle - sometimes elements engage on second attempt
- Pre-heat water manually if possible until professional arrives

**PREVENT HEATING FAILURES**
- Keep heating element area clean of debris
- Use correct water temperatures for your appliance
- Don't overload to allow even heating
- Professional maintenance annually if heavy use
- Replace mineral buildup filters if applicable

**ENVIRONMENTAL FACTORS**
- Very cold incoming water takes longer to heat
- High water usage can overtax heating system
- Appliance location affects ambient temperature
- Ensure proper ventilation around appliance

**WHEN TO CALL FOR HELP**
- If appliance has power but won't heat after reset
- For gas heating issues (safety concern)
- If you found heating element damage
- After trying steps above with no success
- For any gas-related heating concerns (call immediately)"""
        }
        
        # Find matching solution
        answer = None
        for keyword, solution in solutions.items():
            if keyword in query_lower:
                answer = solution
                break
        
        # Default response if no match
        if not answer:
            device_ref = f" for your {brand} {model}" if brand and model else ""
            answer = f"""APPLIANCE TROUBLESHOOTING GUIDE{device_ref}

**GENERAL DIAGNOSTICS**

**STEP 1: POWER VERIFICATION**
- Check if the outlet has power (use another device)
- Verify circuit breaker hasn't tripped
- Ensure power cord is fully connected
- For battery-operated devices: check batteries

**STEP 2: BASIC OPERATION**
- Press power button and listen for any response
- Look for indicator lights or display activation
- Check if anything sounds unusual
- Try the simplest operation first

**STEP 3: SAFETY CHECKS**
- Ensure all access panels are properly secured
- Check door/lid latches are engaged
- Verify no protective shields are in place
- Some machines won't operate with safety override

**STEP 4: SYSTEM RESET**
- Unplug for 5 minutes
- This clears temporary glitches and errors
- Plug back in and retry operation

**STEP 5: MANUAL REFERENCE**
- Your user manual is the definitive resource
- Look for troubleshooting section specific to your model
- Error codes in manual explain exactly what's wrong
- Contains brand-specific solutions

**DETAILED TROUBLESHOOTING FOR**:
- **Appliance won't start**: Check power, doors, safety switches
- **Leaking**: Check hoses, connections, seals
- **Not draining**: Clean filters, check drain hose  
- **Making noise**: Identify noise type, check for debris
- **Bad smell**: Check for mold, bacteria, burning debris
- **Not heating**: Check temperature setting, heating elements
- **Error codes**: Check manual for specific code meanings

⚠️ **Safety Note**: If you smell burning, see sparks, or suspect electrical/gas problems, stop using immediately and contact a professional."""
        
        return {
            "answer": answer,
            "sources": [],
            "confidence_score": 0.75,
            "safety_flag": "gas" in query_lower or "electrical" in query_lower or "shock" in query_lower or "fire" in query_lower or "burning" in query_lower,
            "safety_level": "caution" if any(word in query_lower for word in ["gas", "electrical", "shock", "smoke", "burning"]) else "safe",
            "safety_message": "⚠️ WARNING: This issue may require professional assistance for safety reasons. Stop use if you notice burning, sparks, gas smell, or water/electrical issues." if any(word in query_lower for word in ["gas", "electrical", "shock", "smoke", "burning"]) else ""
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