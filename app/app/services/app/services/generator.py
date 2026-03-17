from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from app.config import settings

class ContentEngine:
    def __init__(self):
        # Initialize LLM (assuming local inference or API wrapper)
        self.tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(settings.MODEL_NAME)
        self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

    def generate_indepth_notes(self, raw_text: str) -> str:
        prompt = f"""
        You are an expert academic writer. Convert the following raw study material into detailed, 
        in-depth study notes. Include headings, sub-topics, detailed explanations, and highlighted definitions.
        
        RAW MATERIAL:
        {raw_text[:4000]} 
        """
        result = self.pipe(prompt, max_new_tokens=2000)
        return result[0]['generated_text']

    def generate_revision_notes(self, raw_text: str) -> str:
        prompt = f"""
        You are an exam revision expert. Compress the following text into rapid revision notes.
        Use bullet points and arrow format (→). Only keep critical facts.
        
        CONTENT:
        {raw_text[:4000]}
        """
        result = self.pipe(prompt, max_new_tokens=1000)
        return result[0]['generated_text']
