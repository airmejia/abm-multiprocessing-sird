import numpy as np
import time
import os
import sys
from multiprocessing import Pool, cpu_count
import math
import platform
import cpuinfo

class Agent:
    def __init__(self, world, start_pos, status, days_infection, delta):
        self.world = world
        self.position = start_pos
        self.agent_id = None
        self.status = status
        self.days_infection = days_infection
        self.delta = delta
        
    def simulate_step(self):
        """Move the agent randomly within grid boundaries."""
        dx = np.random.choice([-self.delta, 0, self.delta])
        dy = np.random.choice([-self.delta, 0, self.delta])
        # Calculate new position and ensure the agent stays within the grid
        new_x = max(0, min(self.world.grid_size[0] - 1, self.position[0] + dx))
        new_y = max(0, min(self.world.grid_size[1] - 1, self.position[1] + dy))
        self.position = (new_x, new_y)
        # Check neighbors
        res = self.status
        x_low = self.position[0] - self.world.cd
        x_high = self.position[0] + self.world.cd
        y_low = self.position[1] - self.world.cd
        y_high = self.position[1] + self.world.cd
        neighbors = self.world.filter_population(self.position[0], self.position[1], x_low, x_high, y_low, y_high, self)
        # Update status 
        if (self.status == 'susceptible' ):
            for neighbor in neighbors:
                if (neighbor.status == 'infected'):
                    res = 'infected'
        
        #if (self.status=='infected'):
        #    for neighbor in neighbors:
        #        if (neighbor.status != 'infected') & (neighbor.status != 'dead'):
        #            neighbor.status = 'infected'
        #            self.world.population[neighbor.agent_id] = neighbor
        #elif (self.status!='infected') & (self.status != 'recovered') & (self.status != 'dead'):
        #    for neighbor in neighbors:
        #        if (neighbor.status == 'infected'):
        #            res = 'infected'
                    
        self.status = res
        if(self.status=='infected'):
            self.days_infection+=1
            if(self.days_infection>self.world.dInf):
                isdead = np.random.rand()
                if(isdead<=self.world.kapa):
                    self.status = 'dead'
                else:
                    self.status = 'recovered'
        
        self.world.population[self.agent_id] = self
                    
class World:
    def __init__(self, gridsize, populationsize, movements, dInf, delta, kapa, cd):
        self.grid_size = gridsize
        self.population_size = populationsize
        self.movements = movements
        self.dInf = dInf
        self.delta = delta
        self.kapa = kapa
        self.cd = cd
        
        self.population = []
        self.susceptible = np.zeros(movements)
        self.infected = np.zeros(movements)
        self.recovered = np.zeros(movements)
        self.dead = np.zeros(movements)
        self.next_id = 0
    
    def add_agent(self,agent):
        agent.agent_id = self.next_id
        self.population.append(agent)
        self.population[self.next_id] = agent
        self.next_id += 1
        
    def filter_population(self, x, y, x_low, x_high, y_low, y_high, calling_agent):
        return [
            agent for agent in self.population
            #if (agent is not calling_agent) and
            #(x_low <= agent.position[0] <= x_high) and
            #(y_low <= agent.position[1] <= y_high)
            if (agent is not calling_agent) and
            (np.sqrt( (agent.position[1]-y)**2 + (agent.position[0]-x)**2 ) < self.cd)
        ]
    
    def simulate(self, movements):
        
        
        for step in range(movements):
            for agent in self.population:
                agent.simulate_step()
            
            # Update the counts of susceptible and infected agents
            susceptible_count = sum(1 for agent in self.population if agent.status == "susceptible")
            infected_count = sum(1 for agent in self.population if agent.status == "infected")
            recovered_count = sum(1 for agent in self.population if agent.status == "recovered")
            dead_count = sum(1 for agent in self.population if agent.status == "dead")

            # Extend the arrays if needed
            if len(self.susceptible) <= step:
                self.susceptible.append(0)
            if len(self.infected) <= step:
                self.infected.append(0)

            self.susceptible[step] = susceptible_count
            self.infected[step] = infected_count
            self.recovered[step] = recovered_count
            self.dead[step] = dead_count
        
        #print("Susceptibles: ",the_grid.count_susceptible())
        #print("Infected: ",the_grid.count_infected())
        #print("Recovered: ",the_grid.count_recovered())
        #print("Dead: ",the_grid.count_dead())
        
    
    def count_susceptible(self):
        return sum(1 for agent in self.population if agent.status == 'susceptible')
    
    def count_infected(self):
        return sum(1 for agent in self.population if agent.status == 'infected')
    
    def count_recovered(self):
        return sum(1 for agent in self.population if agent.status == 'recovered')
    
    def count_dead(self):
        return sum(1 for agent in self.population if agent.status == 'dead')

def simulate_agent_step(agent):
    agent.simulate_step()
    return agent

def simulation(parameters):
    row_idx, col_idx, grid_size, num_simulations, num_movements, population_size, dInf, delta, kapa, cd, init_row, init_col = parameters
    #print(f"-- Start Sim-{id},{jd}: {time.strftime("%Y-%m-%d %H:%M:%S")}")
    print_cell(init_row + row_idx, init_col + col_idx * 7, 'init', 's')
    start_time = time.time()
    status_list = ('susceptible', 'infected', 'recovered', 'dead')
    colors_list = ('orange', 'red', 'green', 'blue')
    markers_list = ('.', '*', '+', 'x')
    #markers_sizes = (ms*2, ms, ms, ms*0.6)
    
    the_grid = World(grid_size, population_size, num_movements, dInf, delta, kapa, cd)
    
    for _ in range(population_size):
        agent_x = np.random.uniform(0, grid_size[0])
        agent_y = np.random.uniform(0, grid_size[1])
        if(_==0):
            newAgent = Agent(the_grid, (agent_x, agent_y), 'infected', 0, delta)
        else:
            newAgent = Agent(the_grid, (agent_x, agent_y), 'susceptible', 0, delta)
        the_grid.add_agent(newAgent)
    
    #plotPopulation('Initial Population '+str(population_size), 'Position x', 'Position y', the_grid.population, status_list, colors_list, markers_list, markers_sizes)
    print_cell(init_row + row_idx, init_col + col_idx * 7, 'run', 's')
    the_grid.simulate(num_movements)
    
    end_time = time.time()
    execution_time = end_time - start_time
    print_cell(init_row + row_idx, init_col + col_idx * 7, execution_time, 'f')

    #plotPopulation('Final Population '+str(population_size), 'Position x', 'Position y', the_grid.population, status_list, colors_list, markers_list, markers_sizes)
      
    S = the_grid.susceptible
    I = the_grid.infected
    R = the_grid.recovered
    D = the_grid.dead
    t = np.linspace(1,num_movements,num_movements)
    
    # Graph results
    #graph_data = np.asmatrix([S,I,R,D])
    #plotLine('SIRD agent based model', 'Time t, [days]', 'Numbers of individuals', t, graph_data, colors_list, status_list)

def initialize_table(init_row, init_col, rows, cols):
    temp = [list(['-' for _ in range(cols)]) for _ in range(rows)]
    for i, row in enumerate(temp):
        move_cursor(init_row + i, init_col)
        print("".join(f"{val:>7}" for val in row))

def move_cursor(row, col):
    """Move the cursor to a specific (x, y) position in the terminal."""
    print(f"\033[{row};{col}H", end="")

def print_cell(row, col, value, valtype):
    """Print a value at a specific cell in the terminal."""
    move_cursor(row, col)
    if(valtype=='f'):
        print(f"{value:7.2f}", end="", flush=True)
    elif(valtype=='s'):
        print(f"{value:>7}", end="", flush=True)
    elif(valtype=='i'):
        print(f"{value:7}", end="", flush=True)


def print_table(table, start_row=1, start_col=1):
    """Print the entire table starting from a specific terminal position."""
    for i, row in enumerate(table):
        move_cursor(start_row + i, start_col)
        print("".join(f"{val:7.2f}" for val in row))

if __name__ == '__main__':
    # Define grid size, number of movements and ppulation
    grid_size = (25, 20)
    num_simulations= 96
    num_movements = 50
    population_size = 1000
    dInf = 21
    delta = 0.5
    kapa = 0.15
    cd = 0.5

    cols = 10
    rows = math.ceil(num_simulations / cols)
    init_row = 13
    init_col = 1
    
    print("\033[2J")  
    os.system('cls' if os.name == 'nt' else 'clear')

    start_time = time.time()
    print(f"Start PROCESS {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("+++++++++++++++++++++++++++++++++++++")
    print("Platform: ",platform.platform())
    print("Processor: ",cpuinfo.get_cpu_info()['brand_raw'])
    print("+++++++++++++++++++++++++++++++++++++")
    print("Population: ",population_size)
    print("Grid size: ",grid_size)
    print(f"Population density: {population_size /(grid_size[0]*grid_size[1]):3.2f}")
    print("Simulations: ",num_simulations)
    print("Ticks: ",num_movements)
    pool = Pool()
    print(f"Using {cpu_count()} CPU cores")
    print("+++++++++++++++++++++++++++++++++++++")
    initialize_table(init_row, init_col, rows, cols)
    
    parameters = [grid_size, num_simulations, num_movements, population_size, dInf, delta, kapa, cd]
    simulations_data = []
    i = 0
    j = 0
    for k in range(num_simulations):
        simulations_data.append([i, j, grid_size, num_simulations, num_movements, population_size, dInf, delta, kapa, cd, init_row, init_col])
        print_cell(init_row + i, init_col + j * 7, k+1, 'i')
        if(j<cols-1):
            j += 1
        else:
            i += 1
            j = 0
    
    results = pool.map(simulation, simulations_data)
    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"\nFinishing PROCESS {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"TOTAL TIME OF EXECUTION {execution_time:.2f} seconds")
    
    
    

    
