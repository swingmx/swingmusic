const putCommas = (artists) => {
  let result = [];

  artists.forEach((i, index, artists) => {
    if (index !== artists.length - 1) {
      result.push(i + ", ");
    } else {
      result.push(i);
    }
  });

  return result;
};

function focusCurrent() {
  const elem = document.getElementsByClassName("currentInQueue")[0];

  if (elem) {
    elem.scrollIntoView({
      behavior: "smooth",
      block: "center",
      inline: "center",
    });
  }
}

function getElem(identifier, type) {
  switch (type) {
    case "class": {
      return document.getElementsByClassName(identifier)[0];
    }
    case "id": {
      return document.getElementById(identifier);
    }
  }
}

function focusSearchBox() {
  const elem = getElem("search", "id");

  elem.focus();
}

let key_down_fired = false;

window.addEventListener("keydown", (e) => {
  let target = e.target;
  let ctrlKey = e.ctrlKey;

  switch (e.key) {
    case "ArrowRight":
      if (target.tagName === "INPUT") return;

      {
        if (!key_down_fired) {
          key_down_fired = true;

          setTimeout(() => {
            key_down_fired = false;
          }, 1000);

          // playAudio.playNext();
        }
      }
      break;

    case "ArrowLeft":
      {
        if (!key_down_fired) {
          if (target.tagName === "INPUT") return;

          key_down_fired = true;

          // playAudio.playPrev();

          setTimeout(() => {
            key_down_fired = false;
          }, 1000);
        }
      }

      break;

    case " ":
      {
        if (!key_down_fired) {
          if (target.tagName === "INPUT") return;
          e.preventDefault();
          key_down_fired = true;

          // playAudio.playPause();
        }
      }

      break;

    case "f": {
      if (!key_down_fired) {
        if (!ctrlKey) return;
        e.preventDefault();
        focusSearchBox();

        key_down_fired = true;
      }
    }
  }
});

window.addEventListener("keyup", () => {
  key_down_fired = false;
});

function formatSeconds(seconds) {
  // check if there are arguments

  const date = new Date(seconds * 1000);

  const hh = date.getUTCHours();
  const mm = date.getUTCMinutes();
  const ss = date.getUTCSeconds();

  let _hh = hh < 10 ? `0${hh}` : hh;
  let _mm = mm < 10 ? `0${mm}` : mm;
  let _ss = ss < 10 ? `0${ss}` : ss;

  if (arguments[1]) {
    if (hh === 1) {
      _hh = hh + " Hour";
    } else {
      _hh = `${hh} Hours`;
    }

    if (mm === 1) {
      _mm = mm + " Minute";
    } else {
      _mm = `${mm} Minutes`;
    }

    if (hh > 0) {
      return `${_hh}, ${_mm}`;
    } else {
      return `${_mm}`;
    }
  }

  if (hh > 0) {
    return `${_hh}:${_mm}:${_ss}`;
  } else {
    return `${_mm}:${_ss}`;
  }
}

export function getCurrentDate(){
  const date = new Date();

  const yyyy = date.getFullYear();
  const mm = date.getMonth() + 1;
  const dd = date.getDate();

  const hh = date.getHours();
  const min = date.getMinutes();
  const sec = date.getSeconds();

  return `${yyyy}-${mm}-${dd} ${hh}:${min}:${sec}`;
}

export default {
  putCommas,
  focusCurrent,
  formatSeconds,
  getElem,
  getCurrentDate
};
