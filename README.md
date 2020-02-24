[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

Disk space sensor for Home Assistant.

Example configuration.yaml

```yaml
sensor:
  - platform: diskspace
    name: Main Disk
    path: "/"
    unit_of_measure: "GB"
```

**Unit of Measure:**
* GB - Gigabytes 
* MB - Megabytes
* TB - Terabyes
* Anything else - Raw data which is given in bytes.

*This uses 1000MB = 1GB*

**Name:** Anything you like. The sensor will then be sensor.disk_space_*name*

**Path:** Where the mount path is. This can be found from the command line using the command *mount* for instance.

## Notes

This is an example of what a sensor looks like.

Sensor|State|Attributes
------|-----|----------
sensor.disk_space_main_disk | 368 | total: 490 used: 97 free: 368 


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
