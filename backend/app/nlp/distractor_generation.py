# # Distractor generation (migrated from old mcq_env)
# from nltk.corpus import wordnet as wn
# import random

# def generate_distractors(correct_answer, doc=None, entity_label=None, num_distractors=3):
#     distractors = set()
#     # Handle numbers
#     if correct_answer.replace(",", "").replace(".", "").isdigit():
#         try:
#             num = float(correct_answer.replace(",", ""))
#             for diff in [-10, -5, 5, 10, -1, 1]:
#                 val = str(int(num + diff)) if num.is_integer() else str(num + diff)
#                 if val != correct_answer:
#                     distractors.add(val)
#                 if len(distractors) >= num_distractors:
#                     break
#         except Exception:
#             pass
#     # Handle named entities
#     elif entity_label and doc is not None:
#         entities = [ent.text for ent in doc.ents if ent.label_ == entity_label and ent.text != correct_answer]
#         random.shuffle(entities)
#         for ent in entities:
#             distractors.add(ent)
#             if len(distractors) >= num_distractors:
#                 break
#     # Fallback to WordNet
#     if len(distractors) < num_distractors:
#         for syn in wn.synsets(correct_answer):
#             for lemma in syn.lemmas():
#                 word = lemma.name().replace("_", " ")
#                 if word.lower() != correct_answer.lower():
#                     distractors.add(word)
#                 if len(distractors) >= num_distractors:
#                     break
#             if len(distractors) >= num_distractors:
#                 break
#     return list(distractors)[:num_distractors]


from nltk.corpus import wordnet as wn
import random

# def generate_distractors(correct_answer, doc=None, entity_label=None, num_distractors=3):
#     distractors = set()

#     # If the correct answer is a number
#     if correct_answer.replace(",", "").replace(".", "").isdigit():
#         try:
#             num = float(correct_answer.replace(",", ""))
#             for diff in [-10, -5, 5, 10, -1, 1]:
#                 val = str(int(num + diff)) if num.is_integer() else str(num + diff)
#                 if val != correct_answer:
#                     distractors.add(val)
#         except Exception:
#             pass

#     # Named entity-based distractors
#     elif entity_label and doc is not None:
#         entities = [ent.text for ent in doc.ents if ent.label_ == entity_label and ent.text != correct_answer]
#         random.shuffle(entities)
#         distractors.update(entities[:num_distractors])

#     # Fallback to WordNet synonyms
#     if len(distractors) < num_distractors:
#         for syn in wn.synsets(correct_answer):
#             for lemma in syn.lemmas():
#                 word = lemma.name().replace("_", " ")
#                 if word.lower() != correct_answer.lower() and word.lower() != correct_answer.strip().lower():
#                     distractors.add(word)
#                 if len(distractors) >= num_distractors:
#                     break
#             if len(distractors) >= num_distractors:
#                 break

#     # Final fallback: dummy distractors if not enough
#     while len(distractors) < num_distractors:
#         dummy = correct_answer + "_" + str(random.randint(1, 100))
#         distractors.add(dummy)

#     return list(distractors)[:num_distractors]

def generate_distractors(correct_answer, doc=None, entity_label=None, num_distractors=3):
    distractors = set()

    # Handle numbers separately
    if correct_answer.replace(",", "").replace(".", "").isdigit():
        try:
            num = float(correct_answer.replace(",", ""))
            for diff in [-10, -5, 5, 10]:
                val = str(int(num + diff)) if num.is_integer() else str(round(num + diff, 2))
                if val != correct_answer:
                    distractors.add(val)
        except Exception:
            pass

    # Use named entities from same label
    if entity_label and doc:
        ents = [ent.text for ent in doc.ents if ent.label_ == entity_label and ent.text != correct_answer]
        distractors.update(ents[:num_distractors])

    # WordNet backup
    if len(distractors) < num_distractors:
        from nltk.corpus import wordnet as wn
        for syn in wn.synsets(correct_answer):
            for lemma in syn.lemmas():
                word = lemma.name().replace("_", " ").title()
                if word.lower() != correct_answer.lower():
                    distractors.add(word)
                if len(distractors) >= num_distractors:
                    break
            if len(distractors) >= num_distractors:
                break

    # Remove similar words
    distractors = [d for d in distractors if d.lower() != correct_answer.lower()]
    distractors = list(set(distractors))[:num_distractors]

    # Add common dummy distractors if still insufficient
    common = ["climate change", "pollution", "waste", "carbon", "greenhouse"]
    while len(distractors) < num_distractors:
        option = random.choice(common)
        if option.lower() != correct_answer.lower() and option not in distractors:
            distractors.append(option)

    return distractors
