from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import google.generativeai as gai
import os

# Initialize FastAPI
router = APIRouter()

# Set up the generative AI model
gai.configure(api_key="***REMOVED***")  
model = gai.GenerativeModel("gemini-1.5-flash")

# Pydantic model for input validation
class StoryRequest(BaseModel):
    title: str

# POST endpoint for generating a story based on the title
@router.post("/story")
async def generate_story(request: StoryRequest):
    # Get the title from the request
    title = request.title
    #title = "A day in the life of a cat"
    
    # Generate story using the provided title
    #breakpoint()
    response = model.generate_content(f"Write a very short story about a {title}")
    # breakpoint()
    
    # Return the generated story as a response
    return {"title": title, "story": response.text}

