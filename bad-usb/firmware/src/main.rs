#![no_std]
#![no_main]

use embassy_executor::Spawner;
use embassy_futures::join::join;
use embassy_time::Timer;
use embassy_usb::{
    Builder, Config,
    class::hid::{HidBootProtocol, HidSubclass, HidWriter},
};
use esp_backtrace as _;
use esp_hal::{
    clock::CpuClock,
    timer::timg::TimerGroup,
    usb::otg::{Usb, embassy_usb_device},
};
use static_cell::StaticCell;
use usbd_hid::descriptor::{KeyboardReport, SerializedDescriptor};

use embassy_usb_device::Config as DriverConfig;

type UsbDriver = embassy_usb_device::Driver<'static>;

#[cfg(all(feature = "windows-demo", feature = "macos-demo"))]
compile_error!("choose exactly one target profile: windows-demo or macos-demo");
#[cfg(not(any(feature = "windows-demo", feature = "macos-demo")))]
compile_error!("choose exactly one target profile: windows-demo or macos-demo");

const VENDOR_ID: u16 = 0x303a;
const PRODUCT_ID: u16 = 0x4001;
const HID_REPORT_LEN: usize = 8;

static DEVICE_CONFIG: StaticCell<[u8; 256]> = StaticCell::new();
static BOS_CONFIG: StaticCell<[u8; 256]> = StaticCell::new();
static MSOS_CONFIG: StaticCell<[u8; 256]> = StaticCell::new();
static CONTROL_BUF: StaticCell<[u8; 64]> = StaticCell::new();
static EP_OUT_BUF: StaticCell<[u8; 256]> = StaticCell::new();
static HID_STATE: StaticCell<embassy_usb::class::hid::State<'static>> = StaticCell::new();

esp_bootloader_esp_idf::esp_app_desc!();

#[esp_hal::main]
async fn main(_spawner: Spawner) -> ! {
    let config = esp_hal::Config::default().with_cpu_clock(CpuClock::max());
    let peripherals = esp_hal::init(config);
    let timer_group = TimerGroup::new(peripherals.TIMG0);
    esp_rtos::start(timer_group.timer0);

    let usb = Usb::new_fs(peripherals.USB_FS, peripherals.GPIO20, peripherals.GPIO19);
    let driver =
        embassy_usb_device::Driver::new(usb, EP_OUT_BUF.init([0; 256]), DriverConfig::default());

    let mut usb_config = Config::new(VENDOR_ID, PRODUCT_ID);
    usb_config.manufacturer = Some("Security Training Lab");
    usb_config.product = Some("Authorized Awareness Demo");
    usb_config.serial_number = Some("BADUSB-DEMO");

    let mut builder = Builder::new(
        driver,
        usb_config,
        DEVICE_CONFIG.init([0; 256]),
        BOS_CONFIG.init([0; 256]),
        MSOS_CONFIG.init([0; 256]),
        CONTROL_BUF.init([0; 64]),
    );

    let keyboard = HidWriter::<_, HID_REPORT_LEN>::new(
        &mut builder,
        HID_STATE.init(embassy_usb::class::hid::State::new()),
        embassy_usb::class::hid::Config {
            report_descriptor: KeyboardReport::desc(),
            request_handler: None,
            poll_ms: 10,
            max_packet_size: HID_REPORT_LEN as u16,
            hid_subclass: HidSubclass::Boot,
            hid_boot_protocol: HidBootProtocol::Keyboard,
        },
    );
    let mut usb_device = builder.build();

    join(usb_device.run(), demo_task(keyboard)).await;
    loop {
        Timer::after_secs(60).await;
    }
}

async fn demo_task(mut keyboard: HidWriter<'static, UsbDriver, HID_REPORT_LEN>) {
    keyboard.ready().await;
    Timer::after_millis(1_200).await;

    #[cfg(feature = "windows-demo")]
    {
        chord(&mut keyboard, 0x08, 0x15).await; // Windows + R
        Timer::after_millis(300).await;
        type_text(&mut keyboard, "notepad").await;
        press(&mut keyboard, 0, 0x28).await; // Enter
        Timer::after_millis(900).await;
    }

    #[cfg(feature = "macos-demo")]
    {
        chord(&mut keyboard, 0x08, 0x2c).await; // Command + Space
        Timer::after_millis(300).await;
        type_text(&mut keyboard, "vi somefile").await;
        press(&mut keyboard, 0, 0x28).await; // Enter
        type_text(&mut keyboard, "i").await;
        press(&mut keyboard, 0, 0x28).await; // Enter
        Timer::after_millis(1_200).await;
    }

    type_text(&mut keyboard, "You've been hacked").await;
    press(&mut keyboard, 0, 0x28).await;
}

async fn type_text(keyboard: &mut HidWriter<'static, UsbDriver, HID_REPORT_LEN>, text: &str) {
    for character in text.chars() {
        let (modifier, key) = match character {
            'A'..='Z' => (0x02, character as u8 - b'A' + 0x04),
            'a'..='z' => (0x00, character as u8 - b'a' + 0x04),
            ' ' => (0x00, 0x2c),
            '\'' => (0x00, 0x34),
            _ => continue,
        };
        press(keyboard, modifier, key).await;
    }
}

async fn chord(
    keyboard: &mut HidWriter<'static, UsbDriver, HID_REPORT_LEN>,
    modifier: u8,
    key: u8,
) {
    let _ = keyboard.write(&[modifier, 0, key, 0, 0, 0, 0, 0]).await;
    Timer::after_millis(100).await;
    release(keyboard).await;
    Timer::after_millis(100).await;
}

async fn press(
    keyboard: &mut HidWriter<'static, UsbDriver, HID_REPORT_LEN>,
    modifier: u8,
    key: u8,
) {
    let _ = keyboard.write(&[modifier, 0, key, 0, 0, 0, 0, 0]).await;
    Timer::after_millis(80).await;
    release(keyboard).await;
    Timer::after_millis(80).await;
}

async fn release(keyboard: &mut HidWriter<'static, UsbDriver, HID_REPORT_LEN>) {
    let _ = keyboard.write(&[0; HID_REPORT_LEN]).await;
}
