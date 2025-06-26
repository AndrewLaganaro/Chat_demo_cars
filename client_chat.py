import requests
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


def load_model():
    
    """ Load the pre-trained model and tokenizer. """
    
    print("🔽 Loading model and tokenizer...")
    
    try: 
        
        device_name = "cuda" if torch.cuda.is_available() else None
        
        if device_name is None:
            
            raise RuntimeError("No GPU available. Please check your CUDA installation.")
        
        device = torch.device(device_name)
        
    except Exception as Error:
        
        print(f"Error verifying GPU: {Error}")
        
        raise Error
    
    tokenizer = AutoTokenizer.from_pretrained("./Models")
    model = AutoModelForCausalLM.from_pretrained("./Models") #torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
    
    print("✅ Model and tokenizer loaded successfully.")
    
    model = model.to(device)
    
    current_device = torch.cuda.is_available()
    device_name = torch.cuda.get_device_name(0)
    
    print(f"Current device: {device_name} (CUDA available: {current_device})")
    
    return tokenizer, model, device


def get_chat_answer(messages, tokenizer, model, device):
    
    """Generate a chat answer based on the provided messages."""
    
    Chat_answer = ""
    
    prompt = tokenizer.apply_chat_template(messages, tokenize = False, add_generation_prompt = True)
    inputs = tokenizer(prompt, return_tensors = "pt").to(device)
    
    output = model.generate(**inputs,
                            max_new_tokens = 300,
                            temperature = 0.73,
                            do_sample = True
                                )
    
    decoded = tokenizer.decode(output[0], skip_special_tokens=False)
        
    if "<|assistant|>" in decoded:
        
        Chat_answer = decoded.split("<|assistant|>")[-1].strip()
        
        if "</s>" in Chat_answer:
            
            Chat_answer = Chat_answer.rstrip("</s>").strip()
        
    else:
        
        Chat_answer = decoded.strip()
        
    return Chat_answer


def build_enrich_answer(table_markdown, tokenizer, model, device):
    
    messages = [
        {"role": "system", "content": """
        Você é um especialista em carros. O cliente recebeu uma tabela com modelos semelhantes. Sua tarefa é:
        1. Mostrar a tabela recebida, idêntica a original, inalterada.
        2. Comparar os modelos listados, destacando diferenças em motor, câmbio, ano, combustível e preço.
        3. Segurir usos de cada modelo, como conforto, passeio, espaço interno, se é ideal para família
        Seja claro, objetivo e amigável. Use apenas as informações da tabela.
        Seu formato de resposta deve ser:
        <|começodaresposta|>
        <|assistant|>
        <|Introdução amigável, como "Certo, tenho alguns modelos para você!"|>
        <|table|>
        <|comment|> deve conter uma análise comparativa dos modelos, destacando diferenças e usos recomendados.
        <|fimdaresposta|>
        Note que você não deve alterar a tabela recebida, apenas comentá-la.
        Note que você não deve incluir os caracteres '<|assistant|>', '<|' ou '|>' na resposta final, nem no comentário, nem na tabela, nem na introdução.
        Note que você não deve incluir os caracteres '<|começodaresposta|>' ou '<|fimdaresposta|>' na resposta final, nem no comentário, nem na tabela, nem na introdução.
            """},
        
    {"role": "user", "content": f"""
        Tabela recebida:
        {table_markdown}
        
        Mostre a tabela e comente as diferenças entre os modelos, por favor!
    """}
                ]
    
    return get_chat_answer(messages, tokenizer, model, device)


def model_prompts(kind = None):
    
    Starting_prompt = ""
    
    if kind == "Car_chat":
        
        Starting_prompt =  """
        
            Você é um assistente que ajuda clientes a escolher carros.
            Se apresente de forma amigável de início, e peça os dados de <|Marca|> e <|Tipo|> do carro.
            Diga que essas informações são necessárias para buscar os modelos de carros.
            Ao receber uma tabela com diferentes modelos, comente de forma amigável e informativa quais são as diferenças ou destaques.
            Suas respostas sempre devem ser em português."""
                
    return Starting_prompt


def build_starting_answer(tokenizer, model, device, first_time = False):
    
    if first_time:
        
        messages = [
            {"role": "system", "content": "Nova conversa iniciada. Aguarde por novo usuário com uma nova pergunta."},
            {"role": "system", "content": model_prompts("Car_chat")},
            # Molde de conversa, já que o modelo é pequeno
            {"role": "user", "content": "Olá! Estou procurando um carro, pode me ajudar?"},
            {"role": "assistant", "content": "Claro! Posso te ajudar a encontrar o carro ideal. Por favor, me diga a marca e o tipo (urbano ou estrada) do carro que você procura. Essas informações são necessárias para buscar os modelos de carros."},
            {"role": "user", "content": "Estou pensando em um carro da Marca Nissan, Tipo estrada."},
            {"role": "assistant", "content": "Aqui estão alguns modelos que encontrei:\n\n| Marca | Tipo | Modelo | Motor | Portas | Cor | Câmbio | Ano | Combustível | Preco |\n|--------|--------|--------|--------|--------|-----|---------|------|-------------|--------|\n| Nissan | Estrada | Frontier | 2.3 Turbo Diesel | 4 | Prata | Automático | 2021 | Diesel | R$ 250.000 |\n| Nissan | Estrada | Kicks | 1.6 Flex | 4 | Branco | CVT | 2022 | Flex | R$ 110.000 |\n\nEsses são alguns dos modelos disponíveis.\n\n\
            Comparando os modelos, a Frontier é uma picape robusta, ideal para quem precisa de força e espaço, enquanto o Kicks é um SUV compacto, mais voltado para conforto e economia. Qual deles te interessa mais?"},
            {"role": "user", "content": "Gostei do Kicks, obrigado!"},
            {"role": "assistant", "content": "De nada! O Kicks é uma ótima escolha. Se precisar de mais informações ou ajuda com outra coisa, é só avisar!"},
            {"role": "system", "content": "Conversa encerrada. Você não tem mais informações sobre carros no momento. As informações da conversa anterior foram apagadas e esquecidas por você. Aguarde por novo usuário com uma nova pergunta."},
                    ]
        
    if not first_time:
        
        messages = [
            {"role": "system", "content": "Nova conversa iniciada. Aguarde por novo usuário com uma nova pergunta."},
            {"role": "system", "content":  model_prompts("Car_chat")},
            {"role": "user", "content": "Olá! Estou procurando um carro, pode me ajudar? Se apresente para que eu saiba que você é um assistente de carros!"},
                    ]
    
    return get_chat_answer(messages, tokenizer, model, device)


def build_table(car_data):
    
    if not car_data:
        
        return "Nenhum carro encontrado."
    
    lines  =  [ "| Marca | Tipo | Modelo | Motor | Portas | Cor | Câmbio | Ano | Combustível | Preco |",
                "|--------|--------|--------|--------|--------|-----|---------|------|-------------|--------|"]
    
    for car in car_data:
        
        lines.append(f"| {car['marca']} | {car['tipo']} | {car['modelo']} | {car['motor']} | {car['portas']} | {car['cor']} | {car['cambio']} | {car['ano']} | {car['combustivel']} | {car['preco']} |")
        
    table = "\n".join(lines)
    
    return table


def extract_user_query_info(query_content):
    
    query_content = query_content.lower()
    
    brands = ['fiat', 'ford', 'chevrolet', 'volkswagen', 'honda', 'mitsubishi', 'toyota', 'nissan', 'hyundai', 'kia']
    types = ['urbano', 'estrada']
    
    brand = next((content.capitalize() for content in brands if content in query_content), None)
    type_ = next((content for content in types if content in query_content), None)
    
    return brand, type_


def client_chat(tokenizer, model, device):
    
    print("Type 'exit' or 'sair' to end the chat.\n")
    
    first_time = True
    
    Bot_answer = build_starting_answer(tokenizer, model, device, first_time = True)
    
    while True:
        
        Bot_answer = build_starting_answer(tokenizer, model, device, first_time = not first_time) # Get the starting answer from the model
        
        print("\nBot:", Bot_answer)
        
        user_query = input("User: ").strip()
        
        if user_query.lower() in ['exit', 'sair']:
            
            print("Ending the chat. Goodbye!")
            
            break
        
        marca, tipo = extract_user_query_info(user_query)
        
        if not all([marca, tipo]):
            
            print("Bot:\nInforme marca e tipo (urbano/estrada)")
            
            continue
        
        payload =  {"action": "car_search",
                    "required_fields": ["marca", "tipo"],
                    "params":  {"marca": marca,
                                "tipo": tipo}
                        }
        
        try:
            
            Mcp_call = requests.post("http://localhost:5000/mcp", json = payload)
            data = Mcp_call.json()
            
        except Exception as Error:
            
            print(f"Bot:\nErro na conexão com o MCP server: {Error}")
            
            continue
        
        retrieved_mcp_table = build_table(data.get("carros", []))
        
        # ## print("\nBot:\n" + retrieved_mcp_table) # Show the retrieved table
        
        Bot_answer = build_enrich_answer(retrieved_mcp_table, tokenizer, model, device) # Enriches the answer with the retrieved table
        
        print("\nBot:", Bot_answer)
        print("\n" + "-"*40 + "\n")



if __name__ == "__main__":
    
    print("Starting the car chat client...\n")
    
    tokenizer, model, device = load_model()
    
    client_chat(tokenizer, model, device)