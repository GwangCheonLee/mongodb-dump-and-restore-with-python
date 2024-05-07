import os


def get_required_env(variable_name: str) -> str:
    variable = os.environ.get(variable_name)
    if variable is None:
        raise ValueError(f"{variable_name} 환경 변수가 설정되지 않았습니다.")
    return variable
