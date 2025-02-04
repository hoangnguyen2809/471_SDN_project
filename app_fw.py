import json

from app import NetworkApp
from rule import Action, ActionType, Rule, MatchPattern
from utils_json import DefaultEncoder

def parse_action(d):
    if 'action_type' in d:
        return {
            'action_type': getattr(ActionType, d['action_type']),
            'out_port': d.get('out_port', None)
            }
    return d


class FirewallApp(NetworkApp):
    def __init__(self, json_file, of_controller=None, priority=3):
        super(FirewallApp, self).__init__(None, json_file, of_controller, priority)

    # Translates the firewall policy file in `self.json_file` to a list of Rule objects `self.rules`
    def from_json(self):
        with open('%s'% self.json_file) as f:
            rules = json.load(f, object_hook=parse_action)
        
        for entry in rules:
            switch_id = entry['switch_id']
            
            match_pattern_data = entry['match_pattern']
            match_pattern = MatchPattern(
                src_mac = match_pattern_data.get('src_mac'),
                dst_mac = match_pattern_data.get('dst_mac'),
                mac_proto = match_pattern_data.get('mac_proto'),
                ip_proto = match_pattern_data.get('ip_proto'),
                src_ip = match_pattern_data.get('src_ip'),
                dst_ip = match_pattern_data.get('dst_ip'),
                src_port = match_pattern_data.get('src_port'),
                dst_port = match_pattern_data.get('dst_port'),
                in_port = match_pattern_data.get('in_port')
            )

            action_data = entry['action']
            action = Action(
                action_type = ActionType(action_data['action_type']),
                out_port = action_data.get('out_port')
            )

            rule = Rule(switch_id=switch_id, match_pattern=match_pattern, action=action)
            self.add_rule(rule)

    # Writes the firewall policy to a JSON file
    def to_json(self, json_file):
        with open('%s'% json_file, 'w', encoding='utf-8') as f:
            json.dump(self.rules, f, ensure_ascii=False, indent=4, cls=DefaultEncoder)

    # This function calls `send_openflow_rules` only.
    # This is because the policy is the actual OpenFlow rules to be sent.
    def calculate_firewall_rules(self):
        self.send_openflow_rules()

    # BONUS: Used to react to changes in the network (the controller notifies the App)
    def on_notified(self, **kwargs):
        pass
