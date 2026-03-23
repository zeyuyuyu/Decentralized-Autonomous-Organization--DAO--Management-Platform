from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional

class ProposalStatus(Enum):
    DRAFT = 'draft'
    ACTIVE = 'active' 
    PASSED = 'passed'
    FAILED = 'failed'
    EXECUTED = 'executed'

class Proposal:
    def __init__(self, id: str, title: str, description: str, creator: str,
                 voting_period_days: int = 7):
        self.id = id
        self.title = title
        self.description = description
        self.creator = creator
        self.status = ProposalStatus.DRAFT
        self.created_at = datetime.now()
        self.voting_ends_at = self.created_at + timedelta(days=voting_period_days)
        self.votes_for = 0
        self.votes_against = 0
        self.voters = set()

    def get_result(self) -> Optional[bool]:
        if datetime.now() < self.voting_ends_at:
            return None
        return self.votes_for > self.votes_against

class GovernanceSystem:
    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}
        self.quorum_threshold = 100  # Minimum votes needed
        self.execution_delay_hours = 24

    def create_proposal(self, id: str, title: str, description: str, 
                       creator: str) -> Proposal:
        if id in self.proposals:
            raise ValueError(f'Proposal with ID {id} already exists')
        
        proposal = Proposal(id, title, description, creator)
        self.proposals[id] = proposal
        return proposal

    def activate_proposal(self, proposal_id: str) -> None:
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')
        
        if proposal.status != ProposalStatus.DRAFT:
            raise ValueError(f'Proposal {proposal_id} is not in draft status')
            
        proposal.status = ProposalStatus.ACTIVE
        
    def cast_vote(self, proposal_id: str, voter: str, vote_for: bool) -> None:
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')
            
        if proposal.status != ProposalStatus.ACTIVE:
            raise ValueError(f'Proposal {proposal_id} is not active')
            
        if voter in proposal.voters:
            raise ValueError(f'Voter {voter} has already voted')
            
        if datetime.now() > proposal.voting_ends_at:
            raise ValueError(f'Voting period has ended for proposal {proposal_id}')
        
        if vote_for:
            proposal.votes_for += 1
        else:
            proposal.votes_against += 1
        proposal.voters.add(voter)

    def process_proposal(self, proposal_id: str) -> None:
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')
            
        if proposal.status != ProposalStatus.ACTIVE:
            raise ValueError(f'Proposal {proposal_id} is not active')
            
        if datetime.now() < proposal.voting_ends_at:
            raise ValueError(f'Voting period has not ended')
            
        total_votes = proposal.votes_for + proposal.votes_against
        if total_votes < self.quorum_threshold:
            proposal.status = ProposalStatus.FAILED
            return
            
        result = proposal.get_result()
        if result:
            proposal.status = ProposalStatus.PASSED
        else:
            proposal.status = ProposalStatus.FAILED

    def execute_proposal(self, proposal_id: str) -> None:
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')
            
        if proposal.status != ProposalStatus.PASSED:
            raise ValueError(f'Proposal {proposal_id} has not passed')
            
        execution_time = proposal.voting_ends_at + timedelta(hours=self.execution_delay_hours)
        if datetime.now() < execution_time:
            raise ValueError(f'Execution delay has not passed')
            
        # Execute proposal logic here
        proposal.status = ProposalStatus.EXECUTED

    def get_active_proposals(self) -> List[Proposal]:
        return [p for p in self.proposals.values() 
                if p.status == ProposalStatus.ACTIVE]

    def get_proposal_history(self, proposal_id: str) -> Dict:
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f'Proposal {proposal_id} not found')
            
        return {
            'id': proposal.id,
            'title': proposal.title,
            'description': proposal.description,
            'creator': proposal.creator,
            'status': proposal.status.value,
            'created_at': proposal.created_at,
            'voting_ends_at': proposal.voting_ends_at,
            'votes_for': proposal.votes_for,
            'votes_against': proposal.votes_against,
            'total_voters': len(proposal.voters)
        }