import subprocess
import re
import matplotlib.pyplot as plt
import argparse

def get_commits_by_author(repo_path):
    """Get the number of commits by each author."""
    cmd = ["git", "-C", repo_path, "shortlog", "-s", "-n"]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    output = result.stdout

    commits_data = []
    for line in output.strip().split("\n"):
        match = re.match(r"\s*(\d+)\s+(.+)", line)
        if match:
            commits_data.append((match.group(2), int(match.group(1))))

    return commits_data

def get_lines_of_code_by_author(repo_path):
    """Get the number of lines of code owned by each author."""
    cmd = ["git", "-C", repo_path, "ls-files"]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    files = result.stdout.strip().split("\n")

    authors = {}
    for file in files:
        blame_cmd = ["git", "-C", repo_path, "blame", "--line-porcelain", file]
        blame_result = subprocess.run(blame_cmd, stdout=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
        blame_output = blame_result.stdout

        for line in blame_output.split("\n"):
            if line.startswith("author "):
                author = line[len("author "):].strip()
                authors[author] = authors.get(author, 0) + 1

    return sorted(authors.items(), key=lambda x: x[1], reverse=True)

def plot_bar_chart(data, title, x_label, y_label, color):
    """Plot a bar chart for the given data."""
    authors, values = zip(*data)
    plt.figure(figsize=(10, 5))
    plt.bar(authors, values, color=color, alpha=0.7)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Analyze a Git repository.")
    parser.add_argument("repo_path", type=str, help="Path to the Git repository")
    args = parser.parse_args()

    repo_path = args.repo_path

    print("Extracting commit data...")
    commits_data = get_commits_by_author(repo_path)
    print("Commits by author:", commits_data)

    print("Extracting lines of code ownership data...")
    loc_data = get_lines_of_code_by_author(repo_path)
    print("Lines of code owned by author:", loc_data)

    print("Generating bar charts...")
    plot_bar_chart(commits_data, "Commits per Author", "Authors", "Number of Commits", "blue")
    plot_bar_chart(loc_data, "Lines of Code Owned per Author", "Authors", "Lines of Code", "green")

if __name__ == "__main__":
    main()
