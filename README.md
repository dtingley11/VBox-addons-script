# `VBox-addons-script`

This Python script allows you to download VirtualBox Guest Additions and Extension Packs easily. It validates user input for VirtualBox versions and provides options for downloading Guest Additions or Extension Packs.

## Prerequisites

- Python 3.x

- Required Python packages: `requests`, `tqdm` - Install them using the following command:

   ```sh
   #!/usr/bin/env sh
   pip install requests tqdm
   ```

## Usage

1. Clone the repository:

   ```sh
   #!/usr/bin/env sh
   git clone https://github.com/dtingley11/VBox-addons-script.git
   ```

4. Navigate to the project directory:

   ```sh
   #!/usr/bin/env sh
   cd VBox-addons-script
   ```

3. Run the script:

   ```sh
   #!/usr/bin/env sh
   python virtualbox-addons-downloader.py
   ```

4. Follow the on-screen prompts to download VirtualBox Add-Ons.

#### Note

If the version you choose is not a beta version, the file will be named somthing like <code>Oracle_VM_VirtualBox_Extension_Pack-x.x.x_<b>BETANone</b></code> or <code>VBoxGuestAdditions_x.x.x_<b>BETANone</b></code> Do not be alarmed, that just means the edition you downloaded was not a beta version.

## Features

- Supports downloading both Guest Additions and Extension Packs.

- Validates user input for VirtualBox versions and options.

- Displays download progress using a progress bar.

## Contributing

Feel free to contribute to this project by opening issues or creating pull requests. Your feedback and contributions are welcome!

## License

This project is licensed under the GNU General Public License V3 – see the [`LICENSE`](LICENSE) file for details.

## Thanks

We would like to express our gratitude to the VirtualBox team for providing such amazing virtualization software. Their hard work and dedication make projects like this possible.
