G마켓 베스트 100 → 텔레그램 자동화 (GitHub Actions 무료 클라우드)

중요한 보안 안내
- 채팅에 노출했던 예전 봇 토큰은 BotFather에서 /revoke로 폐기하고 새 토큰을 발급하세요.
- 새 토큰을 ChatGPT 대화, 공개 코드, README에 붙여넣지 마세요.
- GitHub Settings > Secrets and variables > Actions에 Secret으로 저장합니다.
- 저장소 공개 여부와 무관하게 Secrets 값은 코드에 직접 넣지 않습니다.

1. GitHub 계정 만들기/로그인
https://github.com/

2. 새 저장소 만들기
- 오른쪽 위 + > New repository
- Repository name: gmarket-best100-telegram
- Public을 선택하면 표준 GitHub-hosted runner 실행이 무료입니다.
  (코드가 공개되지만 토큰/채팅 ID는 Secrets에만 저장하면 공개되지 않습니다.)
- Add a README file은 체크하지 않아도 됩니다.
- Create repository 클릭

3. 파일 업로드
- 저장소 페이지에서 Add file > Upload files
- 이 ZIP을 먼저 압축 풀고, 안에 있는 파일/폴더를 업로드합니다.
- gmarket_best100.py 파일과 .github/workflows/daily.yml 경로가 저장소 최상위 기준으로 유지되어야 합니다.
- Commit changes 클릭
  * .github 폴더가 보이지 않으면 압축을 푼 폴더 안에서 해당 폴더를 포함해 업로드하세요.

4. 텔레그램에서 Chat ID 확인
- 텔레그램에서 본인 봇을 열고 Start를 누른 뒤 /start를 보냅니다.
- Chat ID 확인을 위해 봇 토큰을 주소창에 직접 입력하는 방식은 브라우저 기록에 남을 수 있어 권장하지 않습니다.
- 쉬운 방법: PC에서 Python이 있다면 아래 파일 `get_chat_id.py`를 실행하고, 새 토큰을 입력하면 숫자 Chat ID가 출력됩니다.
- 출력된 Chat ID는 본인 텔레그램 대화 식별자입니다. 토큰처럼 공개하지 마세요.

5. GitHub Secrets 등록
저장소의 Settings > Secrets and variables > Actions > New repository secret을 눌러 아래 두 개를 각각 추가합니다.
- Name: TELEGRAM_BOT_TOKEN / Secret: BotFather에서 새로 발급한 토큰
- Name: TELEGRAM_CHAT_ID / Secret: get_chat_id.py가 출력한 숫자
각각 Add secret으로 저장합니다.

6. 첫 실행 테스트
- 저장소 > Actions 탭으로 이동
- 왼쪽에서 Gmarket Best 100 Telegram 선택
- Run workflow > Run workflow를 눌러 수동 실행
- 실행이 초록색 체크로 끝나면 텔레그램을 확인합니다.
- 빨간 X면 해당 실행을 클릭해 오류 로그를 확인하세요. 로그에 토큰을 출력하지 마세요.

7. 매일 자동 실행
- 워크플로는 매일 한국 시간 오전 9시 5분으로 설정돼 있습니다.
- GitHub 예약 실행은 바쁠 때 늦어질 수 있어 정확한 분 단위 도착은 보장되지 않습니다.
- 공개 저장소는 60일 동안 저장소 활동이 없으면 예약 실행이 자동 비활성화될 수 있으므로, 가끔 Actions 탭에서 상태를 확인하세요.

무료 사용/추가 비용 방지
- 공개 저장소 + 표준 GitHub-hosted runner 조합은 GitHub Actions 실행 비용이 무료입니다.
- 더 큰 runner나 별도 유료 서비스는 사용하지 않습니다.
- 혹시 비공개 저장소로 바꾸면 GitHub Free의 월별 무료 실행 시간 한도가 적용됩니다. 이 작업은 짧게 실행되지만, 사용량과 계정 설정을 확인하세요.
- GitHub Settings > Billing and licensing에서 사용량/예산 알림을 확인하고, 사용량 기반 유료 제품이나 더 큰 runner를 선택하지 마세요.
- 텔레그램 봇은 무료입니다.

제한사항
- G마켓 페이지가 바뀌거나 봇 차단/동적 렌더링이 발생하면 수집이 실패할 수 있습니다.
- 80개 미만만 감지되면 잘못된 보고를 막기 위해 메시지를 보내지 않고 실패 처리합니다. 80~99개 감지되면 감지된 개수만 보냅니다.
- 상품 가격은 옵션, 쿠폰, 회원 조건에 따라 달라질 수 있습니다. 첫 보고서의 순위·상품명·가격·링크를 G마켓 페이지와 대조해 주세요.
- 이 버전은 매일 순위·상품명·가격·링크만 보내며, 전날 순위 비교는 하지 않습니다.
