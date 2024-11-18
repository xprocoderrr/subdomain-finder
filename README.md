![Screenshot](https://github.com/tuwiliyt/subdomain-finder/blob/main/Screenshot%20from%202024-11-18%2011-40-22.png?raw=true)



# Subdomain Finder and Crawler

Tuwili Subdomain Finder is a Python-based tool for discovering subdomains of a given domain using various search engines. The tool supports crawling through **Google**, **Yandex**, **Bing**, and **DuckDuckGo** to find potential subdomains, resolving them through DNS, and gathering detailed information such as CMS and IP Address information.

## Features

- **Search Engines**: Crawls subdomains using **Google**, **Yandex**, **Bing**, and **DuckDuckGo**.
- **DNS Resolution**: Validates subdomains and provides corresponding IP addresses.
- **CMS Detection**: Identifies the CMS used by the subdomains (if available).
- **IP Information**: Provides additional IP details such as ASN, network, and country using the IPWhois library.

## Requirements

Before running the script, make sure you have the following Python libraries installed:

```bash
pip install pyfiglet colorama requests beautifulsoup4 dnspython builtwith ipwhois
```

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/username/subdomain-finder.git
   cd subdomain-finder
   ```

2. Run the script:

   ```bash
   python subdomain_finder.py
   ```

3. Enter the domain (e.g., `example.com`) when prompted, and let the script crawl the subdomains for you.

## Example

```bash
Enter the domain (e.g., example.com): example.com

[INFO] Crawling potential subdomains using google...
[INFO] Crawling potential subdomains using yandex...
[INFO] Crawling potential subdomains using bing...
[INFO] Crawling potential subdomains using duckduckgo...

[INFO] Resolving DNS records for crawled subdomains...
[VALID] subdomain1.example.com -> 192.168.1.1
[VALID] subdomain2.example.com -> 192.168.1.2

=== Results ===
Subdomain: subdomain1.example.com
  CMS: WordPress
  IP Address: 192.168.1.1
  ASN: 12345
  ASN Description: Example ASN
  Network: Example Network
  Country: US

Subdomain: subdomain2.example.com
  CMS: Joomla
  IP Address: 192.168.1.2
  ASN: 67890
  ASN Description: Another ASN
  Network: Another Network
  Country: UK
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork this repository and submit pull requests for any improvements. If you have any suggestions or issues, please open an issue in the Issues section.

## Screenshot

![Screenshot](screenshot.png)

---

### About

This project was created to automate the process of finding subdomains of a given domain and provide detailed information about them. It's useful for penetration testing, security assessments, or general curiosity about a domain's infrastructure.
```

### **Penjelasan Markdown:**

- **`#` dan `##`**: Digunakan untuk membuat judul dan subjudul.
- **`-` dan `*`**: Untuk membuat daftar item (bullet points).
- **```bash** dan **```**: Menampilkan kode atau perintah terminal.
- **`![Screenshot](screenshot.png)`**: Untuk menambahkan gambar screenshot dari aplikasi.
- **`[LICENSE](LICENSE)`**: Untuk menautkan file lisensi jika ada di repositori Anda.

### **Cara Menggunakan**

1. Copy seluruh konten di atas.
2. Buat atau edit file `README.md` di repositori GitHub Anda.
3. Paste konten ke dalam file `README.md`.
4. **Commit dan push** perubahan ke repositori Anda.

Jika Anda membutuhkan penyesuaian lebih lanjut atau ada hal lain yang ingin ditambahkan, beri tahu saya!
