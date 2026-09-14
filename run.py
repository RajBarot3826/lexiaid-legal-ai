import uvicorn
import os
import sys

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")
    print("==================================================")
    print("LexiAid: AI for Legal Assistance & Access")
    print(f"Starting server at: http://{host}:{port}")
    print(f"API Documentation: http://{host}:{port}/docs")
    print("==================================================")
    uvicorn.run("backend.app:app", host=host, port=port, reload=False)
