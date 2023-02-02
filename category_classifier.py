from transformers import pipeline

# https://huggingface.co/spaces/joeddav/zero-shot-demo
classifier = pipeline("zero-shot-classification")

# Need a known dictionary to add predictions too if they don't already exist

sequence = "TESCO STORES-2813 LEAMINGTON SP GBR"
candidate_labels = ['INCOME', 'GROCERIES', 'SHOPPING', 'EATING_OUT']

classifier(sequence, candidate_labels)