import datetime
import hashlib
import json

class Proposal:
    def __init__(self, title, description, creator, start_date, end_date):
        self.title = title
        self.description = description
        self.creator = creator
        self.start_date = start_date
        self.end_date = end_date
        self.votes = {}
        self.id = hashlib.sha256((title + description + creator + str(start_date) + str(end_date)).encode()).hexdigest()

    def add_vote(self, voter, vote):
        self.votes[voter] = vote

    def get_vote_count(self, vote_type):
        count = 0
        for vote in self.votes.values():
            if vote == vote_type:
                count += 1
        return count

    def is_active(self):
        now = datetime.datetime.now()
        return self.start_date <= now <= self.end_date

class DAO:
    def __init__(self, name, members):
        self.name = name
        self.members = members
        self.proposals = []

    def add_proposal(self, proposal):
        self.proposals.append(proposal)

    def vote_on_proposal(self, proposal_id, voter, vote):
        for proposal in self.proposals:
            if proposal.id == proposal_id:
                proposal.add_vote(voter, vote)
                break

    def get_proposal_result(self, proposal_id):
        for proposal in self.proposals:
            if proposal.id == proposal_id:
                yes_votes = proposal.get_vote_count('yes')
                no_votes = proposal.get_vote_count('no')
                if yes_votes > no_votes:
                    return 'Passed'
                else:
                    return 'Failed'
        return 'Proposal not found'

    def execute_proposal(self, proposal_id):
        for proposal in self.proposals:
            if proposal.id == proposal_id:
                if proposal.is_active():
                    if self.get_proposal_result(proposal_id) == 'Passed':
                        # Execute the proposal's logic here
                        print(f'Executing proposal: {proposal.title}')
                    else:
                        print(f'Proposal {proposal.title} failed to pass')
                else:
                    print(f'Proposal {proposal.title} is not active')
                break