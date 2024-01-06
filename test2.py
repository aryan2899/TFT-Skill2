from multiprocessing import Process

class Team:
    def __init__(self, mu, std):
        self.mu = mu
        self.std = std
    
    def get_mean(self):
        return self.mu
    
    def get_std(self):
        return self.std
    
    def update_skills(self, delta_mu, delta_std):
        self.mu += delta_mu
        self.std += delta_std


class Match:
    def __init__(self, team1, team2, results):
        self.team1 = team1
        self.team2 = team2
        self.results = results  # Placeholder for match results
    
    def play_match(self):
        # Placeholder deterministic update for simulation
        self.team1.update_skills(1, 1)
        self.team2.update_skills(-1, -1)

def play_parallel_matches(team1, team2, team3, team4):
    # Parallel Process 1: Team1 vs Team2 & Team3 vs Team4
    match1 = Match(team1, team2, (1, 2))  # Results placeholder (for example)
    match2 = Match(team3, team4, (3, 0))  # Results placeholder (for example)
    
    match1.play_match()  # Simulate match 1
    match2.play_match()  # Simulate match 2

    # Update skills for match 1 teams
    team1.update_skills(1, 1)
    team2.update_skills(-1, -1)
    # Update skills for match 2 teams
    team3.update_skills(3, 3)
    team4.update_skills(0, 0)

def play_parallel_matches_reversed(team1, team2, team3, team4):
    # Parallel Process 2: Team2 vs Team4 & Team1 vs Team3
    match1 = Match(team2, team4, (2, 1))  # Results placeholder (for example)
    match2 = Match(team1, team3, (0, 3))  # Results placeholder (for example)
    
    match1.play_match()  # Simulate match 1
    match2.play_match()  # Simulate match 2

    # Update skills for match 1 teams
    team2.update_skills(2, 2)
    team4.update_skills(-1, -1)
    # Update skills for match 2 teams
    team1.update_skills(0, 0)
    team3.update_skills(3, 3)

if __name__ == "__main__":
    team1 = Team(25, 4)
    team2 = Team(25, 4)
    team3 = Team(25, 4)
    team4 = Team(25, 4)

    # Create processes for parallel execution
    process1 = Process(target=play_parallel_matches, args=(team1, team2, team3, team4))
    process2 = Process(target=play_parallel_matches_reversed, args=(team1, team2, team3, team4))

    # Start the processes
    process1.start()
    process2.start()

    # Wait for the processes to complete
    process1.join()
    process2.join()

    # Share the updated skills across parallel processes
    team1.update_skills(0, 0)
    team2.update_skills(0, 0)
    team3.update_skills(0, 0)
    team4.update_skills(0, 0)

    # Check the updated skills after both sets of parallel matches
    print("Team 1 updated skills:", team1.get_mean(), team1.get_std())
    print("Team 2 updated skills:", team2.get_mean(), team2.get_std())
    print("Team 3 updated skills:", team3.get_mean(), team3.get_std())
    print("Team 4 updated skills:", team4.get_mean(), team4.get_std())
