import yaml

# Define the entire configuration as a Python dictionary
# This structure mirrors the YAML file exactly.
config_data = {
    'simulation': {
        'total_agents': 500,
        'time_steps': 1000,
        'initial_links_per_agent': 5
    },
    'network_dynamics': {
        'prob_edge_break': 0.01,
        'prob_edge_form': 0.50,
        'link_inactivity_threshold': 10
    },
    'agent_distribution': {
        'greedy_business': 0.10,
        'ideal_business': 0.10,
        'rational_person': 0.50,
        'greedy_person': 0.15,
        'irrational_person': 0.15
    },
    'defaults': {
        'state_mins': [0, 0, 0, 0, 0],
        'state_maxs': [1000000, 100, 100, 100, 100]
    },
    'agent_types': {
        'rational_person': {
            'initial_state_mean': [100, 10, 5, 70, 80],
            'initial_state_std': [20, 3, 2, 10, 5],
            'utility_exponents': {
                'alpha': 0.2, 'beta': 0.3, 'gamma': 0.1, 'delta': 0.2, 'epsilon': 0.2
            },
            'A_matrix': [
                [1.00, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.95, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.00, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.98, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.98]
            ],
            'B_matrix': [
                [1.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0],
                [0.0, 10.0, 2.0, 1.0, 0.0],
                [0.0, 20.0, 0.0, 0.0, 1.0]
            ]
        },
        'greedy_person': {
            'initial_state_mean': [150, 5, 2, 50, 70],
            'initial_state_std': [50, 2, 1, 15, 10],
            'utility_exponents': {
                'alpha': 0.8, 'beta': 0.05, 'gamma': 0.1, 'delta': 0.0, 'epsilon': 0.05
            },
            'A_matrix': [
                [1.001, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.90, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.00, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.95, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.97]
            ],
            'B_matrix': [
                [1.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0],
                [0.0, 10.0, 2.0, 1.0, 0.0],
                [0.0, 20.0, 0.0, 0.0, 1.0]
            ]
        },
        'greedy_business': {
            'initial_state_mean': [500, 5, 50, 50, 90],
            'initial_state_std': [200, 2, 10, 10, 5],
            'utility_exponents': {},
            'A_matrix': [
                [1.002, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.90, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.00, 0.0, -0.1],
                [0.0, 0.0, 0.0, 1.00, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.95]
            ],
            'B_matrix': [
                [1.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0, 0.0],
                [0.0, 5.0, 0.0, 0.0, 1.0]
            ]
        },
        'ideal_business': {
            'initial_state_mean': [200, 10, 60, 60, 80],
            'initial_state_std': [50, 3, 15, 10, 10],
            'utility_exponents': {},
            'A_matrix': [
                [1.00, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.95, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.00, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.98, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.98]
            ],
            'B_matrix': [
                [1.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0],
                [0.0, 5.0, 5.0, 1.0, 0.0],
                [0.0, 15.0, 0.0, 0.0, 1.0]
            ]
        },
        'irrational_person': {
            'initial_state_mean': [80, 8, 8, 50, 60],
            'initial_state_std': [40, 4, 4, 25, 20],
            'utility_exponents': {
                'alpha': 0.1, 'beta': 0.1, 'gamma': 0.5, 'delta': 0.1, 'epsilon': 0.2
            },
            'A_matrix': [
                [0.99, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.85, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.98, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.90, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.95]
            ],
            'B_matrix': [
                [1.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0],
                [0.0, 25.0, 15.0, 1.0, 0.0],
                [0.0, 10.0, 0.0, 0.0, 1.0]
            ]
        }
    }
}

# Define the output filename
output_filename = 'config.yaml'

# Write the dictionary to a YAML file
try:
    with open(output_filename, 'w') as file:
        # Use yaml.dump to write the data
        # sort_keys=False preserves the original order
        yaml.dump(config_data, file, sort_keys=False, indent=2)
    print(f"Successfully generated '{output_filename}'")
except Exception as e:
    print(f"Error generating YAML file: {e}")

