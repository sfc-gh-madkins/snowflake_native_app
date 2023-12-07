import sys

def main():
    if len(sys.argv) > 1:
        release_tag = sys.argv[1]
        print(f"Received release tag: {release_tag}")
        # Your code here using the release tag


if __name__ == "__main__":
    main()
