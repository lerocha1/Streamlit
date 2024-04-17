import openai

def retorna_resposta_modelo(mensagens, openai_key, modelo="gpt-3.5-turbo", temperatura=0, stream=False):
    # Executa a conversação com o modelo
    openai.api_key = openai_key
    response = openai.ChatCompletion.create(
        model=modelo,
        messages=mensagens,
        temperature=temperatura,
        stream=stream
    )
    return response