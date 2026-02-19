# reputation_core.py

def calculate_reputation_score(agent_data: dict) -> int:
    """
    Calcula o score de reputação de um agente com base nos dados fornecidos.
    
    Args:
        agent_data (dict): Um dicionário contendo os dados do agente, como:
                           - 'moltbook_activity_score': int (0-100)
                           - 'transaction_volume_usd': float
                           - 'age_in_days': int
                           - 'positive_feedback_count': int
                           - 'negative_feedback_count': int
                           - 'x402_payments_made': int
                           - 'x402_payments_received': int

    Returns:
        int: O score de reputação do agente (0-100).
    """
    score = 0

    # Exemplo de lógica de cálculo (simplificada para começar)
    # Esta lógica será refinada nas próximas etapas

    # Atividade no Moltbook
    score += agent_data.get('moltbook_activity_score', 0) * 0.3

    # Volume de transações (ponderado)
    if agent_data.get('transaction_volume_usd', 0) > 1000:
        score += 20
    elif agent_data.get('transaction_volume_usd', 0) > 100:
        score += 10

    # Idade do agente
    if agent_data.get('age_in_days', 0) > 365:
        score += 15
    elif agent_data.get('age_in_days', 0) > 90:
        score += 5

    # Feedback
    positive_feedback = agent_data.get('positive_feedback_count', 0)
    negative_feedback = agent_data.get('negative_feedback_count', 0)
    
    if positive_feedback > 0 and negative_feedback == 0:
        score += 10
    elif positive_feedback > negative_feedback:
        score += 5
    elif negative_feedback > positive_feedback:
        score -= 5 # Penalidade por feedback negativo

    # Pagamentos x402
    if agent_data.get('x402_payments_received', 0) > 5:
        score += 10
    if agent_data.get('x402_payments_made', 0) > 5:
        score += 5

    # Garantir que o score esteja entre 0 e 100
    score = max(0, min(100, int(score)))

    return score


if __name__ == '__main__':
    # Exemplo de uso para teste
    print("\n--- Testando a lógica de reputação ---")

    # Agente com boa reputação esperada
    agent_good = {
        'moltbook_activity_score': 80,
        'transaction_volume_usd': 1500.0,
        'age_in_days': 500,
        'positive_feedback_count': 20,
        'negative_feedback_count': 0,
        'x402_payments_made': 10,
        'x402_payments_received': 15,
    }
    score_good = calculate_reputation_score(agent_good)
    print(f"Score para Agente Bom: {score_good}") # Esperado: Alto

    # Agente com reputação média esperada
    agent_medium = {
        'moltbook_activity_score': 50,
        'transaction_volume_usd': 200.0,
        'age_in_days': 120,
        'positive_feedback_count': 5,
        'negative_feedback_count': 1,
        'x402_payments_made': 3,
        'x402_payments_received': 2,
    }
    score_medium = calculate_reputation_score(agent_medium)
    print(f"Score para Agente Médio: {score_medium}") # Esperado: Médio

    # Agente com reputação baixa esperada
    agent_bad = {
        'moltbook_activity_score': 10,
        'transaction_volume_usd': 50.0,
        'age_in_days': 30,
        'positive_feedback_count': 1,
        'negative_feedback_count': 5,
        'x402_payments_made': 0,
        'x402_payments_received': 0,
    }
    score_bad = calculate_reputation_score(agent_bad)
    print(f"Score para Agente Ruim: {score_bad}") # Esperado: Baixo

    # Agente com dados mínimos
    agent_minimal = {
        'moltbook_activity_score': 0,
        'transaction_volume_usd': 0.0,
        'age_in_days': 0,
        'positive_feedback_count': 0,
        'negative_feedback_count': 0,
        'x402_payments_made': 0,
        'x402_payments_received': 0,
    }
    score_minimal = calculate_reputation_score(agent_minimal)
    print(f"Score para Agente Mínimo: {score_minimal}") # Esperado: Próximo de 0
