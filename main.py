import simulator
import GUI


if __name__ == "__main__":
	mainobj = simulator.Simulator(GUI.GUI())
	mainobj.main_loop()
