# Coding convention for Python

>From [PEP8](https://www.python.org/dev/peps/pep-0008/), [PEP257](https://www.python.org/dev/peps/pep-0257/), [Google Python style guide](https://google.github.io/styleguide/pyguide.html)



* __전역변수 사용 자제__

  코딩 혼자하는거 아니니 불가피한 경우에만 사용합시다.

  전역변수를 사용해놓은 코드를 남이 보면 매우 알아보기 힘듭니다.

  

* 네이밍 규칙(from PEP8)

  이름은 영문으로만 사용가능합니다.

  | 타입                 | Public               | Internal                          |
  | -------------------- | -------------------- | --------------------------------- |
  | 패키지               | `lower_with_under`   |                                   |
  | 모듈                 | `lower_with_under`   | `_lower_with_under`               |
  | 클래스               | `CapWords`           | `_CapWords`                       |
  | 예외                 | `CapWords`           |                                   |
  | 함수                 | `lower_with_under()` | `_lower_with_under()`             |
  | 글로벌/클래스 상수   | `CAPS_WITH_UNDER`    | `_CAPS_WITH_UNDER`                |
  | 글로벌/클래스 변수   | `lower_with_under`   | `_lower_with_under`               |
  | 인스턴스 변수        | `lower_with_under`   | `_lower_with_under`               |
  | 메서드 이름          | `lower_with_under()` | `_lower_with_under()` (protected) |
  | 함수/메서드 매개변수 | `lower_with_under`   |                                   |
  | 지역 변수            | `lower_with_under`   |                                   |



* docstring(from PEP257, Google Python style guide)

  docstring 은 직접 함수의 코드를 읽어보지 않더라도 충분히 함수를 호출하는 코드를 작성 할 수 있을만큼 정보를 제공해야 하며 다음 사항이 포함되어야 합니다.

  >클래스나 함수의 호출 방법과 의미
  >
  >인수의 자료형
  >
  >리턴값의 자료형
  >
  >인수와 리턴값에 대한 설명
  >
  >예외

  

  ##### *Args:*

  - 매개변수를 각각 이름으로 나열합니다. 각 이름에는 설명문이 따르며 콜론 뒤에 공백이나 새로운 라인으로 분리되어야 합니다.
  - 만약 설명문이 너무 길어 한 줄인 80자를 초과할 경우 매개변수 이름보다 2칸 또는 4칸의 들여쓰기를 사용합니다.
  - 만약 코드가 자료형에 대한 주석을 담고 있지 않다면 설명문은 요구되는 자료형을 포함해서 기록해야 합니다.
  - 함수가 `*foo` 또는 `**bar`를 받는다면 `*foo` 와 `**bar`로 기록되어야 합니다.

  ##### *Returns:* (제너레이터에는 *Yields:*)

  - 반환값의 자료형과 의미를 기록합니다. 만약 함수가 None만을 반환한다면 이 섹션은 필요없습니다.
  - 또한 만약 docstring이 Returns 나 Yields로 시작하거나(e.g. `"""Returns row from Bigtable as a tuple of strings."""`) 충분한 설명이 제공된다면 생략 될 수 있습니다.

  ##### *Raises:*

  - interface와 관련된 모든 예외를 설명 뒤에 나열합니다.
  - `Args:`에 설명된 것과 유사한 예외 이름 + 콜론 + 공백 또는 줄 바꿈과 hanging indent 스타일을 사용하세요.

  <br>

  예시(함수)

  ```python
  def fetch_smalltable_rows(table_handle: smalltable.Table,
                          keys: Sequence[Union[bytes, str]],
                          require_all_keys: bool = False,
                        ) -> Mapping[bytes, Tuple[str]]:
    """Fetches rows from a Smalltable.
  
    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.
  
    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table
          row to fetch.  String keys will be UTF-8 encoded.
        require_all_keys: Optional; If require_all_keys is True only
          rows with values set for all keys will be returned.
  
    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:
  
        {b'Serak': ('Rigel VII', 'Preparer'),
        b'Zim': ('Irk', 'Invader'),
        b'Lrrr': ('Omicron Persei 8', 'Emperor')}
  
        Returned keys are always bytes.  If a key from the keys argument is
        missing from the dictionary, then that row was not found in the
        table (and require_all_keys must have been False).
  
    Raises:
        IOError: An error occurred accessing the smalltable.
    """
  ```

  예시(클래스)

  - 클래스는 선언 바로 아래에 해당 클래스를 설명하는 docstring 를 가지고 있어야 합니다.
  - _만약 클래스가 public attributes 를 가지고 있다면 함수의 `Args`섹션과 같은 형식을 사용해 `Attributes` 섹션을 작성해야 합니다._

  ```python
  class RealDataMediator:
      """
      실시간 데이터 start, terminate 전용 mediator
  
      Attributes:
          process_list: market_data.py 의 실시간데이터 감시용 클래스의 인스턴스를 등록하기 위한 리스트.
      """
      def __init__(self):
          self.process_list = []
  ```

  

  

