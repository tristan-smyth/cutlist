import matplotlib.pyplot as plt


class Bin:
    def __init__(self, maxNum):
        self.data = []
        self.maxNum = maxNum

    def add(self, num):
        self.data.append(num)

    def canFit(self, num):
        if sum(self.data) + num <= self.maxNum:
            return True
        else:
            return False

    def waste(self):
        return self.maxNum - sum(self.data)


def read_data_string(string: str) -> dict:
    dataDict = {}

    # Read Data from file
    data = string.split("\n")

    # Format data
    MaterialLengths = [(int(item.split("x")[0]), float(item.split("x")[1])) for item in data[2:]]

    # Unpack Materal Lengths
    endList = []
    for item in MaterialLengths:
        for i in range(item[0]):
            endList.append(item[1])

    endList.sort()

    # Format Material Length and Material Price and add them to dictionary
    dataDict["MaterialLength"] = int(data[0].split("=")[1].replace(" ", ""))
    dataDict["MaterialPrice"] = float(data[1].split("=")[1].replace(" ", ""))
    dataDict["MaterialLengths"] = endList

    return dataDict


def first_fit(dataDict):
    maxSize = dataDict["MaterialLength"]
    data = dataDict["MaterialLengths"]

    binList = [Bin(maxSize)]

    for item in data:
        assigned = False
        for bin in binList:
            if bin.canFit(item):
                bin.add(item)
                assigned = True
                break
        if not assigned:
            new_bin = Bin(maxSize)
            new_bin.add(item)
            binList.append(new_bin)

    return binList


def format_decimal(value):
    # Format the value to display decimal places only if they are not zero and up to a maximum of 3
    formatted_value = '{:.3f}'.format(value).rstrip('0').rstrip('.')
    return formatted_value if formatted_value else '0'


def plot_data_bars(data, price):
    years = list(range(1, len(data) + 1))  # [1, 2, 3, ...]
    bar_height = 1.0  # Set the desired height for all bars

    fig, ax = plt.subplots(figsize=(10, 6))

    wastage = sum(d[-1] for d in data)  # Calculate wastage

    for idx, lengths in enumerate(data):
        bottom = idx * bar_height  # Calculate the bottom position for each bar
        left = 0
        for i, length in enumerate(lengths[:-1]):
            if length != 0:  # Check if the length is non-zero
                ax.barh(idx + 1, length, height=bar_height, left=left, color='beige', edgecolor='black')
                ax.text(left + length / 2, idx + 1, f'{format_decimal(length)}', ha='center', va='center',
                        color='black',
                        fontsize=8, fontweight='bold')
            left += length  # Update the left position for the next segment within the same bar

        # Add the last segment with color specified if non-zero
        if lengths[-1] != 0:
            ax.barh(idx + 1, lengths[-1], height=bar_height, left=left, color='red', edgecolor='black')
            ax.text(left + lengths[-1] / 2, idx + 1, f'{format_decimal(lengths[-1])}', ha='center', va='center',
                    color='black',
                    fontsize=8, fontweight='bold')

    ax.set_xlabel("Length (m)")
    ax.set_ylabel("Length Number")
    ax.set_yticks(range(1, len(data) + 1))  # Set y-ticks as sequential numbers starting from 1
    ax.set_yticklabels(range(1, len(data) + 1))  # Set y-tick labels as sequential numbers starting from 1
    ax.set_xlim(0, max(map(sum, data)))  # Set x-axis limit based on maximum total length

    plt.title(f"Price = £{float(price) * len(data)} | Wastage = {format_decimal(wastage)}m")

    return fig
