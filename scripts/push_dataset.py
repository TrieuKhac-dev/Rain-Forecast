"""
push_dataset.py - Quản lý ClearML Dataset: tạo, thêm/xóa file, upload & finalize

Cách dùng:
    # Tạo dataset mới (có thể tự lấy tên và project từ parent nếu không cung cấp)
    python push_dataset.py --create --name <tên_dataset> --project <tên_project> [--parent_id <id>]
    python push_dataset.py --create --parent_id <id>   (tự lấy tên và project từ dataset cha)

    # Thao tác trên dataset đã có (bắt buộc --id)
    python push_dataset.py --id <dataset_id> [--add_files <file1> <file2> ...] [--remove_files <file1> ...] \\
        [--list] [--push]

    # Kết hợp nhiều hành động trong một lệnh (tạo + thêm file + push)
    python push_dataset.py --create --parent_id <id> --add_files data/ --push

    # Xem danh sách file
    python push_dataset.py --id <id> --list

Ví dụ:
    python push_dataset.py --create --parent_id 20405283ee7d4682afc7f1a4eac12666
    python push_dataset.py --create --name "new_test_dataset" --project "test-project" --parent_id abc123
    python push_dataset.py --create --parent_id 20405283ee7d4682afc7f1a4eac12666 --add_files ./data --push
    python push_dataset.py --id "83a4563bc78c4632837d0d5fc30f3077" --add_files ./data --push
    python push_dataset.py --id "83a4563bc78c4632837d0d5fc30f3077" --list

Lưu ý:
    - --name, --project không bắt buộc nếu có --parent_id (khi đó lấy từ dataset cha).
    - Nếu có cả --parent_id và --name/--project thì ưu tiên dùng giá trị do người dùng cung cấp.
    - Có thể import các hàm để dùng trong script khác.
"""

import argparse
import os
import sys

from clearml import Dataset

try:
    from find_dataset import get_dataset_by_id
except ImportError:
    get_dataset_by_id = None


def create_dataset(name, project, parent_id=None):
    if parent_id:
        ds = Dataset.create(
            dataset_name=name, dataset_project=project, parent_datasets=[parent_id]
        )
    else:
        ds = Dataset.create(dataset_name=name, dataset_project=project)
    print("Tạo dataset thành công!")
    print(f"ID: {ds.id}, Tên: {ds.name}, Project: {ds.project}")
    return ds


def add_files_to_dataset(dataset: Dataset, files: list[str]):
    added = []
    for f in files:
        if os.path.exists(f):
            dataset.add_files(f)
            added.append(f)
        else:
            print(f"[Cảnh báo] File không tồn tại: {f}")
    return added


def remove_files_from_dataset(dataset: Dataset, files: list[str]):
    for f in files:
        dataset.remove_files(f)


def list_dataset_files(dataset: Dataset):
    return dataset.list_files()


def push_dataset(dataset: Dataset):
    dataset.upload()
    dataset.finalize()
    print("Đã upload và finalize dataset!")


def main():
    parser = argparse.ArgumentParser(
        description="Quản lý ClearML Dataset: tạo, thêm/xóa file, upload & finalize"
    )
    parser.add_argument("--create", action="store_true", help="Tạo dataset mới")
    parser.add_argument(
        "--name", help="Tên dataset (không bắt buộc nếu có --parent_id)"
    )
    parser.add_argument(
        "--project", help="Tên project (không bắt buộc nếu có --parent_id)"
    )
    parser.add_argument("--parent_id", help="ID dataset cha (tùy chọn khi --create)")
    parser.add_argument(
        "--id", help="ID dataset để thao tác (bắt buộc khi không --create)"
    )
    parser.add_argument(
        "--add_files",
        nargs="+",
        help="Thêm file vào dataset (yêu cầu --id hoặc dùng cùng --create)",
    )
    parser.add_argument(
        "--remove_files", nargs="+", help="Xóa file khỏi dataset (yêu cầu --id)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Liệt kê các file trong dataset (yêu cầu --id)",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Upload và finalize dataset (yêu cầu --id hoặc dùng cùng --create)",
    )
    args = parser.parse_args()

    # Xử lý tạo mới
    if args.create:
        # Lấy name và project từ parent nếu thiếu
        if args.parent_id:
            if get_dataset_by_id is None:
                print(
                    "Không import được get_dataset_by_id từ find_dataset.py. Không thể lấy thông tin parent."
                )
                sys.exit(1)
            parent_dataset = get_dataset_by_id(args.parent_id)
            if parent_dataset is None:
                print(f"Không tìm thấy dataset cha với id={args.parent_id}")
                sys.exit(1)
            if not args.name:
                args.name = parent_dataset.name
                print(f"Tự động lấy tên dataset từ parent: {args.name}")
            if not args.project:
                args.project = parent_dataset.project
                print(f"Tự động lấy project từ parent: {args.project}")
        if not args.name or not args.project:
            print(
                "--create yêu cầu --name và --project (hoặc --parent_id để lấy tự động)"
            )
            sys.exit(1)

        ds = create_dataset(args.name, args.project, args.parent_id)
        print(f"Dataset id: {ds.id}")

        # Nếu có các thao tác thay đổi (add_files, remove_files, push) thì thực hiện trên dataset vừa tạo
        if args.add_files or args.remove_files or args.push:
            args.id = ds.id  # gán ID để xử lý ở phần dưới
        else:
            return  # không có thao tác gì thêm thì kết thúc

    # Các thao tác còn lại đều yêu cầu --id (đã được gán nếu từ --create)
    if not args.id:
        print("Các thao tác này yêu cầu --id. Nếu muốn tạo mới, hãy dùng --create.")
        sys.exit(1)
    if get_dataset_by_id is None:
        print("Không import được get_dataset_by_id từ find_dataset.py.")
        sys.exit(1)
    dataset = get_dataset_by_id(args.id)
    if dataset is None:
        print(f"Không tìm thấy dataset với id={args.id}")
        sys.exit(1)
    if dataset.is_final():
        print("Dataset đã finalize, không thể chỉnh sửa.")
        sys.exit(1)

    # Truy vấn
    if args.list:
        files = list_dataset_files(dataset)
        print("Danh sách file đã add vào dataset:")
        for f in files:
            print(f)
        # Nếu chỉ list thì không thực hiện thay đổi
        if not (args.add_files or args.remove_files or args.push):
            return

    # Thao tác thay đổi
    if args.add_files:
        added = add_files_to_dataset(dataset, args.add_files)
        if added:
            print(f"Đã thêm file: {added}")
    if args.remove_files:
        remove_files_from_dataset(dataset, args.remove_files)
        print(f"Đã xóa file: {args.remove_files}")
    if args.push:
        push_dataset(dataset)


if __name__ == "__main__":
    main()
