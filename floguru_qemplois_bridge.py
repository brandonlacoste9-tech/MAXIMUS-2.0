import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Bridge logic - locate q-emplois dynamically
SCRIPTS_DIR = Path(__file__).parent.resolve()
DEFAULT_Q_PATH = SCRIPTS_DIR.parent / "q-emplois"
Q_EMPLOIS_PATH = Path(os.getenv("Q_EMPLOIS_PATH", str(DEFAULT_Q_PATH)))

sys.path.append(str(Q_EMPLOIS_PATH / "openclaw" / "skills"))

try:
    from qemplois.utils import parse_french_date, parse_french_time
except ImportError:
    # High-level fallback for the demo
    def parse_french_date(d): return "2026-03-20"
    def parse_french_time(t): return "14:00"

class FloguruDispatchBridge:
    """The brain that bridges natural talk to Q-emplois service engine."""
    
    def process_natural_request(self, user_text: str):
        print(f"🧠 FLOGURU DISPATCH: Processing request -> '{user_text}'")
        
        # In a real scenario, this would be an LLM call to extract intent
        # Here we demonstrate the mapping
        intent_mapping = {
            "fuit": "plomberie",
            "électricité": "électricité",
            "panne": "électricité",
            "nettoyer": "nettoyage",
            "déménager": "déménagement"
        }
        
        extracted_service = None
        for keyword, service in intent_mapping.items():
            if keyword in user_text.lower():
                extracted_service = service
                break
        
        if not extracted_service:
            return "❌ I couldn't identify the service type. Could you specify if it's plumbing, electrical, etc.?"
            
        print(f"✅ Service identified: {extracted_service.upper()}")
        
        # Demo of the Q-emplois structured payload
        payload = {
            "service_type": extracted_service,
            "status": "PROACTIVE_DISPATCH",
            "source": "FLOGURU_ADMIN",
            "summary": user_text
        }
        
        print(f"📝 Q-EMPLOIS PAYLOAD GENERATED:")
        print(payload)
        return payload

if __name__ == "__main__":
    bridge = FloguruDispatchBridge()
    # Test with a natural Quebec-style request
    bridge.process_natural_request("Mon lavabo fuit depuis ce matin à Pointe-Claire!")
