from snapcraft import gather_lists, add_lists, initialize, export_plot, export_csv
import json
import matplotlib.pyplot as plt

os_names = [

]
arch_types = [
    'installed_base_by_architecture',
    'weekly_installed_base_by_architecture'
]

change_types = [
    'daily_device_change',
    'weekly_device_change'
]

alt_types = [
    'installed_base_by_channel',
    'installed_base_by_operating_system',
    'weekly_installed_base_by_channel',
    'weekly_installed_base_by_operating_system',
]
alt_names = [
    "Installed Base by Channel",
    "Installed Base by Operating System",
    "Weekly Installed Base by Channel",
    "Weekly Installed Base by Operating System"
]
change_names = [
    'Daily Device Change',
    'Weekly Device Change'
]
app_names = [
    'rosemusic',
    'jrosarybibleapp'
]
def alt_export_csv(dates, values, names, filename):
    with open(filename, 'w') as f:
        f.write('Date')
        for name in names:
            f.write(f',{name}')
        f.write('\n')
        for i in range(len(dates)):
            f.write(f'{dates[i]}')
            for j in range(len(values)):
                f.write(f',{values[j][i]}')
            f.write('\n')
def initialize_device_change(change_type):
    filename = f'../data/{change_type}/rosemusic.json'
    with open(filename) as f:
        rosemusic_data = json.load(f)
    filename = f'../data/{change_type}/jrosarybibleapp.json'
    with open(filename) as f:
        rosarybibleapp_data = json.load(f)
    return rosemusic_data, rosarybibleapp_data



def device_change():
    for change_type in change_types:
        filename = f'../data/{change_type}/rosemusic.json'
        with open(filename) as f:
            rosemusic_data = json.load(f)
        filename = f'../data/{change_type}/jrosarybibleapp.json'
        with open(filename) as f:
            rosarybibleapp_data = json.load(f)
        rosemusic_series = next(item for item in rosemusic_data['series'] if item['name'] == change_type)
        rosarybibleapp_series = next(item for item in rosarybibleapp_data['series'] if item['name'] == change_type)

        plt.figure(figsize=(10, 5))
        plt.plot(rosemusic_data['buckets'], rosemusic_series['values'], label='RoseMusic')
        plt.plot(rosarybibleapp_data['buckets'], rosarybibleapp_series['values'], label='RosaryBibleApp')

        plt.xlabel('Date')
        plt.ylabel('Devices')
        plt.title(f'Device Change - {change_type}')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig(f'../output/plots/{change_type}.png')
        plt.close()

def gather_device_lists(json_data):
    buckets = json_data['buckets']
    series = json_data['series']
    
    continued_values = next((s['values'] for s in series if s['name'] == 'continued'), [])
    lost_values = next((s['values'] for s in series if s['name'] == 'lost'), [])
    new_values = next((s['values'] for s in series if s['name'] == 'new'), [])
    return buckets, continued_values, lost_values, new_values

def add_device_lists(continued, lost, new):
    combined_list = []
    max_len = max(len(continued), len(lost), len(new))
    for i in range(max_len):
        val1 = continued[i] if i < len(continued) and continued[i] is not None else 0
        val2 = lost[i] if i < len(lost) and lost[i] is not None else 0
        val3 = new[i] if i < len(new) and new[i] is not None else 0
        combined_list.append((val1 - val2) + val3)
    return combined_list

def alt_gather(json_data):
    buckets = json_data['buckets']
    series = json_data['series']
    values = []
    names = []
    for item in series:
        if item['values'] is None:
            values.append(0)
        else:
            values.append(item['values'])
        names.append(item['name'])
    return buckets, values, names
def single_init(alt_type, name):
    filename = f'../data/{alt_type}/{name}.json'
    with open(filename) as f:
        data = json.load(f)
    return data
        
def alt_plotter(names, values, dates, title, x_label, y_label, filename, rotation=75):
    height = ((len(dates) * 0.5)) * 0.75
    plt.figure(figsize=((len(dates) * 0.5), height))
    colors = [
        'blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white',
        'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'lime', 'navy'
    ]
    for i in range(len(names)):
        plt.plot(dates, values[i], label=names[i], color=colors[i])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=rotation)
    plt.legend()
    plt.savefig(filename)
    '''
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

    
'''
def alt_plots():
    for i in range(len(alt_types)):
        for a in range(len(app_names)):
            data = single_init(alt_types[i], app_names[a])
            dates, values, names = alt_gather(data)
            export_plot_file = f'../output/plots/{alt_types[i]}/{app_names[a]}.png'
            alt_plotter(names, values, dates, alt_names[i] + " - " + app_names[a], 'Date', 'Devices', export_plot_file)
            export_csv_file = f'../output/csv/{alt_types[i]}/{app_names[a]}.csv'
            alt_export_csv(dates, values, names, export_csv_file)
       # export_plot_file = f'../output/plots/{alt_types[i]}/{alt_types[i]}.png'
        #export_plot(rosemusic_dates, rosemusic_data, rosarybibleapp_dates, rosarybibleapp_data, alt_types[i], 'Date', 'Devices', export_plot_file)

def arch_plots():
    for i in range(len(arch_types)):
        rosemusic_data, rosarybibleapp_data = initialize(arch_types[i])
        rosemusic_dates, rosemusic_amd64, rosemusic_arm64, rosemusic_armhf = gather_lists(rosemusic_data)
        rosarybibleapp_dates, rosarybibleapp_amd64, rosarybibleapp_arm64, rosarybibleapp_armhf = gather_lists(rosarybibleapp_data)
        rosemusic_data = add_lists(rosemusic_amd64, rosemusic_arm64, rosemusic_armhf)
        rosarybibleapp_data = add_lists(rosarybibleapp_amd64, rosarybibleapp_arm64, rosarybibleapp_armhf)
        export_plot_file = f'../output/plots/{arch_types[i]}/{arch_types[i]}.png'
        export_plot(rosemusic_dates, rosemusic_data, rosarybibleapp_dates, rosarybibleapp_data, arch_types[i], 'Date', 'Devices', export_plot_file)
        export_csv(rosemusic_dates, rosemusic_data, rosarybibleapp_data, f'../output/csv/{arch_types[i]}/{arch_types[i]}.csv')

def device_change_runner():
    for i in range(len(change_types)):
        rosemusic_data, rosarybibleapp_data = initialize_device_change(change_types[i])
        rosemusic_dates, rosemusic_continued, rosemusic_lost, rosemusic_new = gather_device_lists(rosemusic_data)
        rosarybibleapp_dates, rosarybibleapp_amd64, rosarybibleapp_arm64, rosarybibleapp_armhf = gather_device_lists(rosarybibleapp_data)
        rosemusic_data = add_device_lists(rosemusic_continued, rosemusic_lost, rosemusic_new)
        rosarybibleapp_data = add_device_lists(rosarybibleapp_amd64, rosarybibleapp_arm64, rosarybibleapp_armhf)
        export_plot_file = f'../output/plots/{change_types[i]}/{change_types[i]}.png'
        export_plot(rosemusic_dates, rosemusic_data, rosarybibleapp_dates, rosarybibleapp_data, change_names[i], 'Date', 'Devices', export_plot_file)
        export_csv(rosemusic_dates, rosemusic_data, rosarybibleapp_data, f'../output/csv/{change_types[i]}/{change_types[i]}.csv')
def runner():
    alt_plots()
    device_change_runner()
    arch_plots()
