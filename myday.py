"""
Simulation of my (not really) day
Uses finite state machine implementation
"""
import random
import time
from dataclasses import dataclass, field


@dataclass(frozen=True)
class State:
    name: str = "starting state"
    takes_time: int = 0
    conditions_to_start: list = field(default_factory=list)

    def check_conditions(self, characteristics: list) -> bool:
        """
        Checks if a State can be processed
        :return: bool
        """
        for item in self.conditions_to_start:
            if item not in characteristics:
                return False
        return True


def info(func):
    """
    Takes a function, prints the states of completion
    """

    def wrapper(*args, **kwargs):
        print(f"My characteristics: {', '.join(args[0].characteristics)}")
        print(f"I have decided to {args[1][3:]}")
        func(*args, **kwargs)
        print()

    return wrapper


class Simulation:
    """
    Creating a simulation
    """

    def __init__(self):
        self._curr_state = None
        self._hour = 0
        self.to_sleep = self.sleep_state()
        self.to_eat = self.eat_state()
        self.to_workout = self.workout_state()
        self.to_study = self.study_state()
        self.to_walk = self.walk_state()
        self.to_watch_youtube = self.watch_state()
        self.to_shower = self.shower_state()
        self.characteristics = list()
        self.slept = False

    def get_current_state(self):
        return self._curr_state

    @info
    def send_to_state(self, value):
        """
        Sends a current state message about activity
        """
        next(self._curr_state)
        self._curr_state.send(value)

    def add_chars(self, values: list) -> None:
        """
        Adds items in characteristics from values if necessary
        :param values: strings
        :return: None
        """
        for item in values:
            if item not in self.characteristics:
                self.characteristics.append(item)

    def del_chars(self, values: list) -> None:
        """
        Deletes items in characteristics if they exist
        """
        for item in values:
            if item in self.characteristics:
                self.characteristics.remove(item)

    def sleep_state(self):
        """
        A state for sleeping
        """
        state = State("sleep", 7, ["tired"])
        while True:
            received = yield
            if received == "to_sleep":
                if state.check_conditions(self.characteristics):
                    self.slept = True
                    self._hour += state.takes_time
                    self.del_chars(["tired"])
                    self.add_chars(["relaxed", "hungry"])
                    self._curr_state = self.to_eat
                else:
                    self._hour += 1
                    self.do_random_action()

            elif received == "to_skip":
                self._hour += 2

    def eat_state(self):
        """
        A state for eating.
        """
        state = State("eat", 1, ["hungry"])
        while True:
            received = yield
            if received == "to_eat":
                if state.check_conditions(self.characteristics):
                    self._hour += state.takes_time
                    self.del_chars(["hungry"])
                    self.add_chars(["relaxed"])
                    self._curr_state = random.choice([self.to_study, self.to_walk, self.to_watch_youtube])
                else:
                    self._hour += 1
                    self.do_random_action()

            elif received == "to_skip":
                self.add_chars(["angry"])
                self._hour += 1
                self.do_random_action()

    def study_state(self) -> None:
        """
        Studying state
        """
        state = State("study", random.randint(1, 4), ["relaxed"])
        while True:
            received = yield
            if received == "to_study":
                if state.check_conditions(self.characteristics):
                    self._hour += state.takes_time
                    self.del_chars(["relaxed"])
                    self.add_chars(["tired"])
                    self._curr_state = random.choice(
                        [self.to_walk, self.to_watch_youtube, self.to_eat, self.to_workout])
                else:
                    self._hour += 1
                    self.do_random_action()

            elif received == "to_skip":
                self.add_chars(["angry", "hungry"])
                self.del_chars(["happy"])
                self._hour += 1
                self.do_random_action()

    def shower_state(self) -> None:
        """
        A shower state
        """
        state = State("shower", 1, [])
        while True:
            received = yield
            if received == "to_shower":
                self._hour += state.takes_time
                self.del_chars(["angry", "dirty", "tired"] if self.slept else ["angry", "dirty"])
                self.add_chars(["relaxed"])
                self.do_random_action()
            elif received == "to_skip":
                self.do_random_action()

    def walk_state(self) -> None:
        """
        Being on a walk state
        """
        state = State("walk", random.randint(1, 2), ["relaxed"])
        while True:
            received = yield
            if received == "to_walk":
                self._hour += state.takes_time
                self.del_chars(["tired", "angry"] if self.slept else ["angry"])
                self.add_chars(["hungry"])
                self._curr_state = random.choice([self.to_sleep, self.to_study, self.to_eat, self.to_shower])
            elif received == "to_skip":
                self.do_random_action()

    def workout_state(self):
        state = State("workout", random.randint(1, 2), ["relaxed", "angry"])
        while True:
            received = yield
            if received == "to_workout":
                self._hour += state.takes_time
                self.del_chars(["angry", "relaxed"] if self.slept else ["relaxed"])
                self.add_chars(["tired", "dirty", "hungry"])
                self._curr_state = random.choice([self.to_eat, self.to_shower])
            elif received == "to_skip":
                self.add_chars(["happy", "relaxed"])
                self.do_random_action()

    def watch_state(self):
        state = State("watch", 1, ["tired"])
        while True:
            received = yield
            if received == "to_watch":
                self._hour += state.takes_time
                self.del_chars(["tired", "angry"] if self.slept else ["angry"])
                self.add_chars(["happy"])
                self.do_random_action()
            elif received == "to_skip":
                self.add_chars(["angry"])
                self.do_random_action()

    def cycle(self):
        self.add_chars(["tired", "hungry", "dirty"])
        self.do_random_action()
        while self._hour < 24:
            print(f"{self._hour} hour(s) passed")
            if self._curr_state == self.to_eat:
                if self.happen_prob(5) is False:
                    self.send_to_state("to_eat")
                else:
                    self.send_to_state("to_skip")
            elif self._curr_state == self.to_sleep:
                if self.happen_prob(4) is False:
                    self.send_to_state("to_sleep")
                else:
                    self.send_to_state("to_skip")
            elif self._curr_state == self.to_walk:
                if self.happen_prob(3) is False:
                    self.send_to_state("to_walk")
                else:
                    self.send_to_state("to_skip")
            elif self._curr_state == self.to_study:
                if self.happen_prob(5) is False:
                    self.send_to_state("to_study")
                else:
                    self.send_to_state("to_skip")
            elif self._curr_state == self.to_shower:
                if self.happen_prob(8) is False:
                    self.send_to_state("to_shower")
                else:
                    self.send_to_state("to_skip")
            elif self._curr_state == self.to_workout:
                if self.happen_prob(2):
                    self.send_to_state("to_workout")
                else:
                    self.send_to_state("to_skip")
            elif self._curr_state == self.to_watch_youtube:
                if self.happen_prob(2) is True:
                    self.send_to_state("to_watch")
                else:
                    self.send_to_state("to_skip")
        print(f"Me at the end of a day: {', '.join(self.characteristics)}")

    @staticmethod
    def happen_prob(prob: int):
        """
        20 percent chance <-> happen_prob(5)
        """
        return random.randint(1, prob) == 1

    def do_random_action(self):
        """
        Performs a random action. Changes current state to a random one.
        """
        self._curr_state = random.choice([
            self.to_eat, self.to_walk, self.to_study,
            self.to_sleep, self.to_shower, self.to_workout, self.to_watch_youtube
        ])
        print(f"Random event: {self._curr_state.__name__}")


if __name__ == "__main__":
    simulation = Simulation()
    simulation.cycle()
