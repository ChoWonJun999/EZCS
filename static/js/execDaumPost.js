function execDaumPostcode() {
    new daum.Postcode({
        oncomplete: function (data) {
            // 팝업을 통한 검색 결과 항목 클릭 시 실행
            var addr = ""; // 주소_결과값이 없을 경우 공백
            var extraAddr = ""; // 참고항목

            //사용자가 선택한 주소 타입에 따라 해당 주소 값을 가져온다.
            if (data.userSelectedType === "R") {
                // 도로명 주소를 선택
                addr = data.roadAddress;
            } else {
                // 지번 주소를 선택
                addr = data.jibunAddress;
            }

            if (data.userSelectedType === "R") {
                if (data.bname !== "" && /[동|로|가]$/g.test(data.bname)) {
                    extraAddr += data.bname;
                }
                if (data.buildingName !== "" && data.apartment === "Y") {
                    extraAddr += extraAddr !== "" ? ", " + data.buildingName : data.buildingName;
                }
                if (extraAddr !== "") {
                    extraAddr = " (" + extraAddr + ")";
                }
            } else {
                document.getElementById("address").value = "";
            }

            // 선택된 우편번호와 주소 정보를 input 박스에 넣는다.
            document.getElementById("addressCode").value = data.zonecode;
            document.getElementById("address").value = addr;
            document.getElementById("address").value += extraAddr;
            document.getElementById("addressDetail").focus(); // 우편번호 + 주소 입력이 완료되었음으로 상세주소로 포커스 이동
        }
    }).open();
}
