import multiprocessing
import opc

numLEDs = 35
client = opc.Client('localhost:7890')
pixels = multiprocessing.Array('i', numLEDs)


def main():
    while True:
        for idx, n in enumerate(pixels):
            pixels[idx] = (200,200,0)
        client.put_pixels(pixels)
        
        
if __name__ == "__main__":
    main()