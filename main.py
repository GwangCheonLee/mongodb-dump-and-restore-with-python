import asyncio

from dotenv import load_dotenv

from database.mongo_operations import perform_snapshot, perform_dump, perform_restore
from user_interaction.selector import select_mode

load_dotenv()


async def main():
    mode = select_mode()

    if mode == 1:
        await perform_snapshot()
    elif mode == 2:
        await perform_dump()
    elif mode == 3:
        await perform_restore()
    else:
        print("잘못된 선택입니다.")


if __name__ == "__main__":
    asyncio.run(main())
