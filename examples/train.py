import time
import torch

def main():
    print("Starting dummy training...")
    # Simulate some CPU load
    x = torch.randn(1000, 1000)
    for i in range(5):
        _ = torch.matmul(x, x)
        time.sleep(1) # Simulate IO/Idle
        print(f"Step {i+1} done")

if __name__ == "__main__":
    main()
