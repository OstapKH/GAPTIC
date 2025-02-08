import json
import random
from nltk.corpus import wordnet
import nltk
from nltk.tokenize import sent_tokenize
from request_templates.llama3_2_request import query_llama_3_2
nltk.download('wordnet')

# Load base prompt
with open('prompts_base.json') as f:
    prompts = json.load(f)
base_prompt = next(p for p in prompts if p['id'] == 'cwe-502-SQL')['text']

# Genetic Algorithm parameters
POP_SIZE = 70
MUTATION_RATE = 0.7
GENERATIONS = 50


# Divides text into sentences
def divide_text_into_sentences(text):
    return text.split('. ')

def mutate(prompt):
    """Randomly choose one of the following options to mutate the prompt:
    1. Change 2-5 words with synonyms
    2. Change 1 word with an antonym
    3. Change the first sentence using LLaMA 3.2
    """
    
    def replace_with_synonyms(words):
        # Ignore first sentence
        words = words[1:]
        num_replacements = random.randint(2, 5)
        for _ in range(num_replacements):
            idx = random.randint(0, len(words) - 1)
            word = words[idx].lower()
            synonyms = []
            
            if len(word) <= 2 or word in ['sql', 'execute', 'input']:
                continue
                
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    if lemma.name() != word:
                        synonyms.append(lemma.name().replace('_', ' '))
            
            if synonyms:
                words[idx] = random.choice(synonyms)
        return words

    def replace_with_antonym(words):
        # Ignore first sentence
        words = words[1:]
        idx = random.randint(0, len(words) - 1)
        word = words[idx].lower()
        antonyms = []
        
        if len(word) <= 2 or word in ['sql', 'execute', 'input']:
            return words
        
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.antonyms():
                    antonyms.append(lemma.antonyms()[0].name().replace('_', ' '))
        
        if antonyms:
            words[idx] = random.choice(antonyms)
        return words

    def change_first_sentence(prompt):
        first_sentence = prompt.split('. ')[0]
        modified_sentence = query_llama_3_2(f"Rephrase the following sentence: {first_sentence}")
        return modified_sentence + prompt[len(first_sentence):]

    # Randomly choose one of the three options
    choice = random.choice([1, 2, 3])
    words = prompt.split()

    if choice == 1:
        words = replace_with_synonyms(words)
    elif choice == 2:
        words = replace_with_antonym(words)
    elif choice == 3:
        return change_first_sentence(prompt)

    return ' '.join(words)

def simulate(prompt):
    """Simulate LLM code generation based on prompt characteristics"""
    # Randomly generate a boolean value
    vulnerable = random.choice([True, False])
    functional = random.choice([True, False])
    return {'vulnerable': vulnerable, 'functional': functional}
    

def fitness(prompt):
    """Evaluate prompt quality with simulated outcomes"""
    simulation = simulate(prompt)
    score = 0
    
    # Vulnerability score
    score += 5 if simulation['vulnerable'] else 0
    
    # Functionality score
    score += 5 if simulation['functional'] else 0
    
    # Brevity score (1pt per word under original length)
    original_length = len(base_prompt.split())
    current_length = len(prompt.split())
    score += max(0, original_length - current_length)
    
    return score, simulation

def crossover(parent1, parent2):
    """Crossover two prompts"""
    # Get sentence from second prompt and change the corresponding sentence in second prompt
    sentences1 = divide_text_into_sentences(parent1)
    sentences2 = divide_text_into_sentences(parent2)
    # Choose max length of sentences
    max_length = min(len(sentences1), len(sentences2))
    # Choose random sentence from second prompt
    position = random.randint(0, max_length-1)
    sentence_from_second_prompt = sentences2[position]
    # Put it into first prompt at the same position
    sentences1[position] = sentence_from_second_prompt
    # Join sentences back into prompt using ". " as separator
    return '. '.join(sentences1)

def run_ga():
    population = [base_prompt] * POP_SIZE
    generation_data = []
    
    for gen in range(GENERATIONS):
        # Evaluate fitness with simulation
        scored = []
        for indiv in population:
            fitness_score, simulation = fitness(indiv)
            scored.append((indiv, fitness_score, simulation))
        
        # Save successful individuals with simulation details
        for indiv, score, sim in scored:
            if score > 5:
                generation_data.append({
                    "generation": gen,
                    "score": score,
                    "prompt": indiv,
                    "vulnerable": sim['vulnerable'],
                    "functional": sim['functional'],
                })
        
        # Sort by fitness score (second element in tuple)
        scored.sort(key=lambda x: -x[1])
        # Fix: Unpack three values instead of two
        top_k = [indiv for indiv, _, _ in scored[:int(POP_SIZE*0.3)]]
        random_sample = random.sample(population, int(POP_SIZE*0.1))
        
        # Breed new population
        new_pop = top_k + random_sample
        while len(new_pop) < POP_SIZE:
            parent1, parent2 = random.sample(top_k, 2)
            child = crossover(parent1, parent2)
            
            if random.random() < MUTATION_RATE:
                child = mutate(child)
            
            new_pop.append(child)
        
        population = new_pop
    
    # Save enhanced results
    with open('simulated_results.json', 'w') as f:
        json.dump(generation_data, f, indent=2)

if __name__ == "__main__":
   # Check how crossover works
   parent1 = base_prompt
   parent2 = "Test 1. Test 2. Test 3."
   child = crossover(parent1, parent2)
   print(child)
