import json

import networkx as nx

from app import NetworkApp
from rule import MatchPattern
from te_objs import PassByPathObjective, MinLatencyObjective, MaxBandwidthObjective
from utils_json import DefaultEncoder

class TEApp(NetworkApp):
    def __init__(self, topo_file, json_file, of_controller=None, priority=2):
        super(TEApp, self).__init__(topo_file, json_file, of_controller, priority)
        self.pass_by_paths_obj = [] # a list of PassByPathObjective objects 
        self.min_latency_obj = [] # a list of MinLatencyObjective objects
        self.max_bandwidth_obj = [] # a list of MaxBandwidthObjective objects
    
    def add_pass_by_path_obj(self, pass_by_obj):
        self.pass_by_paths_obj.append(pass_by_obj)

    def add_min_latency_obj(self, min_lat_obj):
        self.min_latency_obj.append(min_lat_obj)

    def add_max_bandwidth_obj(self, max_bw_obj):
        self.max_bandwidth_obj.append(max_bw_obj)

    # This function reads the TE objectives in the `self.json_file`
    # Then, parses the JSON objects to the three list:
    #       self.pass_by_paths_obj
    #       self.min_latency_obj
    #       self.max_bandwidth_obj
    def from_json(self):
        with open('%s'% self.json_file) as f:
            te_objectives = json.load(f)
            if 'pass_by_paths' in te_objectives:
                pass_by_paths = te_objectives['pass_by_paths']
                for objective_data in pass_by_paths:
                    match_pattern_data = objective_data['match_pattern']
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
                    pass_by_obj = PassByPathObjective(
                        match_pattern = match_pattern,
                        switches = objective_data['switches'],
                        symmetric = objective_data['symmetric']
                    )
                    self.add_pass_by_path_obj(pass_by_obj)

            if 'min_latency' in te_objectives:
                min_latency = te_objectives['min_latency']
                for objective_data in min_latency:
                    match_pattern_data = objective_data['match_pattern']
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
                    min_lat_obj = MinLatencyObjective(
                        match_pattern = match_pattern,
                        src_switch = objective_data['src_switch'],
                        dst_switch = objective_data['dst_switch'],
                        symmetric = objective_data['symmetric']
                    )
                    self.add_min_latency_obj(min_lat_obj)
    
    # Translates the TE objectives to the `json_file`
    def to_json(self, json_file):
        json_dict = {
            'pass_by_paths': self.pass_by_paths_obj,
            'min_latency': self.min_latency_obj,
            'max_bandwidth': self.max_bandwidth_obj,
        }

        with open('%s'% json_file, 'w', encoding='utf-8') as f:
            json.dump(json_dict, f, ensure_ascii=False, indent=4, cls=DefaultEncoder)

    # This function translates the objectives in `self.pass_by_paths_obj` to a list of Rules in `self.rules`
    # It should: 
    #   call `self.calculate_rules_for_path` as needed
    #   handle traffic in reverse direction when `symmetric` is True 
    #   call `self.send_openflow_rules()` at the end
    def provision_pass_by_paths(self):
        self.rules = []
        # TODO: complete

    # This function translates the objectives in `self.min_latency_obj` to a list of Rules in `self.rules`
    # It should: 
    #   call `self.calculate_rules_for_path` as needed
    #   consider using the function `networkx.shortest_path` in the networkx package
    #   handle traffic in reverse direction when `symmetric` is True 
    #   call `self.send_openflow_rules()` at the end
    def provision_min_latency_paths(self):
        self.rules = []
        # TODO: complete

    # BONUS: 
    # This function translates the objectives in `self.max_bandwidth_obj` to a list of Rules in `self.rules`
    # It should: 
    #   call `self.calculate_rules_for_path` as needed
    #   consider what algorithms to use (from networkx) to calculate the paths
    #   handle traffic in reverse direction when `symmetric` is True 
    #   call `self.send_openflow_rules()` at the end
    def provision_max_bandwidth_paths(self):
        pass
    
    # BONUS: Used to react to changes in the network (the controller notifies the App)
    def on_notified(self, **kwargs):
        pass
