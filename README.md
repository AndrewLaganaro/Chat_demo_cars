# 🧠 Car Assistant Chat (Demo com LLM local + MCP)

Este projeto é uma demo mínima que simula um chat entre um cliente e um assistente de carros, que faz consultas a um servidor MCP (Model Context Protocol) e simula um RAG básico obtendo informações de um servidor e usando-as para enriquecer a resposta do chat.

---

## 🚗 O que este projeto faz?

- O usuário conversa com um assistente via terminal.
- O assistente coleta informações mínimas obrigatórias: **Marca** e **Tipo** do carro (urbano ou estrada).
- Uma requisição é feita ao servidor **MCP**, que busca todos os carros da mesma marca e tipo.
- O modelo LLM gera uma resposta comentando a tabela recebida e comparando os carros da mesma marca.

Este projeto usa o modelo:

> ✅ `TinyLlama/TinyLlama-1.1B-Chat-v1.0`  
- Pequeno, leve, e instruído para chat — ideal para máquinas locais com VRAM limitada.
- Infelizmente, teve um desempenho bem decepcionante com o que era esperado dados os chats atuais na web, uma abordagem com API da OpenAI tornaria isso muito mais fácil, e os problemas abordados seriam bem menores
- Modelos menores são pouco otimizados para tarefas de chat, eles podem apresentar comportamento repetitivo (repetir uma rotina ou uma história, se ela foi dada num prompt de instrução inicial), alteração de idioma numa mesma resposta, reproduzir o prompt de instrução mesmo quando claramente dito para não fazer isso, e outros problemas que não são esperados em modelos maiores.
- Modelos maiores por outro lado funcionam plenamente em chats, mas exigem uma GPU com pelo menos 16GB de VRAM, o que não é o caso da maioria dos usuários, nem mesmo do autor deste projeto.
- Uma abordagem com API geraria outras preocupações menores em relação a contexto de resposta de modelo, embora prompts corretos ainda sejam úteis, mas daria mais espaço a outros pontos relacionados ao código em si, modularização, classes, aplicações RAG de verdade com vetorização e Vector Stores (como não é o caso aqui), e outras melhorias em funcionalidades, mas que não são o foco deste projeto.

---

## 📦 Requisitos

- Python 3.10 ou superior
- CUDA instalado (GPU obrigatória para rodar localmente o modelo com desempenho aceitável)
- NVIDIA GPU com pelo menos **6GB de VRAM** (recomendada: 8GB+)
- A GPU usada nos testes foi uma **NVIDIA GeForce RTX 3060 Ti**

---

## 💻 Setup (passo a passo)

1. **Clone ou baixe este repositório**

2. **Crie e ative um ambiente virtual**
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```
3.1 **Instale o PyTorch com suporte a CUDA**
```bash
https://pytorch.org/get-started/locally/
```

3.2 **Instale o CUDA Toolkit**
    - Siga as instruções de instalação do [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) para sua plataforma.

4. **Teste sua GPU com CUDA**
```bash
python test_cuda.py
```
5. **Baixe o modelo de linguagem**
```bash
python retrieve_model.py
```
---

## 🛠️ Inicialização

1. **Gere o banco de dados falso (roda uma vez só):**
```bash
python generate_fake_db.py
```

2. **Em um terminal separado, inicie o servidor MCP**
```bash
python content_server_mcp.py
```

3. **Em outro terminal, rode o chat com o assistente**
```bash
python client_chat.py
```

---

## 💬 Exemplos testados

Você pode testar conversas como:

```text
Quero um carro Mitsubishi urbano
Quero um carro Nissan estrada
```

Os modelos de carros disponíveis são:
> ['Fiat', 'Ford', 'Chevrolet', 'Volkswagen', 'Honda', 'Mitsubishi', 'Toyota', 'Nissan', 'Hyundai', 'Kia']

Os tipos de carros disponíveis são:
> ['urbano', 'estrada']

O assistente irá responder com uma tabela formatada (na maioria das vezes) e um comentário comparando os modelos encontrados.(pelo modelo ser pequeno, os comentários não fazem muito sentido, mas o objetivo é demonstrar a funcionalidade)

---

## ❗ Importante

- O projeto roda um **modelo LLM localmente**, o que exige que o **CUDA esteja instalado corretamente** para usar a GPU.
- A execução na CPU é possível, mas **muito mais lenta**.
- O código é uma prova de conceito e pode ser melhorado em robustez, modularização, tratamento de exceções e aplicação real de RAG com vetorização

---

## 🛠 Curiosidade técnica

Este projeto simula o uso de um **protocolo MCP** onde o modelo não responde diretamente às perguntas, mas sim comenta os resultados de uma consulta intermediária.

Isso simula cenários reais de:
- integração com bancos de dados
- separação entre motor de busca (MCP) e camada de linguagem natural (LLM)
- aplicação de RAG (mesmo que conceitual) dentro do servidor MCP
