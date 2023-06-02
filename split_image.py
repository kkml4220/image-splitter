import sys
import cv2
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 出力先のディレクトリを指定
OUTPUT_DIR_NAME = "output"
# 出力ファイルの画像形式
OUTPUT_IMAGE_EXTENTION = "png"

# openCV imwriteの仕様により指定できるフォーマットは限定されています
# 詳しくはopenCV imwriteのドキュメントをご確認ください
# URL: https://docs.opencv.org/3.4/d4/da8/group__imgcodecs.html#gabbc7ef1aa2edfaa87772f1202d67e0ce

# 出力ファイル名のprefix
OUTPUT_FILE_PREFIX = "splitted"


def normalize_path(path):
    """パスを正規化
    Unix系のOSでは"/"を使うがWindowsでは"\\"を使うため,
    これを"/"に正規化する
    """
    return os.path.normpath(path.replace('/', '\\'))


def get_output_dir_path():
    """outputディレクトへのパスを取得

    Returns (str): outputディレクトリへの絶対パス
    """
    output_dir_path = os.path.join(BASE_DIR, OUTPUT_DIR_NAME)

    # outputディレクトリが存在しない場合
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    return output_dir_path


def get_file_basename_without_extention(filepath):
    """ファイルのパスから拡張子なしのファイル名を取得

    Returns (str): 拡張子なしのファイル名
    """
    # ファイル名を取得
    basename = os.path.basename(filepath)
    file_name_without_extention = os.path.splitext(basename)[0]

    return file_name_without_extention


def is_absolute_path(path):
    """絶対パスか判定

    Returns (bool): 絶対パスだったらTrue, 相対パスならFalse
    """
    return os.path.isabs(path)


def get_absolute_path(path):
    """ファイルの絶対パスを取得

    Returns (str): ファイルの絶対パスを取得
    """
    if not is_absolute_path(path):
        absolute_path = os.path.abspath(path)
    else:
        absolute_path = path

    if not os.path.exists(absolute_path):
        raise FileNotFoundError(f"{absolute_path}が見つかりません")

    return absolute_path


def decorator_print_arguments_and_result(original_function):
    """引数と結果を描画するデコレータ"""
    def wrapper_function(*args, **kwargs):
        # 引数の表示
        print("=" * 60)
        print(f"引数: {args}, {kwargs}")
        # 関数の実行
        result = original_function(*args, **kwargs)
        # 結果の表示
        print(f"結果: {result}")
        print("=" * 60)

        return result
    return wrapper_function


def get_output_filename(filepath, col, row):
    """出力ファイルのファイル名を取得
    Args:
        filepath (str): 入力ファイルのファイルパス
        col (int): 行番号
        row (int): 列番号
    Returns:
        str: 出力ファイルのファイル名
    """
    filename_without_extention = get_file_basename_without_extention(filepath)
    output_filename = f"{OUTPUT_FILE_PREFIX}_{filename_without_extention}_{str(col)}_{str(row)}.{OUTPUT_IMAGE_EXTENTION}"

    return output_filename


@decorator_print_arguments_and_result
def split_image(filepath, cols, rows):

    # 分割数に対して画像数は+1
    cols += 1
    rows += 1

    otuput_dir_path = get_output_dir_path()
    output_files = []

    # 画像の読み込み
    image = cv2.imread(filepath)
    # 画像のサイズを取得
    height, width = image.shape[:2]
    # 分割後の各領域の高さと幅の計算
    row_height = height // rows
    col_width = width // cols

    # 画像の分割と保存
    for row in range(rows):
        for col in range(cols):
            start_row = row * row_height
            end_row = start_row + row_height
            start_col = col * col_width
            end_col = start_col + col_width

            splitted_image = image[start_row:end_row, start_col:end_col]

            # 出力ファイル名のフォーマット
            output_name = get_output_filename(filepath, row, col)
            output_file_path = os.path.join(otuput_dir_path, output_name)
            cv2.imwrite(output_file_path, splitted_image)
            output_files.append(output_file_path)

    return output_files


def is_integer(value):
    """整数かどうか判定"""
    if isinstance(value, int):
        return True
    else:
        return False


class ValidationError(Exception):
    """バリデーションエラー"""

    def __init__(self, message="バリデーションエラーです"):
        self.message = message
        super().__init__(self.message)


def validation_check(input_file_path, cols, rows):
    """入力時のバリデーションチェック"""

    # ファイルが存在するか確認
    if not os.path.exists(input_file_path):
        raise ValidationError(f"{input_file_path}が見つかりません")

    # 分割数が整数か確認
    if not (is_integer(cols) and is_integer(rows)):
        return False

    # 分割数が非負であることを確認
    if not (rows >= 0 and cols >= 0):
        return False

    return True


def main():
    args = sys.argv

    if len(args) != 4:
        raise ValidationError("コマンドライン引数が無効です")

    # 引数の受け取り
    input_file_path = get_absolute_path(
        normalize_path(args[1]))
    cols = int(args[2])
    rows = int(args[3])

    # バリデーションチェック
    if validation_check(input_file_path, cols, rows):
        split_image(input_file_path, cols, rows)


if __name__ == '__main__':
    main()
