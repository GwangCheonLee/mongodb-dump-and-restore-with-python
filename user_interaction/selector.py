import os


def validate_environment_variable(prompt: str, variable_name: str) -> str:
    variable = os.environ.get(variable_name)
    if variable is None:
        return input(prompt)

    return variable


def select_mode() -> int:
    while True:
        print("모드를 선택해주세요:")
        print("1: 스냅샷")
        print("2: 백업")
        print("3: 복원")
        choice = input("선택: ")
        if choice in ['1', '2', '3']:
            return int(choice)
        print("잘못된 선택입니다. 1, 2, 3 중에서 선택해주세요.")


def get_user_database_choice(databases):
    print("사용할 데이터베이스를 선택하세요:")
    print("1. 전체")
    for index, db_name in enumerate(databases, start=2):
        print(f"{index}. {db_name}")

    choice = input("선택 : ").strip()

    if choice == '1':
        return databases

    try:
        selected_indexes = [int(x) - 1 for x in choice.split(',')]
        selected_dbs = [databases[i - 1] for i in selected_indexes]
        return selected_dbs
    except (IndexError, ValueError):
        print("잘못된 입력입니다. 올바른 숫자를 입력해주세요.")
        return get_user_database_choice(databases)


def select_dump_folder(dump_path='./dump'):
    try:
        snapshots = [s for s in os.listdir(dump_path) if os.path.isdir(os.path.join(dump_path, s))]
        snapshots.sort(reverse=True)
    except FileNotFoundError:
        print("지정된 경로가 존재하지 않습니다.")
        return None

    if not snapshots:
        print("폴더 내에 스냅샷 디렉토리가 없습니다.")
        raise ValueError("폴더 내에 스냅샷 디렉토리가 없습니다.")

    print("복원할 스냅샷 폴더를 선택해주세요:")
    for index, snapshot in enumerate(snapshots, start=1):
        print(f"{index}. {snapshot}")

    snapshot_choice = input("번호를 선택하세요: ")
    if not snapshot_choice.isdigit() or not 1 <= int(snapshot_choice) <= len(snapshots):
        print("잘못된 입력입니다.")
        return

    selected_snapshot = snapshots[int(snapshot_choice) - 1]
    snapshot_path = os.path.join(dump_path, selected_snapshot)
    databases = [db for db in os.listdir(snapshot_path) if os.path.isdir(os.path.join(snapshot_path, db))]

    if not databases:
        print("선택된 스냅샷 폴더 내에 데이터베이스 폴더가 없습니다.")
        raise ValueError("선택된 스냅샷 폴더 내에 데이터베이스 폴더가 없습니다.")

    print("복원할 데이터베이스 폴더를 선택해주세요: ")
    print("1. 전체")
    for index, database in enumerate(databases, start=2):
        print(f"{index}. {database}")

    database_choice = input("번호를 선택해주세요: ")
    if database_choice == '1':
        selected_databases = databases
    else:
        selected_indices = database_choice.split(',')
        try:
            selected_databases = [databases[int(index) - 2] for index in selected_indices]
        except (IndexError, ValueError):
            print("잘못된 입력입니다. 올바른 번호를 입력해주세요.")
            return

    selected_collections_info = []
    for db in selected_databases:
        database_path = os.path.join(snapshot_path, db)
        collections = [f for f in os.listdir(database_path) if f.endswith('.json')]
        for col in collections:
            collection_path = os.path.join(database_path, col)
            collection_info = {
                "database_name": db,
                "collection_name": os.path.splitext(col)[0],
                "file_path": collection_path
            }
            selected_collections_info.append(collection_info)

    return selected_collections_info
