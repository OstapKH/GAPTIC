import json
import random
from nltk.corpus import wordnet
import nltk
nltk.download('wordnet')

# Load base prompt
with open('prompts_base.json') as f:
    prompts = json.load(f)
base_prompt = next(p for p in prompts if p['id'] == 'cwe-502-SQL')['text']

# Genetic Algorithm parameters
POP_SIZE = 70
MUTATION_RATE = 0.7
GENERATIONS = 50

def mutate(prompt):
    """Replace 2-5 words with synonyms"""
    words = prompt.split()
    num_replacements = random.randint(2, 5)
    
    for _ in range(num_replacements):
        idx = random.randint(0, len(words)-1)
        word = words[idx].lower()  # Convert to lowercase for better matching
        synonyms = []
        
        # Skip if word is too short or a common SQL keyword
        if len(word) <= 2 or word in ['sql', 'execute', 'input']:
            continue
            
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.name() != word:
                    synonyms.append(lemma.name().replace('_', ' '))
        
        if synonyms:
            words[idx] = random.choice(synonyms)
    
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
    """Single-point crossover"""
    p1_words = parent1.split()
    p2_words = parent2.split()
    pt = random.randint(1, min(len(p1_words), len(p2_words))-1)
    return ' '.join(p1_words[:pt] + p2_words[pt:])

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
    run_ga()
