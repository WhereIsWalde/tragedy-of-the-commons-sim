import statistics

class Game:
    def __init__(self):
        self.N: int = 0
        self.player_choices: dict[str, int] = {}

        self.player_utilities: dict[str, float] = {}
        self.player_emissions: dict[str, int] = {}

        self.is_finished: bool = False
        self.emission_multiplier: float = 1.0
        self.total_base_utility: float = 0.0

    def add_player(self, factory_name: str, amount_produced: int):
        self.player_choices[factory_name] = amount_produced
        self.N += 1

    def play(self):
        """Given initiated player_choices dict and number of players N, computes player_utilities and player emissions.
            Stores them inside the class"""
        if self.N == 0:
            print("There are zero players, game can not be played!")
            return
        if len(self.player_choices) == 0:
            print("The player choices are not initialized, the game can not be played!")
            return
        self.player_emissions = self.__compute_base_emissions(choices=self.player_choices)
        base_utilities: dict[str: float] = self.__compute_base_utilities(self.player_choices)
        self.total_base_utility = sum(v for v in base_utilities.values())
        self.player_utilities = self.__compute_final_utilities(base_utilities = base_utilities, emissions=self.player_emissions)
        self.is_finished = True

    def get_mean_utility(self) -> float:
        return statistics.mean(self.player_utilities.values())
    
    def get_median_utility(self) -> float:
        return statistics.median(self.player_utilities.values())
    
    def get_total_utility(self) -> float:
        return sum(v for v in self.player_utilities.values())
    
    def get_total_emissions(self) -> int:
        return sum(v for v in self.player_emissions.values())
    
    def get_theoretic_maximum_utility(self) -> float:
        return self.N * 1.25

    def __compute_base_utilities(self, choices: dict[str, int]) -> dict[str, float]:
        # This is currently very simple but exists in case more complicated interraction is wanted
        return {k: v for k,v in choices.items()}

    def __compute_base_emissions(self, choices: dict[str, int]) -> dict[str, float]:
        # This is currently very simple but exists in case more complicated interraction is wanted
        return {k: v for k,v in choices.items()}
    
    def __compute_emission_multiplier(self, emissions: dict[str, int]) -> float:
        self.emission_multiplier = (1-sum(e for e in emissions.values()) / (5 * self.N))
        return self.emission_multiplier
    
    def __compute_final_utilities(self, base_utilities: dict[str, int], emissions: dict[str, int]):
        C = self.__compute_emission_multiplier(emissions)
        return {k: C*v for k,v in base_utilities.items()}
    

    
