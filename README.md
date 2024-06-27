# 환경
python=3.11

# KT에이블스쿨 5기 충남/충북 21조 
## 깃 클론 및 브랜치 연결 방법
1. 클론할 경로로 이동
- cd 폴더경로

2. 깃 클론 
- git clone 

3. 원격 저장소 연결 확인 
- git remote -v 포크한 자기 로컬명
- git checkout -t 새로컬브랜치명 origin/원격브랜치명
- 원격 브랜치를 기반으로 새 로컬 브랜치를 생성하고 해당 브랜치로 전환합니다
- 이 명령은 origin/원격브랜치명을 기반으로 로컬에서 새 로켤 브랜치 명 이라는 이름의 브랜치를 생성하고, 이 브랜치가 원격 브랜치를 자동으로 추적하도록 설정합니다. 이렇게 설정하면 git push나 git pull 명령을 사용할 때 원격 브랜치 이름을 명시하지 않아도 됩니다.

4. 원준님 레포를 갖고오기 위한 upstream 설정
- git remote add uptream 원준님레포주소
- 현재 체크아웃 위치 확인하고 특정 브랜치에 원준님 새 내용을 갖고오고 싶으면 그 브랜치로 이동하기! 안하면 현재 체크아웃 되어있는 브랜치로 내용 와짐
- git pull upstream 원준님꺼에서갖고올브랜치명
- 갈등발생시 vscode 켜서 갈등부분 확인하고 자신이 원하는 걸로 다시 작성 및 저장
- git add > git commit > git push 순으로 하면 자신이 현재 체크아웃 되어있는 브랜치로 이 내용 푸시. 원준님한테는 영향 X 

5. 원준님 깃에 합치고 싶다면, ? 
- 자기 깃헙 들어가서 브랜치 설정 후 옆에 synk fort 누르기
- open pull request 클릭
- 만약 싱크포크가 안뜬다? 하면 풀 리퀘스트 탭 클릭 
- 풀 리퀘스트 생성
- 상위 머지 경로 설정
- 
## 기본 커맨드 모음
- git init : 현재 디렉토리를 Git이 관리하는 프로젝트 디렉토리(=working directory)로 - 설정하고 그 안에 레포지토리(.git 디렉토리) 생성
- git config user.name 'codeit' : 현재 사용자의 아이디를 'codeit'으로 설정(커밋할 - 때 필요한 정보)
- git config user.email 'teacher@codeit.kr' : 현재 사용자의 이메일 주소를 - 'teacher@codeit.kr'로 설정(커밋할 때 필요한 정보)
- git add [파일 이름] : 수정사항이 있는 특정 파일을 staging area에 올리기
- git add [디렉토리명] : 해당 디렉토리 내에서 수정사항이 있는 모든 파일들을 staging - area에 올리기
- git add . : working directory 내의 수정사항이 있는 모든 파일들을 staging area에 - 올리기
- git reset [파일 이름] : staging area에 올렸던 파일 다시 내리기
- git status : Git이 현재 인식하고 있는 프로젝트 관련 내용들 출력(문제 상황이 - 발생했을 때 현재 상태를 파악하기 위해 활용하면 좋음)
- git commit -m "커밋 메시지" : 현재 staging area에 있는 것들 커밋으로 남기기
- git help [커맨드 이름] : 사용법이 궁금한 Git 커맨드의 공식 메뉴얼 내용 출력
- 
- 
- git remote add origin 주소
- git branch -M main
- git push -u origin main : 로컬 레포지토리의 내용을 처음으로 리모트 레포지토리에 - 올릴 때 사용합니다.(-u origin master가 무슨 뜻인지는 'Git에서 브랜치 사용하기' - 챕터에서 배울 거니까 걱정마세요!)
- git push : 로컬 레포지토리의 내용을 리모트 레포지토리에 보내기
- git pull : 리모트 레포지토리의 내용을 로컬 레포지토리로 가져오기
- git clone [프로젝트의 GitHub 상 주소] : GitHub에 있는 프로젝트를 내 컴퓨터로 - 가져오기git log : 커밋 히스토리를 출력
- git log --pretty=oneline : --pretty 옵션을 사용하면 커밋 히스토리를 다양한 - 방식으로 출력할 수 있습니다. --pretty 옵션에 oneline이라는 값을 주면 커밋 하나당 한 - 줄씩 출력해줍니다. --pretty 옵션에 대해 더 자세히 알고싶으면 이 링크를 참고하세요.
- git show [커밋 아이디] : 특정 커밋에서 어떤 변경사항이 있었는지 확인
- git commit --amend : 최신 커밋을 다시 수정해서 새로운 커밋으로 만듦
- git config alias.[별명] [커맨드] : 길이가 긴 커맨드에 별명을 붙여서 이후로 - 별명으로 해당 커맨드를 실행할 수 있도록 설정
- git diff [커밋 A의 아이디] [커밋 B의 아이디] : 두 커밋 간의 차이 비교
- git reset [옵션] [커밋 아이디] : 옵션에 따라 하는 작업이 달라짐(옵션을 생략하면 - --mixed 옵션이 적용됨)(2) staging area도 특정 커밋처럼 리셋(--mixed는 여기까지 - 수행)그리고 이때 커밋 아이디 대신 HEAD의 위치를 기준으로 한 표기법(예 : HEAD^, - HEAD~3)을 사용해도 됨
- (3) working directory도 특정 커밋처럼 리셋(--hard는 여기까지 수행)
- (1) HEAD가 특정 커밋을 가리키도록 이동시킴(--soft는 여기까지 수행)
- git tag [태그 이름] [커밋 아이디] : 특정 커밋에 태그를 붙임
- git branch [새 브랜치 이름]: 새로운 브랜치를 생성
- git checkout -b [새 브랜치 이름]: 새로운 브랜치를 생성하고 그 브랜치로 바로 이동
- git branch -d [기존 브랜치 이름]: 브랜치 삭제
- git checkout [기존 브랜치 이름]: 그 브랜치로 이동
- git merge [기존 브랜치 이름]: 현재 브랜치에 다른 브랜치를 머지
- git merge --abort: 머지를 하다가 conflict가 발생했을 때, 일단은 머지 작업을 - 취소하고 이전 상태로 돌아감- git show [커밋 아이디] : 특정 커밋에서 어떤 변경사항이 있었는지 확인
- git commit --amend : 최신 커밋을 다시 수정해서 새로운 커밋으로 만듦
- git config alias.[별명] [커맨드] : 길이가 긴 커맨드에 별명을 붙여서 이후로 - 별명으로 해당 커맨드를 실행할 수 있도록 설정
- git diff [커밋 A의 아이디] [커밋 B의 아이디] : 두 커밋 간의 차이 비교
- git reset [옵션] [커밋 아이디] : 옵션에 따라 하는 작업이 달라짐(옵션을 생략하면 - --mixed 옵션이 적용됨)(2) staging area도 특정 커밋처럼 리셋(--mixed는 여기까지 - 수행)그리고 이때 커밋 아이디 대신 HEAD의 위치를 기준으로 한 표기법(예 : HEAD^, - HEAD~3)을 사용해도 됨
- (3) working directory도 특정 커밋처럼 리셋(--hard는 여기까지 수행)
- (1) HEAD가 특정 커밋을 가리키도록 이동시킴(--soft는 여기까지 수행)
- git tag [태그 이름] [커밋 아이디] : 특정 커밋에 태그를 붙임
- 
- 
- 
- 
- 
- git branch [새 브랜치 이름]: 새로운 브랜치를 생성
- git checkout -b [새 브랜치 이름]: 새로운 브랜치를 생성하고 그 브랜치로 바로 이동
- git branch -d [기존 브랜치 이름]: 브랜치 삭제
- git checkout [기존 브랜치 이름]: 그 브랜치로 이동
- git merge [기존 브랜치 이름]: 현재 브랜치에 다른 브랜치를 머지
- git merge --abort: 머지를 하다가 conflict가 발생했을 때, 일단은 머지 작업을 - 취소하고 이전 상태로 돌아감

- 희승 머지부탁드립니당 당 
