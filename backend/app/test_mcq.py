from app.nlp.mcq_generation import generate_mcqs
from app.nlp.question_generation import generate_question
from app.nlp.distractor_generation import generate_distractors
import spacy
import random

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def test_generate_mcqs():
    # More detailed test content
    text = """
    The Industrial Revolution, which began in the late 18th century, marked the beginning of significant environmental changes. 
    In 1952, London experienced the Great Smog, a severe air pollution event that lasted for five days. 
    This event led to the Clean Air Act of 1956, which aimed to reduce air pollution in the UK. 
    Modern cities like Delhi and Beijing have been facing severe air quality issues due to rapid industrialization and urbanization. 
    The World Health Organization (WHO) estimates that around 7 million people die annually due to exposure to polluted air. 
    Persistent organic pollutants (POPs) like DDT can remain in the environment for decades, affecting wildlife and human health. 
    The Chernobyl disaster in 1986 and Fukushima disaster in 2011 released radioactive materials that will remain hazardous for thousands of years. 
    The Paris Agreement, adopted in 2015, aims to limit global warming to well below 2 degrees Celsius. 
    The Kyoto Protocol, signed in 1997, was the first international agreement to set binding targets for reducing greenhouse gas emissions. 
    The Stockholm Convention, signed in 2001, focuses on eliminating persistent organic pollutants (POPs) globally.
    """
    
    # Generate MCQs
    mcqs = generate_mcqs(text, num_questions=20)
    
    # Print results
    print("\nGenerated MCQs:")
    for i, mcq in enumerate(mcqs, 1):
        print(f"\nQ{i}: {mcq['question']}")
        options = mcq['options']
        random.shuffle(options)  # Shuffle options again for variety
        for j, option in enumerate(options, 1):
            print(f"  {chr(65+j-1)}. {option}")
        print(f"Answer: {mcq['answer']}")
        print(f"Quality Score: {mcq.get('quality_score', 'N/A')}")

if __name__ == "__main__":
    test_generate_mcqs()
