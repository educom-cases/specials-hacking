# bad-usb

An authorized USB HID security-awareness demo for the ESP32-S3-DevKitC-1. The firmware enumerates as a standard keyboard, opens Notepad or TextEdit, and types `You've been hacked`. It does not require a host-side listener.

## Board connection

Use the board's native USB OTG connector, wired to GPIO20 (D+) and GPIO19 (D−), to run the HID demonstration. The separate USB-to-UART connector does not expose the HID device. The board has no reliable way to identify the connected computer's operating system, so build the profile for the target machine.

To flash over the native USB connector, put the ESP32-S3 into download mode first: hold **BOOT**, tap **RESET**, then release **BOOT**. Confirm that a new serial port appears (`espflash list-ports` on macOS), then run the flash command. When the firmware starts, it enumerates as a keyboard and the serial port disappears; this is expected. Alternatively, flash through the USB-to-UART connector and select its serial port with `--port`.

## Build and flash

Install the Espressif Rust toolchain and flashing utility, then load the toolchain environment and connect the board's native USB OTG port:

```sh
espup install --targets esp32s3
source ~/export-esp.sh
cargo install espflash
cd firmware
cargo +esp run --release --no-default-features --features windows-demo
```

For macOS, replace `windows-demo` with `macos-demo`. The firmware's `.cargo/config.toml` runner flashes the firmware and opens a serial monitor.

The HID action starts after USB enumeration. Windows uses Win+R and launches Notepad; macOS uses Command+Space and launches TextEdit. Both then type the demo sentence. Test only on a machine or VM you control. The board can type into whichever computer it is connected to, so unplug it after the demonstration.

## Host-side simulator

The root Rust binary remains available for a software-only demonstration on the host:

```sh
cargo run -- --demo
```

It opens the platform editor and types the same message without using the ESP32.
