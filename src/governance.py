import json
import time
from typing import List, Tuple, Dict

class Proposal:
    def __init__(self, title: str, description: str, author: str, start_time: int, end_time: int, vote_results: Dict[str, int]):
        self.title = title
        self.description = description
        self.author = author
        self.start_time = start_time
        self.end_time = end_time
        self.vote_results = vote_results

    def is_active(self) -> bool:
        current_time = int(time.time())
        return self.start_time <= current_time <= self.end_time

    def get_vote_tally(self) -> Tuple[int, int]:
        yes_votes = self.vote_results.get('yes', 0)
        no_votes = self.vote_results.get('no', 0)
        return yes_votes, no_votes

    def is_passed(self) -> bool:
        yes_votes, no_votes = self.get_vote_tally()
        return yes_votes > no_votes

class GovernanceModule:
    def __init__(self, dao_members: List[str], quorum_percentage: float = 0.2, passing_percentage: float = 0.6):
        self.dao_members = dao_members
        self.quorum_percentage = quorum_percentage
        self.passing_percentage = passing_percentage
        self.proposals: List[Proposal] = []

    def submit_proposal(self, proposal: Proposal) -> bool:
        self.proposals.append(proposal)
        return True

    def vote_on_proposal(self, member: str, proposal_idx: int, vote: str) -> bool:
        if member not in self.dao_members:
            return False

        if proposal_idx < 0 or proposal_idx >= len(self.proposals):
            return False

        proposal = self.proposals[proposal_idx]
        if not proposal.is_active():
            return False

        proposal.vote_results[vote] = proposal.vote_results.get(vote, 0) + 1
        return True

    def execute_proposal(self, proposal_idx: int) -> bool:
        if proposal_idx < 0 or proposal_idx >= len(self.proposals):
            return False

        proposal = self.proposals[proposal_idx]
        if not proposal.is_passed():
            return False

        # Execute the proposal logic here
        print(f'Executing proposal: {proposal.title}')
        return True

    def get_active_proposals(self) -> List[Proposal]:
        return [p for p in self.proposals if p.is_active()]

    def get_passed_proposals(self) -> List[Proposal]:
        return [p for p in self.proposals if p.is_passed()]
