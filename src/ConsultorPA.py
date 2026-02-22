from dotenv import load_dotenv
import os, json

class ConsultorPA:
    
    def __init__(self):
        load_dotenv()
        self.token = None
        
    def cargar_token(self):
        archivo_tokens= os.getenv('TOKENS_FILE')
        if os.path.exists(archivo_tokens):
            with open(archivo_tokens, 'r') as f:
                data = json.load(f)
                self.token = data.get('jwt')
        return None
    
        
    