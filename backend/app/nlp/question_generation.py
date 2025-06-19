# Question generation (migrated from old mcq_env)
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load the pre-trained model (this may take a moment on first run)
MODEL_NAME = "valhalla/t5-small-qg-hl"
_tokenizer = None
_model = None

def get_model_and_tokenizer():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        _tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
        _model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
    return _tokenizer, _model

def generate_question(context, answer):
    """
    Generate a question based on the context and highlighted answer.
    """
    tokenizer, model = get_model_and_tokenizer()
    # Create a prompt with <hl> markers around the answer
    prompt = f"generate question: {context.replace(answer, f'<hl> {answer} <hl>')}"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(input_ids)
    question = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return question