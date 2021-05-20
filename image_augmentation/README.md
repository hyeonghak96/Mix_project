### 이미지 자동 회전 및 라벨링

라벨링된 이미지에 대하여 각각 시계방향으로 90도, 180도, 270도 회전한 이미지와 json 파일을 생성합니다.

* `rotate.py` 파일을 실행시킨 뒤 라벨링 된 이미지가 저장되어있는 폴더 경로를 입력합니다.

  > 이때 `C:\Users\SH\Desktop\bigdata\final_project\image_morph` 와 같이 역슬래시로 구분된 경로가 아닌 
  >
  > `C:/Users/SH/Desktop/bigdata/final_project/openCV_examples/image_add_test` 와 같이 슬래시로 구분된 경로를 입력해야 합니다.

* 주의사항
  * 대상으로 지정한 폴더 안에는 __이미지 파일__과 __이미지를 라벨링한 `*.json` 파일__만 존재해야 합니다.
  * 폴더 안의 모든 이미지 파일은 라벨링이 되어 있어야 합니다.
  * `*.json` 파일 내부의 `imageData` 값은 모두 `null` 로 지정합니다. `labelme` 를 실행시켜 변형된 모든 이미지에 대하여 save as를 수행하여 덮어쓰면 `imageData` 값을 얻을 수 있습니다.
  * _참고) `imageData` 값은 base64 와 관련된 것 같지만 `labelme` 내부적으로 추가적인 프로세스가 있는 것 같으므로 `null` 값으로 두었습니다. `labelme`를 통해서 생성하는것이 안전하며, 이때 키보드, 마우스 매크로를 사용하세요_

