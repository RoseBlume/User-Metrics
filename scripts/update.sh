
#!/bin/bash

app_names=(
    "jrosarybibleapp"
    "rosemusic"
)

metric_types=(
    "daily_device_change"
    "installed_base_by_channel"
    "installed_base_by_country"
    "installed_base_by_operating_system"
    "installed_base_by_version"
    "installed_base_by_architecture"
    "weekly_device_change"
    "weekly_installed_base_by_channel"
    "weekly_installed_base_by_country"
    "weekly_installed_base_by_operating_system"
    "weekly_installed_base_by_version"
    "weekly_installed_base_by_architecture"
)

init() {
    for metric_type in "${metric_types[@]}"; do
        mkdir -p "../output/csv/$metric_type"
    done
}

# init


retrieve_metrics() {
    local app_name=$1
    local metric_type=$2
    local start_date="2024-11-10"

    snapcraft metrics "$app_name" --name "$metric_type" --start "$start_date" --format=json > ../data/"$metric_type"/"$app_name".json
}

for app_name in "${app_names[@]}"; do
    for metric_type in "${metric_types[@]}"; do
        output_file="../data/${app_name}_${metric_type}.json"
        retrieve_metrics "$app_name" "$metric_type"
    done
done
