voting = False  # stores if vote is in progress


class Vote:
    voters = []

    def __init__(self, voters):
        self.voters = voters
        print(voters)
