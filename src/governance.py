import datetime
import json
from typing import List, Dict

class Proposal:
    def __init__(self, title: str, description: str, creator: str, start_date: datetime.datetime, end_date: datetime.datetime, vote_threshold: float):
        self.title = title
        self.description = description
        self.creator = creator
        self.start_date = start_date
        self.end_date = end_date
        self.vote_threshold = vote_threshold
        self.votes = {}

    def cast_vote(self, voter: str, vote: bool):
        self.votes[voter] = vote

    def get_vote_count(self) -> Dict[bool, int]:
        yes_votes = sum(1 for vote in self.votes.values() if vote)
        no_votes = sum(1 for vote in self.votes.values() if not vote)
        return {'yes': yes_votes, 'no': no_votes}

    def is_passed(self) -> bool:
        vote_count = self.get_vote_count()
        total_votes = vote_count['yes'] + vote_count['no']
        return vote_count['yes'] / total_votes >= self.vote_threshold

class DAOGovernance:
    def __init__(self, members: List[str], vote_threshold: float = 0.5):
        self.members = members
        self.vote_threshold = vote_threshold
        self.proposals = []

    def create_proposal(self, title: str, description: str, creator: str, start_date: datetime.datetime, end_date: datetime.datetime) -> Proposal:
        proposal = Proposal(title, description, creator, start_date, end_date, self.vote_threshold)
        self.proposals.append(proposal)
        return proposal

    def cast_vote(self, proposal_index: int, voter: str, vote: bool):
        proposal = self.proposals[proposal_index]
        proposal.cast_vote(voter, vote)

    def get_proposal_status(self, proposal_index: int) -> Dict[str, any]:
        proposal = self.proposals[proposal_index]
        vote_count = proposal.get_vote_count()
        return {
            'title': proposal.title,
            'description': proposal.description,
            'creator': proposal.creator,
            'start_date': proposal.start_date.isoformat(),
            'end_date': proposal.end_date.isoformat(),
            'vote_threshold': proposal.vote_threshold,
            'yes_votes': vote_count['yes'],
            'no_votes': vote_count['no'],
            'passed': proposal.is_passed()
        }