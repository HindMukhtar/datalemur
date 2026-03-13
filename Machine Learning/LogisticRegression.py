import numpy as np 

class LogisticRegression: 
    def __init__(self, learning_rate = 0.01, num_iterations = 1000): 
        self.lr = learning_rate 
        self.epochs = num_iterations 
        self.w = None 
        self.b = None

    def sigmoid(self, z:np.array): 
        return  1/(1 + np.exp(-z))

    def fit(self, X:np.array, y: np.Array) -> None: 
        # Initialize weights 
        n_samples, n_features = X.shape
        self.X = X 
        self.y = y 
        w = np.zeros(n_features)
        b = 0

        for i in range(self.epochs): 

            # calculate the weights gradient 
            z = np.dot(X, w) + b
            dW = (1/n_samples)*X.T*(self.sigmoid(z) - y)
            db = (1/n_samples)*sum(self.sigmoid(z) - y)

            # update new weights 
            w = w + self.lr*dW 
            b = b + self.lr*db 

        self.w = w 
        self.b = b 

        return 
    
    def predictprob(self, x: int) -> int:
        z = self.w.T*x + self.b
        return self.sigmoid(z)
    
    def predict(self, x: int) -> int: 
        prob = self.predictprob(x)

        return (prob >= 0.5).astype(int)
    


