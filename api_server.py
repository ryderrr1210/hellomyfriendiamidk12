from fastapi      import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from urllib.parse import urlparse, ParseResult
from pydantic     import BaseModel
from core         import Grok
from uvicorn      import run
from json         import dumps


app = FastAPI()

class ConversationRequest(BaseModel):
    proxy: str | None = None
    message: str
    model: str = "grok-4.20-expert"
    system_prompt: str | None = None
    extra_data: dict | None = None

def format_proxy(proxy: str) -> str:
    
    if not proxy.startswith(("http://", "https://")):
        proxy: str = "http://" + proxy
    
    try:
        parsed: ParseResult = urlparse(proxy)

        if parsed.scheme not in ("http", ""):
            raise ValueError("Not http scheme")

        if not parsed.hostname or not parsed.port:
            raise ValueError("No url and port")

        if parsed.username and parsed.password:
            return f"http://{parsed.username}:{parsed.password}@{parsed.hostname}:{parsed.port}"
        
        else:
            return f"http://{parsed.hostname}:{parsed.port}"
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid proxy format: {str(e)}")

@app.post("/ask")
async def create_conversation(request: ConversationRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    proxy = format_proxy(request.proxy) if request.proxy else None
    
    try:
        answer: dict = Grok(request.model, proxy).start_convo(request.message, request.extra_data, request.system_prompt)

        return {
            "status": "success",
            **answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/ask/stream")
async def create_conversation_stream(request: ConversationRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    proxy = format_proxy(request.proxy) if request.proxy else None

    def event_generator():
        try:
            grok = Grok(request.model, proxy)
            for event in grok.start_convo_stream(request.message, request.extra_data, request.system_prompt):
                yield f"data: {dumps(event)}\n\n"
        except Exception as e:
            yield f"data: {dumps({'type': 'error', 'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )

if __name__ == "__main__":
    run("api_server:app", host="0.0.0.0", port=6970)