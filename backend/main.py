"""
Idea Factory - Backend API
FastAPI server for generating, refining, and visualizing ideas using Claude API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from anthropic import Anthropic

app = FastAPI(title="Idea Factory API", version="1.0.0")

# CORS middleware for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Anthropic client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


class GenerateRequest(BaseModel):
    topic: str


class RefineRequest(BaseModel):
    idea: str


class VisualizeRequest(BaseModel):
    ideas: List[str]
    topic: str


class GenerateResponse(BaseModel):
    ideas: List[str]


class RefineResponse(BaseModel):
    plan: str


class VisualizeResponse(BaseModel):
    visualization: str


@app.get("/")
async def root():
    return {"message": "Idea Factory API", "version": "1.0.0"}


@app.post("/generate", response_model=GenerateResponse)
async def generate_ideas(request: GenerateRequest):
    """
    Generate 10 novel, cross-disciplinary ideas based on user input
    """
    try:
        prompt = f"""Generate 10 creative, actionable ideas combining {request.topic}.
Each idea should be unique, specific, and formatted as a bullet point.
Avoid generic suggestions. Focus on novel cross-disciplinary approaches.

Format each idea as:
- [Idea title]: [Brief description]

Be creative and think outside the box!"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract ideas from response
        response_text = message.content[0].text
        ideas = [line.strip() for line in response_text.split('\n') if line.strip().startswith('-')]

        # Ensure we have at least some ideas
        if not ideas:
            ideas = response_text.split('\n')
            ideas = [idea.strip() for idea in ideas if idea.strip()]

        return GenerateResponse(ideas=ideas[:10])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ideas: {str(e)}")


@app.post("/refine", response_model=RefineResponse)
async def refine_idea(request: RefineRequest):
    """
    Refine a selected idea into a step-by-step plan with tasks, challenges, and resources
    """
    try:
        prompt = f"""Refine the following idea into a detailed plan: "{request.idea}".

Output a markdown table with columns: Task | Challenges | Resources.
Include 3-5 tasks, 2-3 challenges per task, and specific resources/tools.

Make it actionable and practical."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        plan = message.content[0].text

        return RefineResponse(plan=plan)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refining idea: {str(e)}")


@app.post("/visualize", response_model=VisualizeResponse)
async def visualize_ideas(request: VisualizeRequest):
    """
    Format ideas into a Mermaid.js mind map
    """
    try:
        ideas_text = "\n".join(request.ideas)

        prompt = f"""Format the following ideas into a Mermaid.js mind map:

{ideas_text}

Root node: {request.topic}

Create a clean mind map using mermaid syntax. Format it as:

```mermaid
mindmap
  root(({request.topic}))
    [Idea category or title]
      Specific idea
    [Another category]
      Another idea
```

Make it visually organized and clear."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        visualization = message.content[0].text

        return VisualizeResponse(visualization=visualization)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating visualization: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
