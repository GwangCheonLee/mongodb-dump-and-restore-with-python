## **개요**

이 문서는 MongoDB 작업을 수행하는 Docker 애플리케이션의 설정과 실행 방법을 설명합니다. 애플리케이션은 MongoDB 덤프를 복원하는 기능을 포함하며, 사용자는 환경변수를 통해 설정을 조정할 수 있습니다.

## **사용 가능한 환경변수**

애플리케이션은 다음과 같은 환경변수를 입력받아 사용합니다:

- **DUMP_MONGODB_URL**: MongoDB 덤프 데이터베이스의 연결 URL입니다. 덤프 데이터를 가져오는 데 사용됩니다.
- **RESTORE_MONGODB_URL**: MongoDB 복원 데이터베이스의 연결 URL입니다. 데이터 복원 작업에 사용됩니다.

## **볼륨**

애플리케이션에서 사용하는 볼륨은 /app/dump 입니다.

## **Docker 컨테이너 실행 방법**

Docker 컨테이너를 실행할 때는 다음 옵션을 사용해야 합니다:

- **`-rm`**: 컨테이너 종료 후 자동으로 컨테이너를 삭제합니다.
- **`i`**: 컨테이너의 표준 입력을 열어두어 대화형 모드로 실행할 수 있습니다.
- **`-network host`**: 호스트의 네트워크 환경을 사용하여 네트워크 격리 없이 실행합니다.

### **기본 실행 명령어**

```bash
docker run --rm -i --network host \
-e DUMP_MONGODB_URL="mongodb://your_username:your_password@localhost:27017" \
-e RESTORE_MONGODB_URL="mongodb://your_username:your_password@localhost:27017" \
-v "./dump:/app/dump" \
image_name
```