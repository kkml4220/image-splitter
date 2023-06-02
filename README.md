# image-splitter

![APM](https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat)
![Editor](https://img.shields.io/badge/-Visual%20Studio%20Code-007ACC.svg?logo=visual-studio-code&style=flat)

分割数を指定して画像を分割

## Demo

### Original

![original](./images/sample_background.png)

### Split image

| ![01](./images/splitted_sample_background_0_0.png) | ![02](./images/splitted_sample_background_0_1.png)| ![03](./images/splitted_sample_background_0_2.png)|
| ![11](./images/splitted_sample_background_1_0.png) | ![12](./images/splitted_sample_background_1_1.png)| ![13](./images/splitted_sample_background_1_2.png)|
| ![21](./images/splitted_sample_background_2_0.png) | ![22](./images/splitted_sample_background_2_1.png)| ![23](./images/splitted_sample_background_2_2.png)|

## Installation

```bash
git clone https://github.com/kkml4220/image-splitter.git
cd image-splitter
pip install -r requirements.txt
```

## Usage

```bash
python split_image.py input/sample_background.png 2 2
```

**分割数に対して分割された画像数は+1 であることに注意してください**

- コマンドライン引数で画像のパスの後に縦、横の分割数を渡すと分割数を変更することができます

## Author

- 作成者 : 高橋 克征 (Takahashi Katsuyuki)
- E-mail : [Takahashi.Katsuyuki.github@gmail.com](Takahashi.Katsuyuki.github@gmail.com)

## License

"image-splitter" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
