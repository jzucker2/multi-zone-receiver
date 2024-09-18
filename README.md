# Multi Zone Receiver

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

**TO BE REMOVED: If you need help, as a developer, to use this custom component tempalte,
please look at the [User Guide in the Cookiecutter documentation](https://cookiecutter-homeassistant-custom-component.readthedocs.io/en/stable/quickstart.html)**

**This component will set up the following platforms.**

| Platform        | Description                             |
| --------------- | --------------------------------------- |
| `binary_sensor` | Show something `True` or `False`.       |
| `sensor`        | Show info from Multi Zone Receiver API. |

![example][exampleimg]

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `multi_zone_receiver`.
4. Download _all_ the files from the `custom_components/multi_zone_receiver/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Multi Zone Receiver"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/multi_zone_receiver/translations/en.json
custom_components/multi_zone_receiver/translations/fr.json
custom_components/multi_zone_receiver/translations/nb.json
custom_components/multi_zone_receiver/translations/sensor.en.json
custom_components/multi_zone_receiver/translations/sensor.fr.json
custom_components/multi_zone_receiver/translations/sensor.nb.json
custom_components/multi_zone_receiver/translations/sensor.nb.json
custom_components/multi_zone_receiver/__init__.py
custom_components/multi_zone_receiver/api.py
custom_components/multi_zone_receiver/binary_sensor.py
custom_components/multi_zone_receiver/config_flow.py
custom_components/multi_zone_receiver/const.py
custom_components/multi_zone_receiver/manifest.json
custom_components/multi_zone_receiver/sensor.py
custom_components/multi_zone_receiver/switch.py
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[buymecoffee]: https://www.buymeacoffee.com/jzucker2
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/jzucker2/multi-zone-receiver.svg?style=for-the-badge
[commits]: https://github.com/jzucker2/multi-zone-receiver/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/jzucker2/multi-zone-receiver.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40jzucker2-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/jzucker2/multi-zone-receiver.svg?style=for-the-badge
[releases]: https://github.com/jzucker2/multi-zone-receiver/releases
[user_profile]: https://github.com/jzucker2

## Notes

- Custom integration requirements
  - https://developers.home-assistant.io/docs/creating_integration_manifest/#requirements
  - https://github.com/home-assistant/core/blob/dev/requirements.txt
- denon avr component
  - https://github.com/home-assistant/core/tree/dev/homeassistant/components/denonavr
- https://developers.home-assistant.io/blog/2024/04/30/store-runtime-data-inside-config-entry/
- https://developers.home-assistant.io/blog/2024/08/05/coordinator_async_setup/
- https://developers.home-assistant.io/blog/2024/05/01/improved-hass-data-typing
- https://github.com/home-assistant/core/blob/dev/homeassistant/components/ecowitt/entity.py
- https://developers.home-assistant.io/docs/asyncio_thread_safety/
  - This covers adding and removing and callbacks
- https://developers.home-assistant.io/docs/development_validation
- https://developers.home-assistant.io/docs/core/platform/significant_change/
  - I want to use this to stabilize volume changes and keep them response on the client end
- https://github.com/home-assistant/core/blob/931c8f9e66193348fdcf92f93e7803d79b077f2f/homeassistant/components/group/config_flow.py#L22
  - For selecting entities

## Debug Notes

```
home-assistant  | 2024-09-12 13:55:15.081 DEBUG (MainThread) [custom_components.multi_zone_receiver] New state from 'media_player.denon_avr_x4300h_main_zone_living_room': '<state media_player.denon_avr_x4300h_main_zone_living_room=on; source_list=['APPLE TV', 'AUX1', 'Bluetooth', 'JohnCast', 'Media Player', 'NUC', 'Online Music', 'PS4', 'Phono', 'TV Audio', 'Tuner', 'VINYL', 'WII U'], sound_mode_list=['MUSIC', 'MOVIE', 'GAME', 'AUTO', 'STANDARD', 'VIRTUAL', 'MATRIX', 'ROCK ARENA', 'JAZZ CLUB', 'VIDEO GAME', 'MONO MOVIE', 'DIRECT', 'PURE DIRECT', 'DOLBY DIGITAL', 'DTS SURROUND', 'AURO3D', 'AURO2DSURR', 'MCH STEREO', 'STEREO', 'ALL ZONE STEREO'], volume_level=0.45, is_volume_muted=False, media_content_type=channel, media_title=VINYL, source=VINYL, sound_mode=STEREO, sound_mode_raw=STEREO, dynamic_eq=True, device_class=receiver, friendly_name=Denon AVR-X4300H Main Zone Living Room, supported_features=69004 @ 2024-09-12T13:55:15.078347-07:00>'
home-assistant  | 2024-09-12 13:55:20.175 DEBUG (MainThread) [custom_components.multi_zone_receiver] New state from 'media_player.denon_avr_x4300h_zone_3_kitchen': '<state media_player.denon_avr_x4300h_zone_3_kitchen=on; source_list=['APPLE TV', 'AUX1', 'Bluetooth', 'JohnCast', 'Media Player', 'NUC', 'Online Music', 'PS4', 'Phono', 'SOURCE', 'TV Audio', 'Tuner', 'VINYL', 'WII U'], sound_mode_list=['MUSIC', 'MOVIE', 'GAME', 'AUTO', 'STANDARD', 'VIRTUAL', 'MATRIX', 'ROCK ARENA', 'JAZZ CLUB', 'VIDEO GAME', 'MONO MOVIE', 'DIRECT', 'PURE DIRECT', 'DOLBY DIGITAL', 'DTS SURROUND', 'AURO3D', 'AURO2DSURR', 'MCH STEREO', 'STEREO', 'ALL ZONE STEREO'], volume_level=0.47, is_volume_muted=False, media_content_type=channel, media_title=CD, source=CD, device_class=receiver, friendly_name=Denon AVR-X4300H Zone 3 Kitchen, supported_features=69004 @ 2024-09-12T13:55:20.174114-07:00>'
home-assistant  | 2024-09-12 13:55:20.807 DEBUG (MainThread) [custom_components.multi_zone_receiver] New state from 'media_player.denon_avr_x4300h_zone_2_dining_room': '<state media_player.denon_avr_x4300h_zone_2_dining_room=off; source_list=['APPLE TV', 'AUX1', 'Bluetooth', 'JohnCast', 'Media Player', 'NUC', 'Online Music', 'PS4', 'Phono', 'SOURCE', 'TV Audio', 'Tuner', 'VINYL', 'WII U'], sound_mode_list=['MUSIC', 'MOVIE', 'GAME', 'AUTO', 'STANDARD', 'VIRTUAL', 'MATRIX', 'ROCK ARENA', 'JAZZ CLUB', 'VIDEO GAME', 'MONO MOVIE', 'DIRECT', 'PURE DIRECT', 'DOLBY DIGITAL', 'DTS SURROUND', 'AURO3D', 'AURO2DSURR', 'MCH STEREO', 'STEREO', 'ALL ZONE STEREO'], device_class=receiver, friendly_name=Denon AVR-X4300H Zone 2 Dining Room, supported_features=69004 @ 2024-09-12T13:55:11.342777-07:00>'
home-assistant  | 2024-09-12 13:55:22.345 DEBUG (MainThread) [custom_components.multi_zone_receiver] New state from 'media_player.denon_avr_x4300h_zone_2_dining_room': '<state media_player.denon_avr_x4300h_zone_2_dining_room=on; source_list=['APPLE TV', 'AUX1', 'Bluetooth', 'JohnCast', 'Media Player', 'NUC', 'Online Music', 'PS4', 'Phono', 'SOURCE', 'TV Audio', 'Tuner', 'VINYL', 'WII U'], sound_mode_list=['MUSIC', 'MOVIE', 'GAME', 'AUTO', 'STANDARD', 'VIRTUAL', 'MATRIX', 'ROCK ARENA', 'JAZZ CLUB', 'VIDEO GAME', 'MONO MOVIE', 'DIRECT', 'PURE DIRECT', 'DOLBY DIGITAL', 'DTS SURROUND', 'AURO3D', 'AURO2DSURR', 'MCH STEREO', 'STEREO', 'ALL ZONE STEREO'], volume_level=0.52, is_volume_muted=False, media_content_type=channel, media_title=CD, source=CD, device_class=receiver, friendly_name=Denon AVR-X4300H Zone 2 Dining Room, supported_features=69004 @ 2024-09-12T13:55:22.344393-07:00>'
```
