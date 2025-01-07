import json
import matplotlib.pyplot as plt


metric_types=[
    "daily_device_change",
    "installed_base_by_channel",
    "installed_base_by_country",
    "installed_base_by_operating_system",
    "installed_base_by_version",
    "installed_base_by_architecture",
    "weekly_device_change",
    "weekly_installed_base_by_channel",
    "weekly_installed_base_by_country",
    "weekly_installed_base_by_operating_system",
    "weekly_installed_base_by_version",
    "weekly_installed_base_by_architecture"
]
def gather_lists(json_data):
    buckets = json_data['buckets']
    series = json_data['series']
    
    amd64_values = next((s['values'] for s in series if s['name'] == 'amd64'), [])
    arm64_values = next((s['values'] for s in series if s['name'] == 'arm64'), [])
    armhf_values = next((s['values'] for s in series if s['name'] == 'armhf'), [])
    
    return buckets, amd64_values, arm64_values, armhf_values

def add_lists(list1, list2, list3):
    combined_list = []
    max_len = max(len(list1), len(list2), len(list3))
    for i in range(max_len):
        val1 = list1[i] if i < len(list1) and list1[i] is not None else 0
        val2 = list2[i] if i < len(list2) and list2[i] is not None else 0
        val3 = list3[i] if i < len(list3) and list3[i] is not None else 0
        combined_list.append(val1 + val2 + val3)
    return combined_list
# Example usage
def initialize(metric_type):
    filename = f'../data/{metric_type}/rosemusic.json'
    with open(filename, 'r') as f:
        rosemusic_data = json.load(f)
    filename = f'../data/{metric_type}/jrosarybibleapp.json'
    with open(filename, 'r') as f:
        rosarybibleapp_data = json.load(f)
    return rosemusic_data, rosarybibleapp_data


def plot_data(dates1, data1, dates2, data2, title, x_label, y_label, rotation=75):
    plt.plot(dates1, data1, marker="o", label='Rose Music', color='blue')
    plt.plot(dates2, data2, marker="o", label='Rosary Bible App', color='red')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=rotation)
    plt.legend()
    plt.show()

def export_plot(dates1, data1, dates2, data2, title, x_label, y_label, filename, rotation=75):
    height = (max(max(data1), max(data2)) / 3)
    plt.figure(figsize=((len(dates1) * 0.5), height))
    plt.plot(dates1, data1, marker="o", label='Rose Music', color='blue')
    plt.plot(dates2, data2, marker="o", label='Rosary Bible App', color='red')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=rotation)
    plt.legend()
    plt.savefig(filename)

def export_csv(dates, data1, data2, filename):
    with open(filename, 'w') as f:
        f.write('Date, Rosary Music, Rosary Bible App\n')
        for date, d1, d2 in zip(dates, data1, data2):
            f.write(f'{date}, {d1}, {d2}\n')


def runner():
    for i in range(len(metric_types)):
        rosemusic_data, rosarybibleapp_data = initialize(metric_types[i])
        rosemusic_dates, rosemusic_amd64, rosemusic_arm64, rosemusic_armhf = gather_lists(rosemusic_data)
        rosarybibleapp_dates, rosarybibleapp_amd64, rosarybibleapp_arm64, rosarybibleapp_armhf = gather_lists(rosarybibleapp_data)
        rosemusic_data = add_lists(rosemusic_amd64, rosemusic_arm64, rosemusic_armhf)
        rosarybibleapp_data = add_lists(rosarybibleapp_amd64, rosarybibleapp_arm64, rosarybibleapp_armhf)
        export_csv_file = f'../output/csv/{metric_types[i]}/{metric_types[i]}.csv'
        export_csv(rosemusic_dates, rosemusic_data, rosarybibleapp_data, export_csv_file)