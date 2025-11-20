import asyncio
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from openai import OpenAI
from starlette.responses import StreamingResponse
from starlette.templating import Jinja2Templates

# Setup logging & load environment variables
logging.basicConfig(level=logging.INFO)
load_dotenv()

# Initialize FastAPI, templates, and OpenAI client
app = FastAPI()
templates = Jinja2Templates(directory="templates")
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.get("/")
def index_view(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


@app.get("/stream")
async def stream(message: str):
    try:
        completion = openai_client.responses.create(
            model="gpt-4o-mini",
            input=message,
            stream=True,
        )

        # Define an asynchronous generator to forward SSE events
        async def async_generator():
            yield "event: start\ndata: [START]\n\n"

            for event in completion:
                if event.type == "response.output_text.delta":
                    text = event.delta
                    yield f"data: {text}\n\n"
                if event.type == "response.completed":
                    total_tokens = event.response.usage.total_tokens
                    logging.info(f"Used tokens: {total_tokens}")
                await asyncio.sleep(0)

            yield "event: end\ndata: [END]\n\n"

        return StreamingResponse(
            async_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise HTTPException(
            detail=str(e),
            status_code=500,
        )
