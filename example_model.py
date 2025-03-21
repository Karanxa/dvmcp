import numpy as np
import pickle

class VulnerableModel:
    def __init__(self):
        self.weights = np.random.randn(10)
        self.bias = np.random.randn()
        
    def predict(self, X):
        # VULNERABLE: No input validation
        return np.dot(X, self.weights) + self.bias

# Create and save a sample model
if __name__ == '__main__':
    model = VulnerableModel()
    
    # Save the model (vulnerable serialization)
    with open('sample_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Example prediction
    X = np.random.randn(10)
    print(f"Example prediction: {model.predict(X)}") 