from typing import List, Dict
import time
from dataclasses import dataclass
from enum import Enum

class VoteChoice(Enum):
    YES = 'yes'
    NO = 'no'
    ABSTAIN = 'abstain'

@dataclass
class Vote:
    voter: str
    choice: VoteChoice
    voting_power: float
    timestamp: float

@dataclass 
class Proposal:
    id: str
    title: str
    description: str
    proposer: str
    start_time: float
    end_time: float
    execution_payload: Dict
    votes: List[Vote]
    executed: bool = False
    
class GovernanceSystem:
    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}
        self.min_voting_period = 72 * 3600  # 72 hours
        self.quorum_threshold = 0.4  # 40% participation required
        self.approval_threshold = 0.6  # 60% yes votes required
        
    def create_proposal(self, id: str, title: str, description: str, 
                       proposer: str, execution_payload: Dict) -> Proposal:
        if id in self.proposals:
            raise ValueError('Proposal ID already exists')
            
        proposal = Proposal(
            id=id,
            title=title,
            description=description,
            proposer=proposer,
            start_time=time.time(),
            end_time=time.time() + self.min_voting_period,
            execution_payload=execution_payload,
            votes=[]
        )
        self.proposals[id] = proposal
        return proposal
        
    def cast_vote(self, proposal_id: str, voter: str, 
                  choice: VoteChoice, voting_power: float) -> Vote:
        if proposal_id not in self.proposals:
            raise ValueError('Invalid proposal ID')
            
        proposal = self.proposals[proposal_id]
        
        if time.time() > proposal.end_time:
            raise ValueError('Voting period has ended')
            
        # Remove any existing vote by this voter
        proposal.votes = [v for v in proposal.votes if v.voter != voter]
        
        vote = Vote(
            voter=voter,
            choice=choice,
            voting_power=voting_power,
            timestamp=time.time()
        )
        proposal.votes.append(vote)
        return vote
        
    def get_vote_results(self, proposal_id: str) -> Dict:
        if proposal_id not in self.proposals:
            raise ValueError('Invalid proposal ID')
            
        proposal = self.proposals[proposal_id]
        total_voting_power = sum(vote.voting_power for vote in proposal.votes)
        yes_power = sum(vote.voting_power for vote in proposal.votes 
                       if vote.choice == VoteChoice.YES)
        no_power = sum(vote.voting_power for vote in proposal.votes 
                      if vote.choice == VoteChoice.NO)
                      
        return {
            'total_votes': len(proposal.votes),
            'total_voting_power': total_voting_power,
            'yes_power': yes_power,
            'no_power': no_power,
            'approval_rate': yes_power / total_voting_power if total_voting_power > 0 else 0
        }
        
    def can_execute(self, proposal_id: str) -> bool:
        if proposal_id not in self.proposals:
            return False
            
        proposal = self.proposals[proposal_id]
        if proposal.executed:
            return False
            
        if time.time() <= proposal.end_time:
            return False
            
        results = self.get_vote_results(proposal_id)
        total_power = results['total_voting_power']
        approval_rate = results['approval_rate']
        
        return (total_power >= self.quorum_threshold and 
                approval_rate >= self.approval_threshold)
                
    def execute_proposal(self, proposal_id: str) -> bool:
        if not self.can_execute(proposal_id):
            return False
            
        proposal = self.proposals[proposal_id]
        
        try:
            # Execute the proposal payload
            # This would integrate with other system components
            print(f'Executing proposal {proposal_id}: {proposal.execution_payload}')
            proposal.executed = True
            return True
        except Exception as e:
            print(f'Failed to execute proposal {proposal_id}: {str(e)}')
            return False