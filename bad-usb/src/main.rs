use std::{
    io::{BufRead, BufReader},
    process::Command,
    thread,
    time::Duration,
};

use anyhow::{Context, Result, bail};

const ESPRESSIF_VID: u16 = 0x303a;
const USB_SERIAL_JTAG_PID: u16 = 0x1001;
const TRIGGER: &str = "BAD_USB_DEMO";
const MESSAGE: &str = "You've been hacked";

fn main() -> Result<()> {
    let demo_mode = std::env::args().skip(1).any(|arg| arg == "--demo");

    if demo_mode {
        open_editor_and_type(MESSAGE)?;
        return Ok(());
    }

    println!("bad-usb awareness demo: waiting for an ESP32-S3 USB serial device");
    println!("The device must send the line {TRIGGER:?}; press Ctrl-C to stop.");

    loop {
        if let Some(port) = find_board_port() {
            println!("Found ESP32-S3 on {}", port.port_name);
            match watch_port(&port.port_name) {
                Ok(()) => println!("Device disconnected; waiting again."),
                Err(error) => eprintln!("Serial connection ended: {error:#}"),
            }
        }
        thread::sleep(Duration::from_millis(750));
    }
}

fn find_board_port() -> Option<serialport::SerialPortInfo> {
    serialport::available_ports()
        .ok()?
        .into_iter()
        .find(|port| {
            matches!(
                &port.port_type,
                serialport::SerialPortType::UsbPort(usb)
                    if usb.vid == ESPRESSIF_VID && usb.pid == USB_SERIAL_JTAG_PID
            )
        })
}

fn watch_port(port_name: &str) -> Result<()> {
    let port = serialport::new(port_name, 115_200)
        .timeout(Duration::from_millis(250))
        .open()
        .with_context(|| format!("opening serial port {port_name}"))?;
    let mut reader = BufReader::new(port);
    let mut line = String::new();

    loop {
        line.clear();
        match reader.read_line(&mut line) {
            Ok(0) => bail!("serial device disconnected"),
            Ok(_) if line.trim() == TRIGGER => {
                open_editor_and_type(MESSAGE)?;
                println!("Demo message sent. Waiting for the device to disconnect.");
            }
            Ok(_) => {}
            Err(error)
                if matches!(
                    error.kind(),
                    std::io::ErrorKind::TimedOut | std::io::ErrorKind::WouldBlock
                ) => {}
            Err(error) => return Err(error).context("reading serial trigger"),
        }
    }
}

#[cfg(target_os = "macos")]
fn open_editor_and_type(message: &str) -> Result<()> {
    let script = format!(
        "tell application \"TextEdit\" to activate\ndelay 0.7\ntell application \"System Events\" to keystroke \"{}\"",
        message.replace('\\', "\\\\").replace('"', "\\\"")
    );
    run_command("osascript", &["-e", &script])
        .context("opening TextEdit and typing the demo message")
}

#[cfg(target_os = "windows")]
fn open_editor_and_type(message: &str) -> Result<()> {
    let escaped = message.replace('\'', "''");
    let script = format!(
        "Start-Process notepad; Start-Sleep -Milliseconds 900; Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{escaped}')"
    );
    run_command("powershell", &["-NoProfile", "-Command", &script])
        .context("opening Notepad and typing the demo message")
}

#[cfg(not(any(target_os = "macos", target_os = "windows")))]
fn open_editor_and_type(_message: &str) -> Result<()> {
    bail!("the editor demo currently supports macOS and Windows")
}

fn run_command(program: &str, args: &[&str]) -> Result<()> {
    let status = Command::new(program)
        .args(args)
        .status()
        .with_context(|| format!("starting {program}"))?;
    if !status.success() {
        bail!("{program} exited with {status}");
    }
    Ok(())
}
