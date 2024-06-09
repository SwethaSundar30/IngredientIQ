import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from sklearn.model_selection import train_test_split
from tqdm import tqdm
dataset = pd.read_csv("Datasets\FinalDataset.csv")
dataset = dataset.dropna()
def data_summary(input_ingredients):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    
    MAX_LENGTH = 128
    BATCH_SIZE = 16
    LEARNING_RATE = 2e-5
    EPOCHS = 3
    
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(dataset.columns)-1)
    
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)
    
    import random
    def predict_attributes(ingredients):
        predicted_attributes_list = []
        for ingredient in ingredients:
            inputs = tokenizer(ingredient, padding=True, truncation=True, max_length=MAX_LENGTH, return_tensors='pt')
            outputs = model(**inputs)
            predicted_probs = torch.sigmoid(outputs.logits)
            sampled_label_idx = torch.multinomial(predicted_probs, 1).item()
            
            predicted_attributes_list.append({
                'Description': dataset['Description'].iloc[sampled_label_idx],
                'Dietary Needs': dataset['Dietary Needs'].iloc[sampled_label_idx],
                'Allergies': dataset['Allergies'].iloc[sampled_label_idx],
                'Preferences': dataset['Preferences'].iloc[sampled_label_idx],
                'Advantages': dataset['Advantages'].iloc[sampled_label_idx],
                'Disadvantages': dataset['Disadvantages'].iloc[sampled_label_idx],
                'Benefits': dataset['Benefits'].iloc[sampled_label_idx],
                'Impact': dataset['Impact'].iloc[sampled_label_idx],
                'Side Effects': dataset['Side Effects'].iloc[sampled_label_idx]
            })
    
        return predicted_attributes_list
    
    predicted_attributes = predict_attributes(input_ingredients)
    predicted_attributes_list = []

    for i, ingredient in enumerate(input_ingredients):
        predicted_dict = {
            'Ingredient': ingredient,
            'Predicted Description': predicted_attributes[i]['Description'],
            'Predicted Dietary Needs': predicted_attributes[i]['Dietary Needs'],
            'Predicted Allergies': predicted_attributes[i]['Allergies'],
            'Predicted Preferences': predicted_attributes[i]['Preferences'],
            'Predicted Advantages': predicted_attributes[i]['Advantages'],
            'Predicted Disadvantages': predicted_attributes[i]['Disadvantages'],
            'Predicted Benefits': predicted_attributes[i]['Benefits'],
            'Predicted Impact': predicted_attributes[i]['Impact'],
            'Predicted Side Effects': predicted_attributes[i]['Side Effects']
        }
        predicted_attributes_list.append(predicted_dict)
    
    '''# Printing the list of dictionaries
    for predicted_dict in predicted_attributes_list:
        print(predicted_dict)
        print()
    '''
    return predicted_attributes_list
    
