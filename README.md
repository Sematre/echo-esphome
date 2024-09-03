# Echo ESPHome
> [!NOTE] 
> :construction: This project is WIP. :construction:

Home Assistant compatible voice assistant, with on-device voice activation, mainboard drop-in replacement for Amazon Echo Dot (2nd Gen).

## Echo Dot (2nd Gen) Hardware
### Top board
- 4x ADC with miniDSP: [TLV320ADC3101](https://www.ti.com/product/de-de/TLV320ADC3101) ([Datasheet](https://www.ti.com/lit/ds/symlink/tlv320adc3101.pdf))
    - Each chip is connected to 2 stereo microphones
- 7x Microphone (6 ring + 1 center)
- 1x 36-Channel LED driver: [IS31FL3236A](https://www.lumissil.com/applications/industrial/appliance/major-appliances/range-hood/is31fl3236a) ([Datasheet](https://www.lumissil.com/assets/pdf/core/IS31FL3236A_DS.pdf))
- 12x RGBW LED
- 4x Tacktile dom switch
    - 1x Red LED on mute button
    - 1x Light sensor on action button
- 1x Tri-state buffer: [74LVC1G125](https://www.diodes.com/assets/Datasheets/74LVC1G125.pdf)

### Mainboard
- 1x Class-D stereo speaker amplifier: [TPA3118D2](https://www.ti.com/product/TPA3118D2) ([Datasheet](https://www.ti.com/lit/ds/symlink/tpa3118d2.pdf))

## Getting started
```sh
$ git clone --recurse-submodules https://github.com/Sematre/echo-esphome.git
```

## Resources
- [Retasking a 2nd Gen Echo](https://community.home-assistant.io/t/retasking-a-2nd-gen-echo/709084) *by Terry Sanders*
- [Inside the Amazon Echo Dot (3rd Gen): A Complete Teardown](https://pallavaggarwal.in/2023/01/10/teardown-amazon-echo-dot-3rd-gen/) *by Pallav Aggarwal*
