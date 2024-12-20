document.addEventListener("DOMContentLoaded", () => {
    const audioAPI = "/api/get-audio-files";

    // 방송 목록 업데이트
    function updateBroadcastList(files) {
        const tableBody = document.getElementById("broadcast-table");
        tableBody.innerHTML = "";

        files.forEach((file, index) => {
            const row = document.createElement("tr");

            const numberCell = document.createElement("td");
            numberCell.textContent = index + 1;
            row.appendChild(numberCell);

            const titleCell = document.createElement("td");
            const titleLink = document.createElement("a");
            titleLink.textContent = file.title;
            titleLink.href = "#";
            titleLink.addEventListener("click", (event) => {
                event.preventDefault();
                playAudio(`/audio/${file.filename}`);
            });
            titleCell.appendChild(titleLink);
            row.appendChild(titleCell);

            tableBody.appendChild(row);
        });
    }

    // 오디오 재생 함수
    function playAudio(src) {
        const audio = new Audio(src);
        audio.play().catch((error) => {
            console.error("Audio playback failed:", error);
        });
    }

    // 방송 목록 로드
    fetch(audioAPI)
        .then((response) => response.json())
        .then((files) => {
            updateBroadcastList(files);
        })
        .catch((err) => {
            console.error("Error loading audio files:", err);
        });
});
