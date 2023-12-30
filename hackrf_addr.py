import hackrf

def main():
    # Retrieve a list of HackRF devices attatched to the system
    device_list = hackrf.hackrf_device_list()

    # Print the device addresses for each device in the list
    for i in range(device_list.contents.count):
        device = device_list.contents.devices[i]
        print("Device {}: {}".format(i, device.serial_number))

if __name__ == '__main__':
    main()