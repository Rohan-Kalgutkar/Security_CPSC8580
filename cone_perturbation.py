from environs import Env
import lgsvl


env = Env()

sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", lgsvl.wise.SimulatorSettings.simulator_host), env.int("LGSVL__SIMULATOR_PORT", lgsvl.wise.SimulatorSettings.simulator_port))
if sim.current_scene == lgsvl.wise.DefaultAssets.map_borregasave:
    sim.reset()
else:
    sim.load(lgsvl.wise.DefaultAssets.map_borregasave, 42)

spawns = sim.get_spawn()

state = lgsvl.AgentState()
forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])
up = lgsvl.utils.transform_to_up(spawns[0])
state.transform = spawns[0]


state.velocity = 6 * forward
ego = sim.add_agent(env.str("LGSVL__VEHICLE_0", lgsvl.wise.DefaultAssets.ego_lincoln2017mkz_apollo5), lgsvl.AgentType.EGO, state)






for i in range(3 * 1):
    # Create controllables in a block
    start = (
        spawns[0].position
        + (18 + (1.0 * (i // 6))) * forward
        - (-1 + (1.0 * (i % 6))) * right
    )
    end = start + 10 * forward

    state = lgsvl.ObjectState()
    state.transform.position = start
    state.transform.rotation = spawns[0].rotation
    

    # add controllable
    o = sim.controllable_add("TrafficCone", state)


print("\nAdded {} Traffic Cones".format(i + 1))




seconds = 16
input("\nPress Enter to run simulation for {} seconds".format(seconds))
print("\nRunning simulation for {} seconds...".format(seconds))


controllables1 = sim.get_controllables("signal")
print("\n# List of controllable objects in {} scene:".format(lgsvl.wise.DefaultAssets.map_borregasave))
for c in controllables1:
    print(c)
    
    
signal = sim.get_controllable(lgsvl.Vector(15.5, 4.7, -23.9), "signal")
print("\n# Signal of interest:")
print(signal)



print("\n# Current control policy:")
print(signal.control_policy)


control_policy = "trigger=50;green=3;yellow=2;red=1;loop"


signal.control(control_policy)

print("\n# Updated control policy:")
print(signal.control_policy)


print("\n# Current signal state before simulation:")
print(signal.current_state)




state.transform.position = spawns[0].position + 10.0 * forward
state.transform.rotation = spawns[0].rotation

#npc1 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)

#state = lgsvl.AgentState()

# 10 meters ahead, on right lane
state.transform.position = spawns[0].position + 4.0 * right + 10.0 * forward
state.transform.rotation = spawns[0].rotation

npc2 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state, lgsvl.Vector(1, 1, 0))

# If the passed bool is False, then the NPC will not moved
# The float passed is the maximum speed the NPC will drive
# 11.1 m/s is ~40 km/h
#npc1.follow_closest_lane(True, 11.1)


npc2.follow_closest_lane(True, 15)










sim.run(seconds)

print("\nVehicle running over object phase")


#state1 = lgsvl.AgentState()
#state1.transform = spawns[0]



#ego = sim.add_agent(env.str("LGSVL__VEHICLE_0", lgsvl.wise.DefaultAssets.ego_lincoln2017mkz_apollo5), lgsvl.AgentType.EGO, state1)

print("\n# Current signal state when vehicle passes:")
print(signal.current_state)

print("Vehicle bounding box =", ego.bounding_box)

print("Current time = ", sim.current_time)
print("Current frame = ", sim.current_frame)

#input("Press Enter to drive forward for 10 seconds")

#sim.run(10)

#print("Current time = ", sim.current_time)
#print("Current frame = ", sim.current_frame)
