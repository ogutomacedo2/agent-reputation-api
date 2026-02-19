# main.py
from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import uvicorn
from reputation_core import calculate_reputation_score

app = FastAPI(
    title="Agent Trust & Reputation API",
    description="API para verificar a reputação de agentes de IA usando o protocolo x402.",
    version="1.0.0"
)

# Modelo de dados para a entrada da API
class AgentQuery(BaseModel):
    agent_id: str
    moltbook_activity_score: Optional[int] = 0
    transaction_volume_usd: Optional[float] = 0.0
    age_in_days: Optional[int] = 0
    positive_feedback_count: Optional[int] = 0
    negative_feedback_count: Optional[int] = 0
    x402_payments_made: Optional[int] = 0
    x402_payments_received: Optional[int] = 0

# Configurações do x402 (Simuladas para este exemplo)
X402_PAYMENT_ADDRESS = "0x53e585d65a6DE5ac14C09774C9844B4909Fb8cFD" # Substitua pela sua carteira Base
PRICE_PER_QUERY = "0.05" # USDC

@app.get("/")
def read_root():
    return {
        "message": "Bem-vindo à Agent Trust & Reputation API!",
        "payment_protocol": "x402",
        "payment_address": X402_PAYMENT_ADDRESS,
        "price_per_query_usdc": PRICE_PER_QUERY
    }

@app.post("/get-reputation")
async def get_reputation(
    query: AgentQuery,
    x_402_payment_token: Optional[str] = Header(None)
):
    """
    Endpoint principal que retorna o score de reputação.
    Exige um token de pagamento x402 válido no Header.
    """
    
    # Validação simplificada do protocolo x402
    # Na vida real, aqui verificaríamos na blockchain se o token é válido
    if not x_402_payment_token:
        raise HTTPException(
            status_code=402, 
            detail=f"Pagamento Necessário. Envie {PRICE_PER_QUERY} USDC para {X402_PAYMENT_ADDRESS} via protocolo x402."
        )

    # Se o pagamento for "validado", calculamos o score
    score = calculate_reputation_score(query.dict())
    
    # Definir o nível de confiança com base no score
    trust_level = "Baixo"
    if score >= 80:
        trust_level = "Muito Alto"
    elif score >= 60:
        trust_level = "Alto"
    elif score >= 40:
        trust_level = "Médio"

    return {
        "agent_id": query.agent_id,
        "reputation_score": score,
        "trust_level": trust_level,
        "status": "success",
        "payment_confirmed": True
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
