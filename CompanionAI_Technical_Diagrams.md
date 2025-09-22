# CompanionAI - Technical Diagrams & Architecture Details
## For PowerPoint Technical Slides

---

## SYSTEM ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Web Browser   │  │   Mobile App    │  │   API Clients   │ │
│  │   (Streamlit)   │  │   (Future)      │  │   (Postman)     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND API LAYER                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   FastAPI       │  │   CORS Handler  │  │   Health Check  │ │
│  │   Server        │  │   Middleware    │  │   Endpoints     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Rate Limiting │  │   Metrics       │  │   Error         │ │
│  │   Middleware    │  │   Logging       │  │   Handling      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    COMPANIONAI CORE ENGINE                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Safety        │  │   Query         │  │   Response      │ │
│  │   Checker       │  │   Processor     │  │   Formatter     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                │                               │
│                                ▼                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              RAG PIPELINE                               │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │   │
│  │  │ Vector      │ │ Context     │ │ AI Response     │   │   │
│  │  │ Search      │ │ Building    │ │ Generation      │   │   │
│  │  └─────────────┘ └─────────────┘ └─────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA & AI LAYER                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   FAISS         │  │   Embeddings    │  │   Metadata      │ │
│  │   Vector DB     │  │   (NumPy)       │  │   (JSON)        │ │
│  │   652 chunks    │  │   384 dims      │  │   Source refs   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Ollama        │  │   Nvidia NIM    │  │   Template      │ │
│  │   (Local LLM)   │  │   (Cloud API)   │  │   Responses     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## RAG PIPELINE DETAILED FLOW

```
Step 1: QUERY PROCESSING
┌─────────────────────────────────────────────────────────────────┐
│ User Input: "My Samsung WF45 shows E3 error code"              │
│                             │                                   │
│                             ▼                                   │
│ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │
│ │   Query         │  │   Safety        │  │   Brand/Model   │   │
│ │   Cleaning      │  │   Pre-check     │  │   Extraction    │   │
│ │   & Validation  │  │   (Emergency)   │  │   (Samsung/WF45)│   │
│ └─────────────────┘  └─────────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
Step 2: VECTOR EMBEDDING & SEARCH
┌─────────────────────────────────────────────────────────────────┐
│ ┌─────────────────┐                                             │
│ │ Sentence        │ → [0.23, -0.45, 0.78, 0.12, -0.67, ...]   │
│ │ Transformer     │   384-dimensional vector                   │
│ │ Encoder         │                                             │
│ └─────────────────┘                                             │
│                             │                                   │
│                             ▼                                   │
│ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │
│ │   FAISS         │  │   Similarity    │  │   Top K         │   │
│ │   Index         │  │   Search        │  │   Results       │   │
│ │   (652 chunks)  │  │   (cosine)      │  │   (k=10)        │   │
│ └─────────────────┘  └─────────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
Step 3: CONTEXT AUGMENTATION
┌─────────────────────────────────────────────────────────────────┐
│ Retrieved Manual Chunks:                                        │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Chunk 1: "E3 error indicates drainage issue. Check drain   │ │
│ │ hose for kinks or blockages. Clean the drain filter..."    │ │
│ │ Source: Samsung WF45 Manual, Page 23                       │ │
│ │ Relevance: 0.92                                            │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Chunk 2: "Drainage problems common causes: 1. Clogged     │ │
│ │ filter 2. Kinked hose 3. Pump failure..."                 │ │
│ │ Source: Samsung Manual General, Page 45                    │ │
│ │ Relevance: 0.87                                            │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                             │                                   │
│                             ▼                                   │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │          PROMPT CONSTRUCTION                                │ │
│ │ "You are CompanionAI. Based on these manual excerpts:      │ │
│ │ [Manual Context] + User Question: [Query] → Generate       │ │
│ │ step-by-step troubleshooting instructions..."              │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
Step 4: AI GENERATION
┌─────────────────────────────────────────────────────────────────┐
│ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │
│ │   Ollama        │  │   Nvidia NIM    │  │   Template      │   │
│ │   (Primary)     │  │   (Backup)      │  │   (Fallback)    │   │
│ │   Local Model   │  │   Cloud API     │  │   Smart Rules   │   │
│ └─────────────────┘  └─────────────────┘  └─────────────────┘   │
│                             │                                   │
│                             ▼                                   │
│ Generated Response:                                             │
│ "E3 Error = Drainage Problem                                   │
│ 1. Check drain hose for kinks                                  │
│ 2. Clean drain filter (behind front panel)                     │
│ 3. Verify drain height (max 96 inches)                         │
│ 4. Reset machine (unplug 30 seconds)                           │
│ If problem persists, contact Samsung support."                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## SAFETY SYSTEM ARCHITECTURE

```
                    SAFETY-FIRST DETECTION PIPELINE
┌─────────────────────────────────────────────────────────────────┐
│                     QUERY INTAKE                               │
│               "I smell gas from my oven"                       │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                PATTERN MATCHING ENGINE                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Gas Patterns  │  │ Electrical      │  │   Water         │ │
│  │   • "smell gas" │  │ Patterns        │  │   Patterns      │ │
│  │   • "gas leak"  │  │ • "sparking"    │  │   • "flooding"  │ │
│  │   • "gas odor"  │  │ • "shock"       │  │   • "major leak"│ │
│  │   • "propane"   │  │ • "smoke"       │  │   • "water+elec"│ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                SAFETY LEVEL CLASSIFICATION                     │
│                                                                 │
│  🟢 SAFE          🟡 CAUTION       🟠 DANGER      🔴 EMERGENCY  │
│  Normal           Minor           Strong         Immediate      │
│  troubleshooting  warnings        alerts         evacuation    │
│                                                                 │
│  Examples:        Examples:       Examples:      Examples:      │
│  • Filter clean   • Water near    • Electrical   • Gas leaks   │
│  • Reset device   electrical      sparks         • Major flood │
│  • Check power    • Hot surfaces  • Smoke smell  • Fire risk   │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                 RESPONSE GENERATION OVERRIDE                   │
│                                                                 │
│  IF EMERGENCY DETECTED:                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  🚨 SAFETY OVERRIDE ACTIVATED 🚨                        │   │
│  │                                                         │   │
│  │  1. BYPASS all normal RAG processing                    │   │
│  │  2. RETURN immediate safety instructions                │   │
│  │  3. LOG emergency event for monitoring                  │   │
│  │  4. ESCALATE to emergency response team                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Emergency Response Template:                                   │
│  "🚨 GAS SAFETY EMERGENCY 🚨                                   │
│   1. DO NOT use electrical switches                            │
│   2. EVACUATE immediately                                      │
│   3. CALL gas company emergency line                           │
│   4. CALL 911 if necessary"                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## DATABASE SCHEMA & STRUCTURE

```
FAISS VECTOR DATABASE STRUCTURE
┌─────────────────────────────────────────────────────────────────┐
│                      embeddings.npy                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Vector 0: [0.23, -0.45, 0.78, ...] (384 dimensions)    │   │
│  │ Vector 1: [0.12, 0.67, -0.34, ...] (384 dimensions)    │   │
│  │ Vector 2: [-0.89, 0.23, 0.56, ...] (384 dimensions)    │   │
│  │ ...                                                     │   │
│  │ Vector 651: [0.45, -0.12, 0.89, ...] (384 dimensions)  │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      faiss.index                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ FAISS Index (IndexFlatIP - Inner Product)              │   │
│  │ • 652 vectors indexed                                  │   │
│  │ • 384 dimensional space                                │   │
│  │ • Cosine similarity search                             │   │
│  │ • Sub-second query time                                │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    metadata.jsonl                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ {"id": "samsung_wf45_0",                               │   │
│  │  "text": "E3 error indicates drainage issue...",       │   │
│  │  "source": "samsung_manual.pdf",                       │   │
│  │  "brand": "Samsung",                                   │   │
│  │  "model": "WF45",                                      │   │
│  │  "page": 23,                                           │   │
│  │  "filename": "samsung_wf45_manual.pdf"}                │   │
│  │                                                         │   │
│  │ {"id": "lg_microwave_1",                               │   │
│  │  "text": "Turntable rotation problems...",             │   │
│  │  "source": "lg_microwave.pdf",                         │   │
│  │  "brand": "LG",                                        │   │
│  │  "model": "MS2595",                                    │   │
│  │  "page": 45}                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

BRAND/MODEL DISTRIBUTION:
┌──────────────┬──────────┬─────────────────────────────────┐
│ Brand        │ Count    │ Models                          │
├──────────────┼──────────┼─────────────────────────────────┤
│ Samsung      │ 156      │ WF45, WF42H5200, RF23J9011     │
│ LG           │ 142      │ MS2595DIS, WM3488HW, LRFVS3006 │
│ Whirlpool    │ 127      │ WOS51EC0HS, WFW92HEFW          │
│ Bosch        │ 98       │ BGL72294, WAT28401UC           │
│ Philips      │ 89       │ HR7761, HD9641/96              │
│ Other        │ 40       │ GE, KitchenAid, Frigidaire     │
└──────────────┴──────────┴─────────────────────────────────┘
```

---

## PERFORMANCE METRICS DASHBOARD

```
                    COMPANIONAI PERFORMANCE METRICS
┌─────────────────────────────────────────────────────────────────┐
│                        RESPONSE TIMES                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Query         │  │   Vector        │  │   AI            │ │
│  │   Processing    │  │   Search        │  │   Generation    │ │
│  │   0.1s          │  │   0.3s          │  │   1.4s          │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                    Total Average: 1.8 seconds                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       ACCURACY METRICS                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Relevant      │  │   Safety        │  │   User          │ │
│  │   Chunk         │  │   Detection     │  │   Satisfaction  │ │
│  │   Retrieval     │  │   Accuracy      │  │   Rate          │ │
│  │   82%           │  │   98%           │  │   78%           │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      SYSTEM RESOURCES                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Memory        │  │   CPU           │  │   Storage       │ │
│  │   Usage         │  │   Usage         │  │   Usage         │ │
│  │   5.2GB/8GB     │  │   45% avg       │  │   1.8GB/2GB    │ │
│  │   (65%)         │  │                 │  │   (90%)         │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     SAFETY STATISTICS                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Emergency     │  │   Safety        │  │   False         │ │
│  │   Detections    │  │   Overrides     │  │   Positives     │ │
│  │   23 total      │  │   23 triggered  │  │   <2%           │ │
│  │   (this month)  │  │   (100% rate)   │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## DEPLOYMENT ARCHITECTURE

```
                       PRODUCTION DEPLOYMENT
┌─────────────────────────────────────────────────────────────────┐
│                      LOAD BALANCER                             │
│                    (nginx / Cloudflare)                        │
└─────────────────────┬───────────────────────────────────────────┘
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Frontend   │ │  Frontend   │ │  Frontend   │
│  Instance 1 │ │  Instance 2 │ │  Instance 3 │
│ (Streamlit) │ │ (Streamlit) │ │ (Streamlit) │
└─────────────┘ └─────────────┘ └─────────────┘
         │            │            │
         └────────────┼────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND API CLUSTER                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   FastAPI       │  │   FastAPI       │  │   FastAPI       │ │
│  │   Instance 1    │  │   Instance 2    │  │   Instance 3    │ │
│  │   (Primary)     │  │   (Secondary)   │  │   (Tertiary)    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SHARED DATA LAYER                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   FAISS         │  │   Embeddings    │  │   Metadata      │ │
│  │   Index         │  │   Cache         │  │   Database      │ │
│  │   (Read-Only)   │  │   (Redis)       │  │   (PostgreSQL)  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Ollama        │  │   Model         │  │   Logs &        │ │
│  │   Cluster       │  │   Cache         │  │   Metrics       │ │
│  │   (GPU/CPU)     │  │   (Memcached)   │  │   (ELK Stack)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

SCALING CONFIGURATION:
• Auto-scaling: 1-10 instances based on load
• Database: Read replicas for FAISS queries
• Caching: Redis for frequent responses
• Monitoring: Prometheus + Grafana
• Backup: Daily snapshots to cloud storage
```

This comprehensive technical documentation provides all the visual elements and detailed explanations you need for your PowerPoint presentation. You can use these diagrams and architectures to create professional slides that demonstrate the technical depth and innovation of your CompanionAI project.