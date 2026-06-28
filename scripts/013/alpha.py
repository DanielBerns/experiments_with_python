import yaml
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict

# Define state indices for clarity
STATE_MONEY = 0
STATE_FOOD = 1
STATE_GOODS = 2
STATE_HAPPINESS = 3
STATE_ENERGY = 4
STATE_LABELS = ['Money', 'Food', 'Goods', 'Happiness', 'Energy']

class Agent:
    def __init__(self, agent_id, agent_type, config):
        self.id = agent_id
        self.agent_type = agent_type
        self.params = config['agent_types'][agent_type]
        self.defaults = config['defaults']

        # Initialize state from a normal distribution
        mean = self.params['initial_state_mean']
        std = self.params['initial_state_std']
        self.state = np.random.normal(mean, std)
        self.state = np.clip(
            self.state, self.defaults['state_mins'], self.defaults['state_maxs']
        )

        # Pre-compile matrices
        self.A = np.array(self.params['A_matrix'])
        self.B = np.array(self.params['B_matrix'])

    def decide_action(self, graph):
        # Placeholder for decision logic.
        # In a full model, this would be where agents decide to buy/sell.
        # For now, we simulate random interactions.
        neighbors = list(graph.neighbors(self.id))
        if not neighbors:
            return None

        # Simple decision: try to trade with a random neighbor
        target_id = random.choice(neighbors)
        return ('trade', target_id)

    def update_state(self, inputs):
        """Update state based on internal dynamics and external inputs."""
        # s_k+1 = A*s_k + B*x_k
        self.state = self.A @ self.state + self.B @ inputs

        # Apply hard limits (clipping)
        self.state = np.clip(
            self.state, self.defaults['state_mins'], self.defaults['state_maxs']
        )

class Simulation:
    def __init__(self, config):
        self.config = config
        self.agents = []
        self.graph = nx.Graph()
        self.history = self._initialize_history()

        # Create agents based on distribution
        agent_counts = {
            name: int(dist * config['simulation']['total_agents'])
            for name, dist in config['agent_distribution'].items()
        }

        agent_id_counter = 0
        for agent_type, count in agent_counts.items():
            for _ in range(count):
                agent = Agent(agent_id_counter, agent_type, config)
                self.agents.append(agent)
                self.graph.add_node(agent.id)
                agent_id_counter += 1

        # Create initial network links
        for agent in self.agents:
            num_links = config['simulation']['initial_links_per_agent']
            possible_targets = [
                other.id for other in self.agents if other.id != agent.id and not self.graph.has_edge(agent.id, other.id)
            ]
            if len(possible_targets) < num_links:
                continue

            targets = random.sample(possible_targets, num_links)
            for target_id in targets:
                self.graph.add_edge(agent.id, target_id, weight=0) # weight tracks inactivity

    def _initialize_history(self):
        """Prepares the data structure for storing simulation results."""
        history = {
            'time': [],
            'avg_connections': [],
            'total_avg_wealth': [],
            'group_avg_states': defaultdict(lambda: defaultdict(list))
        }
        return history

    def _record_history(self, k):
        """Records the state of the system at time step k."""
        self.history['time'].append(k)

        # Overall metrics
        total_wealth = sum(agent.state[STATE_MONEY] for agent in self.agents)
        self.history['total_avg_wealth'].append(total_wealth / len(self.agents))
        avg_conn = sum(dict(self.graph.degree()).values()) / self.graph.number_of_nodes()
        self.history['avg_connections'].append(avg_conn)

        # --- NEW: Group-level metrics ---
        group_sums = defaultdict(lambda: np.zeros(len(STATE_LABELS)))
        group_counts = defaultdict(int)

        for agent in self.agents:
            group_sums[agent.agent_type] += agent.state
            group_counts[agent.agent_type] += 1

        for agent_type, total_state in group_sums.items():
            avg_state = total_state / group_counts[agent_type]
            for i, label in enumerate(STATE_LABELS):
                self.history['group_avg_states'][agent_type][label].append(avg_state[i])
        # --- End of new section ---

    def _negotiate(self, agent_a, agent_b):
        """Simple negotiation placeholder."""
        # A wants to sell goods, B wants to buy
        # Price is determined by a mix of their happiness and greediness
        price_a = 10 - agent_a.state[STATE_HAPPINESS] / 20
        price_b = 12 - agent_b.state[STATE_HAPPINESS] / 20

        # Simple 1-round negotiation
        final_price = (price_a + price_b) / 2

        if agent_a.state[STATE_GOODS] >= 1 and agent_b.state[STATE_MONEY] >= final_price:
            return final_price, 1 # price, quantity
        return None, None

    def step(self, k):
        random.shuffle(self.agents) # Process agents in random order each step

        for agent in self.agents:
            action = agent.decide_action(self.graph)
            if action:
                action_type, target_id = action
                if action_type == 'trade':
                    other_agent = self.agents[target_id]

                    price, quantity = self._negotiate(agent, other_agent)

                    if price is not None:
                        # Agent A (seller) inputs
                        inputs_a = np.zeros(len(STATE_LABELS))
                        inputs_a[STATE_MONEY] = price * quantity

                        # Agent B (buyer) inputs
                        inputs_b = np.zeros(len(STATE_LABELS))
                        inputs_b[STATE_MONEY] = -price * quantity
                        inputs_b[STATE_GOODS] = quantity

                        agent.state[STATE_GOODS] -= quantity
                        agent.update_state(inputs_a)
                        other_agent.update_state(inputs_b)

        # Update all agents' internal state once after all interactions
        for agent in self.agents:
            agent.update_state(np.zeros(len(STATE_LABELS))) # Update with no external input

        self._record_history(k)

    def run(self):
        time_steps = self.config['simulation']['time_steps']
        for k in range(time_steps):
            self.step(k)
            if k % 100 == 0:
                print(f"--- Step {k}/{time_steps} ---")
        print("Simulation complete.")

def plot_average_wealth(history):
    """Plots the overall average wealth in a separate figure."""
    plt.figure(figsize=(12, 6))
    plt.plot(history['time'], history['total_avg_wealth'], color='tab:blue')
    plt.title('Evolution of Total Average Wealth')
    plt.xlabel('Time Step')
    plt.ylabel('Total Average Wealth')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

def plot_average_connections(history):
    """Plots the average network connections in a separate figure."""
    plt.figure(figsize=(12, 6))
    plt.plot(history['time'], history['avg_connections'], color='tab:red')
    plt.title('Evolution of Average Connections')
    plt.xlabel('Time Step')
    plt.ylabel('Average Connections')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# --- Plotting function for group-level data, now creating separate figures ---
def plot_single_group_state(history, state_label):
    """Plots the evolution of a single state variable, averaged by agent type."""
    agent_types = history['group_avg_states'].keys()

    plt.figure(figsize=(14, 8))

    for agent_type in agent_types:
        plt.plot(
            history['time'],
            history['group_avg_states'][agent_type][state_label],
            label=agent_type
        )

    plt.title(f'Evolution of Average {state_label} by Agent Type', fontsize=16)
    plt.xlabel('Time Step')
    plt.ylabel(f'Average {state_label}')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
# --- End of plotting function section ---


if __name__ == '__main__':
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: config.yaml not found. Please run generate_config.py first.")
        exit()

    sim = Simulation(config)
    sim.run()

    # Generate plots - each in a separate figure
    plot_average_wealth(sim.history)
    plot_average_connections(sim.history)
    for label in STATE_LABELS:
        plot_single_group_state(sim.history, label)

