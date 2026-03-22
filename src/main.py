import os
import json
from typing import List, Dict

class DAOGovernance:
    def __init__(self, dao_config_path: str):
        with open(dao_config_path, 'r') as f:
            self.dao_config = json.load(f)

    def propose_new_policy(self, proposal: Dict):
        """Propose a new policy to the DAO for voting."""
        self.dao_config['proposals'].append(proposal)
        self.save_dao_config()

    def cast_vote(self, voter_address: str, proposal_id: str, vote: bool):
        """Cast a vote on a specific proposal."""
        proposal = next((p for p in self.dao_config['proposals'] if p['id'] == proposal_id), None)
        if proposal:
            proposal['votes'][voter_address] = vote
            self.save_dao_config()

    def tally_votes(self, proposal_id: str) -> bool:
        """Tally the votes for a specific proposal."""
        proposal = next((p for p in self.dao_config['proposals'] if p['id'] == proposal_id), None)
        if proposal:
            yes_votes = sum(1 for v in proposal['votes'].values() if v)
            no_votes = sum(1 for v in proposal['votes'].values() if not v)
            return yes_votes > no_votes
        return False

    def save_dao_config(self):
        """Save the DAO configuration to the file."""
        with open(self.dao_config_path, 'w') as f:
            json.dump(self.dao_config, f, indent=2)

if __name__ == '__main__':
    dao_governance = DAOGovernance('dao_config.json')
    proposal = {
        'id': '1',
        'title': 'Increase Developer Funding',
        'description': 'Increase the monthly budget for the core development team.',
        'votes': {}
    }
    dao_governance.propose_new_policy(proposal)
    dao_governance.cast_vote('0x123456789abcdef', '1', True)
    dao_governance.cast_vote('0xfedcba9876543210', '1', False)
    print(dao_governance.tally_votes('1'))