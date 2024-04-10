import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
# from hmmlearn import hmm
from hmmlearn import hmm

class Random_Variable: 
    
    def __init__(self, name, values, probability_distribution): 
        self.name = name 
        self.values = values 
        self.probability_distribution = probability_distribution
        if all(type(item) is np.int64 for item in values):
#         if all(type(item) is numpy.int64 for item in values):
            self.type = 'numeric'
            self.rv = stats.rv_discrete(name = name, values = (values, probability_distribution))
        elif all(type(item) is str for item in values): 
            self.type = 'symbolic'
            self.rv = stats.rv_discrete(name = name, values = (np.arange(len(values)), probability_distribution))
            self.symbolic_values = values 
        else: 
            self.type = 'numeric'
            self.rv = stats.rv_discrete(name = name, values = (values, probability_distribution))
#             self.type = 'undefined'
            
    def sample(self,size): 
#         print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
#         print(self.type)
        if (self.type =='numeric'):
            return self.rv.rvs(size=size)
        elif (self.type == 'symbolic'): 
            numeric_samples = self.rv.rvs(size=size)
            mapped_samples = [self.values[x] for x in numeric_samples]
            return mapped_samples

    def get_name(self):
        return self.name
# values = ['S', 'C']
# probabilities = [0.9, 0.1]
# weather = Random_Variable('weather', values, probabilities)
# samples = weather.sample(365)
# print(",".join(samples))

# state2color = {} 
# state2color['S'] = 'yellow'
# state2color['C'] = 'grey'

def plot_weather_samples(samples, state2color, title): 
    colors = [state2color[x] for x in samples]
    x = np.arange(0, len(colors))
    y = np.ones(len(colors))
    plt.figure(figsize=(10,1))
    plt.bar(x, y, color=colors, width=1)
    plt.title(title)
    
# plot_weather_samples(samples, state2color, 'iid')

def markov_chain(transmat, state, state_names, samples): 
    (rows, cols) = transmat.shape 
    rvs = [] 
    values = list(np.arange(0,rows))
    
    # create random variables for each row of transition matrix 
    for r in range(rows): 
        rv = Random_Variable("row" + str(r), values, transmat[r])
        rvs.append(rv)
    
    # start from initial state and then sample the appropriate 
    # random variable based on the state following the transitions 
    states = [] 
    for n in range(samples): 
        state = rvs[state].sample(1)[0]    
        states.append(state_names[state])
    return states

transMat = np.array([[0.63, 0.37], [0.37, 0.63]])

CGD = Random_Variable('CGD', ['A', 'C', 'G', 'T'], 
                              [0.15, 0.35, 0.35, 0.15])
CGS = Random_Variable('CGS', ['A', 'C', 'G', 'T'], 
                               [0.40, 0.10, 0.10, 0.40])

def emit_obs(state, CGD, CGS): 
    if (state == 'CGD'): 
        obs = CGD.sample(1)[0]
    else: 
        obs = CGS.sample(1)[0]
    return obs 

state2color = {} 
state2color['CGD'] = 'black'
state2color['CGS'] = 'white'

samples1 = markov_chain(transMat,0,['CGD','CGS'], 1000)
plot_weather_samples(samples1, state2color, 'DNA seq')

obs = [emit_obs(s, CGD, CGS) for s in samples1]

obs2color = {} 
obs2color['A'] = 'red'
obs2color['C'] = 'green'
obs2color['T'] = 'blue'
obs2color['G'] = 'yellow'

plot_weather_samples(obs, obs2color, "DNA color")


transmat =  np.array([[0.63, 0.37], [0.37, 0.63]])

start_prob = np.array([0.5, 0.5])

# yellow and red have high probs for sunny 
# blue and grey have high probs for cloudy 
emission_probs = np.array([[0.15, 0.35, 0.35, 0.15], [0.40, 0.10, 0.10, 0.40]])

model = hmm.MultinomialHMM(n_components=2)
model.startprob_ = start_prob 
model.transmat_ = transmat 
model.emissionprob_ = emission_probs
model.n_trials = 3

# sample the model - X is the observed values 
# and Z is the "hidden" states 
X, Z = model.sample(10000)
# learn a new model 
estModel = hmm.MultinomialHMM(n_components=2, n_iter=10000).fit(X)

print("Estimated model:")
print(estModel.transmat_)
print("Original model:")
print(model.transmat_)

X, Z = estModel.sample(10000)
# print(X)
# print(Z)
state2color = {} 
state2color[0] = 'black'
state2color[1] = 'white'
plot_weather_samples(Z, state2color, 'states')

samples = [item for sublist in X for item in sublist]
obj2color = {} 
obj2color[0] = 'red'
obj2color[1] = 'green'
obj2color[2] = 'blue'
obj2color[3] = 'yellow'
# print(samples)
plot_weather_samples(samples[:10000], obj2color, 'observations')
