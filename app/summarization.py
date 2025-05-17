from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import google.generativeai as genai
import os
import logging

#create log file and format to log and level
logging.basicConfig(filename="summarize.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", filemode="a")

lenofwords = 0

# def chunk_text(text, max_words=10):
    # words = text.split()
    # lenofwords = len(words)
    # logging.info(f"length of story - {lenofwords}")
    
    # for i in range (0, len(words), max_words):
        # chunk = " ".join(words[i:i + max_words])
        # logging.info(f"Processing chunk: {chunk[:50]}...")  # Log first 50 chars
        # yield chunk
def chunk_text(text, max_words=100):
    words = text.split()
    lenofwords = len(words)
    logging.info(f"Total words: {lenofwords}")
    
    for index, i in enumerate(range(0, len(words), max_words)):
        chunk = " ".join(words[i:i + max_words])
        preview = chunk[:50] + "..." if len(chunk) > 50 else chunk
        logging.info(f"Chunk {index + 1}: {preview}")
        yield chunk

# Set up the generative AI model
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-1.5-flash")
#model = genai.GenerativeModel("gemini-1.5-flash-latest")

# breakpoint()
# Initialize FastAPI
router = APIRouter()

# Pydantic model for input validation
class StoryRequest(BaseModel):
    Story: str

# POST endpoint for generating a story based on the title
@router.post("/Summarize")
async def generate_story(request: StoryRequest):
  try:
    # Get the title from the request
    Story = request.Story
    
    # chunk input
    chunks = list(chunk_text(Story, max_words=100))
    summaries = []
    
    # breakpoint()
    # Generate story using the provided title
    for idx, chunk in enumerate(chunks):
        logging.info(f"Generating summary for chunk {idx + 1}")
        response = model.generate_content([f"Please summarize the following text:\n\n{chunk}"])
        summaries.append(response.text)
    # breakpoint()
    # Return the generated story as a response
    final_summary = " ".join(summaries)
    return {"Story": Story, "Summmary": final_summary}
    
  except Exception as e:
      return { "Error" : str(e) }

