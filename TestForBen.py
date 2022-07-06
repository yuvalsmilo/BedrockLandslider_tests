

import numpy as np
from landlab.io.native_landlab import save_grid, load_grid
import matplotlib.pyplot as plt
from bedrock_landslider.bedrock_landslider import BedrockLandslider
from landlab.components import PriorityFloodFlowRouter

## Load the grid

grid_path = '/YourPath/gridd.grid'
grid = load_grid(grid_path)
topo = grid.at_node['topographic__elevation']
br_topo = grid.at_node['bedrock__elevation']
topo2D = grid.node_vector_to_raster(topo)
br2D = grid.node_vector_to_raster(br_topo)

## Plotting for being sure everyhting is alright
fig, ax = plt.subplots()
ax.plot(topo2D[:, 1], color='b', linewidth=1, label='Topo')
ax.plot(br2D[:, 1], color='k', linewidth=1, label='Bedrock')
ax.set_xlim([0, 120])
ax.set_ylim([np.min(topo2D) - 5, np.max(topo2D) + 5])
ax.legend(loc='upper left')
ax.set_xlabel('Distance [m]')
ax.set_ylabel('Elevation [m]')
plt.tight_layout()
plt.show()

fr = PriorityFloodFlowRouter(
    grid,
    flow_metric="D8",
    separate_hill_flow=True,
    hill_flow_metric="Quinn",
    update_hill_flow_instantaneous=True,depression_handler='fill'
)

fr.run_one_step()
hy = BedrockLandslider(
    grid,
    angle_int_frict = 1,
    threshold_slope = 1000,
    cohesion_eff = 1e6,
    landslides_return_time = 1,
    landslides_on_boundary_nodes = False,
)


# Main loop
for storm_cnt in range(1,25):
    [a1, a2] = hy.run_one_step(dt=100)
    topo2D = grid.node_vector_to_raster(topo)
    br2D = grid.node_vector_to_raster(br_topo)
    fig, ax = plt.subplots()
    ax.plot(topo2D[:, 1], color='b', linewidth=1, label='Topo')
    ax.plot(br2D[:, 1], color='k', linewidth=1, label='Bedrock')
    ax.set_xlim([0, 120])
    ax.set_ylim([np.min(topo2D) - 5, np.max(topo2D) + 5])
    ax.legend(loc='upper left')
    ax.set_xlabel('Distance [m]')
    ax.set_ylabel('Elevation [m]')
    plt.tight_layout()
    plt.show()



