from transformers import AutoModelForCausalLM, AutoTokenizer
import torch



def about_model():
    
    Model_description = \
    """	
    TinyLLaMA-1.1B-Chat is a small instruct-tuned language model:
    - Parameters: ~1.1 billion
    - Designed to follow human instructions
    - Lightweight and works on GPUs with <6GB VRAM
    - Ideal for demos, chat interfaces, and educational tools
    """
    
    Model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    
    return Model_description, Model_name

def get_model(Model_name):
    
    print(f"🔽 Downloading model {Model_name}...")
    
    tokenizer = AutoTokenizer.from_pretrained(Model_name)
    
    model = AutoModelForCausalLM.from_pretrained(Model_name,
                                                torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
                                                            )
    
    tokenizer.save_pretrained("./Models")
    model.save_pretrained("./Models")
    
    print("✅ Model saved in ./Models")



if __name__ == "__main__":
    
    Model_description, Model_name = about_model()
    
    print(Model_description)
    print(f"Nome do modelo: {Model_name}")
    
    get_model(Model_name)
