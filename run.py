import uvicorn
import os
import sys

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"==================================================")
    print(f"⚖️  LexiAid: AI for Legal Assistance & Access")
    print(f"🚀 Starting server at: http://{host}:{port}")
    print(f"📄 API Documentation: http://{host}:{port}/docs")
    print(f"==================================================")
    uvicorn.run("backend.app:app", host=host, port=port, reload=False)
