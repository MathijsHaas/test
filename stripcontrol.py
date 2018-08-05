import opc, time

numLEDs = 35
client = opc.Client('localhost:7890')


def main():
    print("stripcontrol main loop start")
    
    while True:
#        for i in range(numLEDs):
 #           client.put_pixels(pixels)
  #          time.sleep(0.01)
        pixels = [ (testmetstrip.kleur[0],testmetstrip.kleur[1],testmetstrip.kleur[2]) ] * numLEDs
        client.put_pixels(pixels)
        time.sleep(0.01)
		
		
import testmetstrip

if __name__ == "__main__":
    main()