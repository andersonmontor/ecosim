import simulator
import GUI


if __name__ == "__main__":
	guiobj = GUI.GUI()
	mainobj = simulator.Simulator(guiobj)
	mainobj.main_loop()
