# Echo ESPHome
> [!NOTE] 
> :construction: This project is WIP. :construction:

Home Assistant compatible voice assistant, with on-device voice activation, drop-in replacement for Amazon Echo Dot (2nd Gen).

## Echo Dot (2nd Gen) Hardware
### Top board
- 4x ADC: [TLV320ADC3101](https://www.ti.com/product/de-de/TLV320ADC3101) ([Datasheet](https://www.ti.com/lit/ds/symlink/tlv320adc3101.pdf))
    - Each chip is connected to 2 stereo microphones
- 6x Ring microphones + 1x Center microphone
- 1x LED driver: [LP5523](https://www.ti.com/product/LP5523) ([Datasheet](https://www.ti.com/lit/ds/symlink/lp5523.pdf))
- 12x RGBW LED
- 4x Tacktile dom switches
    - 1x Red LED on Mute button
    - 1x Light sensor on Action button
- 1x Tri-state buffer: [74LVC1G125](https://www.diodes.com/assets/Datasheets/74LVC1G125.pdf)

### Mainboard
- 1x Speaker amplifier: [TPA3118D2](https://www.ti.com/product/TPA3118D2) ([Datasheet](https://www.ti.com/lit/ds/symlink/tpa3118d2.pdf))

## Resources
- [Retasking a 2nd Gen Echo](https://community.home-assistant.io/t/retasking-a-2nd-gen-echo/709084) *by Terry Sanders*
- [Inside the Amazon Echo Dot (3rd Gen): A Complete Teardown](https://pallavaggarwal.in/2023/01/10/teardown-amazon-echo-dot-3rd-gen/) *by Pallav Aggarwal*
