import {ref} from "@vue/reactivity";

import perks from "./perks";
import media from "./mediaNotification.js";
import state from "./state";

const audio = ref(new Audio()).value;

const pos = ref(0);
const current_time = ref(0);

const playing = ref(state.is_playing);

const url = "http://0.0.0.0:9876/file/";

const playAudio = (trackid) => {
    const elem = document.getElementById('progress');

    const full_path = url + encodeURIComponent(trackid);

    new Promise((resolve, reject) => {
        audio.src = full_path;
        audio.oncanplaythrough = resolve;
        audio.onerror = reject;
    })
        .then(() => {
            audio.play().then(() => {
                    perks.focusCurrent()
                    state.is_playing.value = true;
                }
            );
            audio.ontimeupdate = () => {
                current_time.value = audio.currentTime;
                pos.value = (audio.currentTime / audio.duration) * 100;
                let bg_size = ((audio.currentTime / audio.duration) * 100)

                elem.style.backgroundSize = `${bg_size}% 100%`;
            };
        })
        .catch((err) => console.log(err));
};

function playNext() {
    playAudio(perks.next.value.trackid);
    perks.current.value = perks.next.value;
    media.showMediaNotif();
}

function playPrev() {
    playAudio(state.prev.value.trackid);
    perks.current.value = perks.prev.value;
}

function seek(position) {
    audio.currentTime = (position / 100) * audio.duration;
}

function playPause() {
    if (audio.src === "") {
        playAudio(perks.current.value.trackid);
    }

    if (audio.paused) {
        audio.play();
    } else {
        audio.pause();
    }
}

audio.addEventListener("play", () => {
    state.is_playing.value = true;
});

audio.addEventListener("pause", () => {
    state.is_playing.value = false;
});

audio.addEventListener("ended", () => {
    playNext();
});

export default {playAudio, playNext, playPrev, playPause, seek, pos, playing, current_time};


// TODO
// Try implementing classes to play audio .ie. Make the seek, playNext, playPrev, etc the methods of a class. etc
