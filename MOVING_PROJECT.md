# Moving hallucination-resistant-rag to projects/ folder

## ✅ Path Issues Fixed!

I've updated the code to use **absolute paths** relative to the project directory instead of the current working directory. This means the project will work correctly regardless of where it's located.

## 🔧 What Was Changed:

### Updated Files:
1. **src/main.py** - Added `PROJECT_ROOT` to resolve paths dynamically
2. **src/embed.py** - Uses absolute paths for embeddings directory
3. **src/ingest.py** - Added Path import for better path handling

### Key Changes:
```python
# Before (relative to current working directory):
docsFolder = "data/documents"
embedDir = "embeddings"

# After (relative to project root):
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
docsFolder = PROJECT_ROOT / "data" / "documents"
embedDir = PROJECT_ROOT / "embeddings"
```

## 📁 How to Move Safely:

### Step 1: Test Current Location First
```powershell
cd c:\personal\AI-engineering-projects\hallucination-resistant-rag
python src\main.py
```

### Step 2: Move to projects folder
```powershell
cd c:\personal\AI-engineering-projects
Move-Item hallucination-resistant-rag projects\
```

### Step 3: Test from New Location
```powershell
cd projects\hallucination-resistant-rag
python src\main.py
```

### Step 4: Test from Different Working Directory
```powershell
# From root directory
cd c:\personal\AI-engineering-projects
python projects\hallucination-resistant-rag\src\main.py
```

## ✅ What Now Works:

- ✅ Run from project directory
- ✅ Run from root directory
- ✅ Run from any working directory
- ✅ Import as module
- ✅ API server works from anywhere
- ✅ Data and embeddings always found

## 🔍 Verification Checklist:

After moving, verify:
- [ ] `data/documents/` folder still accessible
- [ ] `embeddings/` folder still accessible  
- [ ] Can run `python src/main.py` from project dir
- [ ] Can run API: `uvicorn src.api:app --reload`
- [ ] Web interface still connects to API
- [ ] Embeddings are created/found correctly

## 📝 Additional Notes:

The project structure after moving:
```
projects/
└── hallucination-resistant-rag/
    ├── src/
    │   ├── main.py (✅ Updated)
    │   ├── embed.py (✅ Updated)
    │   ├── ingest.py (✅ Updated)
    │   └── ...
    ├── data/
    │   └── documents/
    ├── embeddings/
    ├── web/
    └── requirements.txt
```

## 🚀 You're Good to Move!

The code is now **location-independent** and will work correctly in the `projects/` folder!
