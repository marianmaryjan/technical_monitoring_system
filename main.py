from data_source import simulator

def main():
    data = simulator.generate_data(5)
    print("Generated Data:", data)

if __name__ == "__main__":
    main()