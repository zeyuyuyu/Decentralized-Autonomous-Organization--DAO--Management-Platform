from typing import Dict, List, Optional
from datetime import datetime, timedelta
import math

class Proposal:
    def __init__(self, id: str, title: str, description: str, creator: str, voting_period_days: int):
        self.id = id
        self.title = title
        self.description = description
        self.creator = creator
        self.votes_for = {}  # address -> vote weight
        self.votes_against = {}  # address -> vote weight
        self.created_at = datetime.now()
        self.ends_at = self.created_at + timedelta(days=voting_period_days)
        self.executed = False
        self.passed = False

class GovernanceSystem:
    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}
        self.token_balances: Dict[str, float] = {}  # address -> token balance
        self.proposal_counter = 0

    def create_proposal(self, title: str, description: str, creator: str, voting_period_days: int = 7) -> str:
        """Create a new governance proposal"""
        if self.token_balances.get(creator, 0) < 100:
            raise ValueError('Insufficient tokens to create proposal (minimum 100)')

        proposal_id = f'PROP-{self.proposal_counter}'
        self.proposal_counter += 1
        
        proposal = Proposal(proposal_id, title, description, creator, voting_period_days)
        self.proposals[proposal_id] = proposal
        return proposal_id

    def cast_vote(self, proposal_id: str, voter: str, vote_weight: float, support: bool) -> bool:
        """Cast a quadratic vote on a proposal"""
        if proposal_id not in self.proposals:
            raise ValueError('Invalid proposal ID')
        
        proposal = self.proposals[proposal_id]
        
        if datetime.now() > proposal.ends_at:
            raise ValueError('Voting period has ended')
            
        voter_balance = self.token_balances.get(voter, 0)
        max_vote_weight = math.sqrt(voter_balance)
        
        if vote_weight > max_vote_weight:
            raise ValueError(f'Vote weight exceeds maximum allowed ({max_vote_weight})')
            
        if support:
            proposal.votes_for[voter] = vote_weight
        else:
            proposal.votes_against[voter] = vote_weight
            
        return True

    def tally_votes(self, proposal_id: str) -> Dict:
        """Calculate final vote tallies using quadratic voting"""
        if proposal_id not in self.proposals:
            raise ValueError('Invalid proposal ID')
            
        proposal = self.proposals[proposal_id]
        
        if datetime.now() < proposal.ends_at:
            raise ValueError('Voting period still active')
            
        total_for = sum(weight * weight for weight in proposal.votes_for.values())
        total_against = sum(weight * weight for weight in proposal.votes_against.values())
        
        proposal.passed = total_for > total_against
        
        return {
            'total_for': total_for,
            'total_against': total_against,
            'passed': proposal.passed,
            'voter_count': len(proposal.votes_for) + len(proposal.votes_against)
        }

    def execute_proposal(self, proposal_id: str) -> bool:
        """Execute a passed proposal"""
        if proposal_id not in self.proposals:
            raise ValueError('Invalid proposal ID')
            
        proposal = self.proposals[proposal_id]
        
        if not proposal.passed:
            raise ValueError('Proposal has not passed')
            
        if proposal.executed:
            raise ValueError('Proposal already executed')
            
        # Implementation would connect to smart contract or other execution mechanism
        proposal.executed = True
        return True

    def get_proposal(self, proposal_id: str) -> Optional[Proposal]:
        """Retrieve proposal details"""
        return self.proposals.get(proposal_id)

    def get_active_proposals(self) -> List[Proposal]:
        """Get list of currently active proposals"""
        now = datetime.now()
        return [p for p in self.proposals.values() 
                if not p.executed and now <= p.ends_at]

    def get_voter_power(self, address: str) -> float:
        """Calculate voter's voting power using quadratic formula"""
        balance = self.token_balances.get(address, 0)
        return math.sqrt(balance)
