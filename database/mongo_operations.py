import json
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from user_interaction.selector import validate_environment_variable, get_user_database_choice, select_dump_folder
from utils.file_utils import ensure_directory

DUMP_FOLDER = './dump'
TIMESTAMP_PATH = f"{DUMP_FOLDER}/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}"


async def perform_snapshot():
    ensure_directory(TIMESTAMP_PATH)
    DUMP_MONGODB_URL = validate_environment_variable("MongoDB URL을 입력해주세요: ", "DUMP_MONGODB_URL")
    client = AsyncIOMotorClient(DUMP_MONGODB_URL)
    databases = await get_databases(client)

    for db_name in databases:
        ensure_directory(f"{TIMESTAMP_PATH}/{db_name}")
        db = client[db_name]
        collections = await db.list_collection_names()

        for collection_name in collections:
            await save_documents_to_json(client, db_name, collection_name)


async def perform_dump():
    ensure_directory(TIMESTAMP_PATH)
    DUMP_MONGODB_URL = validate_environment_variable("MongoDB URL을 입력해주세요: ", "DUMP_MONGODB_URL")

    client = AsyncIOMotorClient(DUMP_MONGODB_URL)
    databases = await get_databases(client)

    choice_databases = get_user_database_choice(databases)

    for db_name in choice_databases:
        ensure_directory(f"{TIMESTAMP_PATH}/{db_name}")
        db = client[db_name]
        collections = await db.list_collection_names()

        for collection_name in collections:
            await save_documents_to_json(client, db_name, collection_name)


async def perform_restore():
    RESTORE_MONGODB_URL = validate_environment_variable("MongoDB URL을 입력해주세요: ", "RESTORE_MONGODB_URL")
    client = AsyncIOMotorClient(RESTORE_MONGODB_URL)
    user_choice_snapshot_dict_list = select_dump_folder()

    for user_choice_snapshot_dict in user_choice_snapshot_dict_list:
        await restore_collection_from_json(client=client, db_name=user_choice_snapshot_dict["database_name"],
                                           collection_name=user_choice_snapshot_dict["collection_name"],
                                           file_path=user_choice_snapshot_dict["file_path"])


async def restore_collection_from_json(client: AsyncIOMotorClient, db_name: str, collection_name: str, file_path: str):
    db = client[db_name]

    existing_dbs = await get_databases(client)
    if db_name in existing_dbs:
        existing_cols = await db.list_collection_names()
        if collection_name in existing_cols:
            await db[collection_name].drop()
            print(f"기존 collection {collection_name}을 삭제하였습니다.")

    collection = db[collection_name]

    with open(file_path, 'r', encoding='utf-8') as file:
        documents = json.load(file)

    if documents:
        await collection.insert_many(documents)
        print(f"데이터베이스: {db_name}, 컬렉션: {collection_name}에 {len(documents)}개의 문서가 복원되었습니다.")


async def get_databases(client: AsyncIOMotorClient):
    databases = await client.list_database_names()

    result_arr = []
    for db_name in databases:
        if db_name not in ["admin", "local", "config"]:
            result_arr.append(db_name)

    return result_arr


async def save_documents_to_json(client: AsyncIOMotorClient, db_name: str, collection_name: str):
    db = client[db_name]
    documents = await db[collection_name].find().to_list(None)

    if len(documents) > 0:
        with open(f"{TIMESTAMP_PATH}/{db_name}/{collection_name}.json", "w", encoding="utf-8") as file:
            json.dump(documents, file, ensure_ascii=False, default=str)
