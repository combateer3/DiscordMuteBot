import threading


class Vote:
    voters = []
    confirmed = []  # members who have voted yes
    active = False
    mutee = None  # person to be muted
    timer = None

    def __init__(self, voters, mutee):
        self.voters = voters
        self.mutee = mutee
        self.timer = threading.Timer(10, self.stop)

    def activate(self):
        self.active = True
        self.timer.start()

    # returns message to respond with
    def confirm(self, member):
        # check if user is a valid voter
        if member not in self.voters:
            return f"Sorry, {member.mention}, you cannot vote in this election!"

        if member not in self.confirmed:
            self.confirmed.append(member)
            return f"Thank you for your vote {member.mention}! Now at {len(self.confirmed)}/{len(self.voters)}"

        return f"Naughty naughty! You already voted {member.mention}"

    # returns true if majority vote
    def is_majority(self):
        if len(self.confirmed) > (len(self.voters) / 2):
            self.timer.cancel()
            return True
        return False

    def stop(self):
        self.active = False
