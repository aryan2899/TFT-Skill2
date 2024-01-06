import numpy as np
from scipy import stats

# Prior function for team abilities
def prior(x, mu, sigma):
    # Assuming a normal distribution as the prior for team abilities
    return stats.norm.pdf(x, loc=mu, scale=sigma)


# Likelihood function based on win/loss records between teams A and B
def likelihood(mu_A, mu_B, n_A_wins, n_B_wins):
    # Calculate the strengths of teams A and B
    strength_A = np.exp(mu_A)
    strength_B = np.exp(mu_B)

    # Calculate the probability of team A winning based on Bradley-Terry model
    prob_A_wins = strength_A / (strength_A + strength_B)
    print(prob_A_wins)

    # Likelihood contribution from observed win/loss records using a binomial distribution
    return prob_A_wins ** n_A_wins * (1 - prob_A_wins) ** n_B_wins


def acceptance_ratio(mu_current, mu_proposed, sigma, n_A_wins, n_B_wins):
    # Calculate the prior probabilities for the current and proposed means
    prior_current = prior(mu_current, sigma)
    prior_proposed = prior(mu_proposed, sigma)
    
    # Calculate the likelihood for the current and proposed means
    likelihood_current = likelihood(mu_current, mu_proposed, n_A_wins, n_B_wins)
    likelihood_proposed = likelihood(mu_proposed, mu_current, n_B_wins, n_A_wins)
    
    # Calculate the acceptance ratio based on the prior and likelihood
    acceptance = (likelihood_proposed * prior_proposed) / (likelihood_current * prior_current)
    
    return min(1, acceptance)  # Cap acceptance at 1 for Metropolis-Hastings

from scipy.stats import norm

def true_skill_likelihood(mu_A, sigma_A, mu_B, sigma_B):
    # Calculate the variance of the sum of skills
    sigma_squared_sum = sigma_A**2 + sigma_B**2
    
    # Calculate the difference in skills
    skill_diff = mu_A - mu_B
    
    # Calculate the probability of A winning against B using Gaussian CDF
    return norm.cdf(skill_diff / (sigma_squared_sum ))

from scipy.stats import norm

def aggregated_true_skill_likelihood(mu_A, sigma_A, mu_B, sigma_B, total_matches, team_A_wins, team_B_wins):
    # Calculate the variance of the sum of skills
    sigma_squared_sum = sigma_A**2 + sigma_B**2 + 2  # Adjusted sum of variances
    
    # Calculate the difference in skills
    skill_diff = mu_A - mu_B
    
    # Calculate the probability of A winning against B using Gaussian CDF
    prob_A_wins = norm.cdf(skill_diff / (sigma_squared_sum))
    
    # Likelihood based on aggregated win/loss records
    likelihood = (prob_A_wins ** team_A_wins) * ((1 - prob_A_wins) ** team_B_wins)
    
    # Adjust likelihood based on total matches
    adjusted_likelihood = likelihood ** total_matches
    
    return stats.binom.pmf(team_A_wins, total_matches, prob_A_wins)


# Example usage:
mu_1 = 90
sigma_1 = 8.3
mu_2 = 30
sigma_2 = 8.3
probability_A_wins = aggregated_true_skill_likelihood(mu_1,sigma_1, mu_2, sigma_2, 10, 7, 3)
print(probability_A_wins)
