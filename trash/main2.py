import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Prior function for team abilities
def prior(x, mu, sigma):
    # Assuming a normal distribution as the prior for team abilities
    return stats.norm.pdf(x, loc=mu, scale=sigma)

def likelihood(mu_A, sigma_A, mu_B, sigma_B, total_matches, team_A_wins, team_B_wins):
    # Calculate the variance of the sum of skills
    sigma_squared_sum = sigma_A**2 + sigma_B**2 + 2  # Adjusted sum of variances
    
    # Calculate the difference in skills
    skill_diff = mu_A - mu_B
    
    # Calculate the probability of A winning against B using Gaussian CDF
    prob_A_wins = stats.norm.cdf(skill_diff / (sigma_squared_sum))
    
    # Likelihood based on aggregated win/loss records
    likelihood = (prob_A_wins ** team_A_wins) * ((1 - prob_A_wins) ** team_B_wins)
    
    # Adjust likelihood based on total matches
    adjusted_likelihood = likelihood ** total_matches
    
    return adjusted_likelihood

def acceptance_ratio(mu_proposed, mu_current, mu_1, mu_2, sigma, n_A_wins, n_B_wins):
    # Calculate the prior probabilities for the current and proposed means
    total_matches = n_A_wins + n_B_wins
    prior_current = prior(mu_current, mu_1, sigma)
    prior_proposed = prior(mu_proposed,mu_1, sigma)
    
    # Calculate the likelihood for the current and proposed means
    likelihood_current = likelihood(mu_current, mu_proposed, n_A_wins, n_B_wins)
    likelihood_proposed = likelihood(mu_proposed, mu_current, n_B_wins, n_A_wins)
    
    # Calculate the acceptance ratio based on the prior and likelihood
    acceptance = (likelihood_proposed * prior_proposed) / (likelihood_current * prior_current)
    
    return min(1, acceptance)  # Cap acceptance at 1 for Metropolis-Hastings


results = []

mu_1 = 35
mu_2 = 30
sigma = 8.33
n_1 = 30
n_2 = 15

# Initialzie a value of p
x = np.random.uniform(0, 50)

# Define model parameters
n_samples = 25000
burn_in = 5000
lag = 5

# Create the MCMC loop
for i in range(n_samples):
    # Propose a new value of p randomly from a uniform distribution between 0 and 1
    x_new = np.random.random_sample()
    # Compute acceptance probability
    R = acceptance_ratio(x, x_new)
    # Draw random sample to compare R to
    u = np.random.random_sample()
    # If R is greater than u, accept the new value of p (set p = p_new)
    if u < R:
        x = x_new
    # Record values after burn in - how often determined by lag
    if i > burn_in and i%lag == 0:
        results.append(x)
        
    
        

