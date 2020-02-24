[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

Disk space sensor for Home Assistant.

```yaml
sensor:
  - platform: diskspace
    name: Main Disk
    path: "/"
    unit_of_measure: "GB"
```

## Notes

Sensor|State|Attributes
-----------------------
sensor.disk_space_main_disk|368|total: 490 used: 97 free: 368 percentage_free: 75 unit_of_measurement: GB friendly_name: disk space Main Disk icon: mdi:harddisk


Notice that Total - Used doesn't equal Free. This is a limitation of the operating system and happens on both MacOS and Linux.

## Notification Template
```yaml
- id: "2121054773"
  alias: Low Disk Space
  description: "Notify me of low disk space"
  trigger:
    - platform: template
      value_template: "{% if state_attr('sensor.disk_space_main_disk', 'percentage_free') < 10 %}true{% endif %}"
  condition: []
  action:
    - data:
        message: Main disk is almost full
      service: notify.slack
```

Be careful with the indentation if copy and pasting this example.