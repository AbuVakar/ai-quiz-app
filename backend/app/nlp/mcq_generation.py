# # MCQ generation (migrated from old mcq_env)
# import random
# import spacy
# from .question_generation import generate_question
# from .distractor_generation import generate_distractors

# # Load spaCy English model
# nlp = spacy.load("en_core_web_sm")

# def generate_mcqs(text, num_questions=20):
#     """
#     Generate a list of MCQs from the input text.
#     Each MCQ is a dictionary with keys: question, options, answer.
#     """
#     mcqs = []
#     doc = nlp(text)
#     # Extract candidate answers from named entities and noun chunks
#     candidates = [ent.text for ent in doc.ents if len(ent.text.split()) <= 4]
#     if len(candidates) < num_questions:
#         candidates += [chunk.text for chunk in doc.noun_chunks]
#     # Remove duplicates and trim list to the required number
#     candidates = list(dict.fromkeys(candidates))[:num_questions]

#     for candidate in candidates:
#         context = ""
#         entity_label = None
#         # Use the sentence that contains the candidate as context
#         for ent in doc.ents:
#             if ent.text == candidate:
#                 entity_label = ent.label_
#                 break
#         for sent in doc.sents:
#             if candidate in sent.text:
#                 context = sent.text
#                 break
#         if not context:
#             context = text  # fallback

#         # Generate question using the candidate as answer
#         question = generate_question(context, candidate)
#         distractors = generate_distractors(candidate, doc=doc, entity_label=entity_label)
#         # Ensure the correct answer is included and shuffle options
#         options = distractors + [candidate]
#         random.shuffle(options)
#         mcqs.append({
#             "question": question,
#             "options": options,
#             "answer": candidate
#         })

#     # Deduplicate and validate questions
#     unique_mcqs = []
#     seen_questions = []
#     for mcq in mcqs:
#         q = mcq["question"].strip()
#         # Basic validation: skip too short or awkward questions
#         if len(q) < 8 or not any(w in q.lower() for w in ["what", "where", "when", "who", "how", "which", "why"]):
#             continue
#         # Answer-in-context validation
#         answer = mcq["answer"].strip()
#         context = ""
#         for sent in doc.sents:
#             if answer in sent.text:
#                 context = sent.text
#                 break
#         if answer not in context:
#             continue
#         # Deduplication: skip if similar to any already kept question
#         is_duplicate = False
#         q_doc = nlp(q)
#         for seen_q in seen_questions:
#             if q_doc.similarity(nlp(seen_q)) > 0.85:
#                 is_duplicate = True
#                 break
#         if not is_duplicate:
#             unique_mcqs.append(mcq)
#             seen_questions.append(q)
#     return unique_mcqs
import random
import spacy
from .question_generation import generate_question
from .distractor_generation import generate_distractors

nlp = spacy.load("en_core_web_sm")

def generate_mcqs(text, num_questions=10):
    mcqs = []
    doc = nlp(text)

    # Step 1: Extract candidate answers
    candidates = [ent.text for ent in doc.ents if len(ent.text.split()) <= 4]
    if len(candidates) < num_questions:
        candidates += [chunk.text for chunk in doc.noun_chunks]
    candidates = list(dict.fromkeys(candidates))[:num_questions]

    for candidate in candidates:
        context = ""
        entity_label = None

        for ent in doc.ents:
            if ent.text == candidate:
                entity_label = ent.label_
                break
        for sent in doc.sents:
            if candidate in sent.text:
                context = sent.text
                break
        if not context:
            context = text

        # Generate question
        question = generate_question(context, candidate)
        if not question or len(question) < 8 or not any(q_word in question.lower() for q_word in ["what", "who", "when", "where", "which", "why", "how"]):
            continue

        # Generate distractors
        distractors = generate_distractors(candidate, doc=doc, entity_label=entity_label)
        options = distractors + [candidate]
        # options = list(set(options))  # Remove duplicates
        options = list(set([opt.strip().lower().capitalize() for opt in options if len(opt.strip()) > 2]))

        if len(options) < 4:
            # Add dummy options if fewer than 4
            while len(options) < 4:
                options.append(candidate + "_" + str(random.randint(10, 99)))

        random.shuffle(options)

        mcqs.append({
            "question": question,
            "options": options[:4],
            "answer": candidate
        })

    # Deduplicate questions
    unique_mcqs = []
    seen_questions = []
    for mcq in mcqs:
        if mcq["question"] not in seen_questions:
            seen_questions.append(mcq["question"])
            unique_mcqs.append(mcq)

    return unique_mcqs
